import unittest
from app import app
from model.timesheet_status import TimesheetStatus

from service.timesheet_service import TimesheetService
from service.user_service import UserService


class TestTimesheetController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.timesheet_service = TimesheetService()
        self.user_service = UserService()

    def authenticate(self, username, password):
        """
        Helper method to authenticate a user.
        """
        user = {
            "username": username,
            "password": password
        }
        response = self.client.post('/user/login', json=user)
        return response.json['accessToken']

    def test_ensure_timesheet_exists(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwi1', 'test_password')
        # Test for already existing timesheet
        test_existing_timesheet_data = {
            'username': 'testHiwi1',
            'month': 5,
            'year': 2024
        }
        existing_response = self.client.post('/timesheet/ensureExists', json=test_existing_timesheet_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, existing_response.status_code)
        # Test for non-existing timesheet
        test_non_existing_timesheet_data = {
            'username': 'testHiwi1',
            'month': 8,
            'year': 2024
        }
        non_existing_response = self.client.post('/timesheet/ensureExists', json=test_non_existing_timesheet_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(201, non_existing_response.status_code)
        timesheet = self.timesheet_service.get_timesheet('testHiwi1', 8, 2024).data
        self.assertIsNotNone(timesheet)
        # Reset database to original state
        self.timesheet_service.delete_timesheet_by_id(timesheet.timesheet_id)

    def test_sign_timesheet(self):
        """
        Test the sign_timesheet method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwi1', 'test_password')
        response = self.client.patch('/timesheet/sign', json={"_id": "6679ca2935df0d8f7202c5fa"},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheet = self.timesheet_service.get_timesheet('testHiwi1', 5, 2024).data
        self.assertEqual(timesheet.status, TimesheetStatus.WAITING_FOR_APPROVAL)
        # Reset database to original state
        self.timesheet_service._set_timesheet_status(str(timesheet.timesheet_id), TimesheetStatus.NOT_SUBMITTED)

    def test_approve_timesheet(self):
        """
        Test the approve_timesheet method of the TimesheetController class.
        """
        access_token = self.authenticate('testSupervisor1', 'test_password')
        test_timesheet_id = "667bd177cf0aa6181e9c8ddb"

        response = self.client.patch('/timesheet/approve', json={"_id": test_timesheet_id},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheet = self.timesheet_service.get_timesheet_by_id(test_timesheet_id).data
        self.assertEqual(TimesheetStatus.COMPLETE, timesheet.status)
        # Reset database to original state
        self.timesheet_service._set_timesheet_status(str(timesheet.timesheet_id), TimesheetStatus.WAITING_FOR_APPROVAL)

    def test_request_change(self):
        """
        Test the request_change method of the TimesheetController class.
        """
        access_token = self.authenticate('testSupervisor1', 'test_password')
        test_timesheet_id = "667bd177cf0aa6181e9c8ddb"

        response = self.client.patch('/timesheet/requestChange', json={"_id": test_timesheet_id},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheet = self.timesheet_service.get_timesheet_by_id(test_timesheet_id).data
        self.assertEqual(TimesheetStatus.REVISION, timesheet.status)
        # Reset database to original state
        self.timesheet_service._set_timesheet_status(test_timesheet_id, TimesheetStatus.WAITING_FOR_APPROVAL)

    def test_get_timesheets(self):
        """
        Test the get_timesheets method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwi1', 'test_password')
        test_username = "testHiwi1"
        response = self.client.get('/timesheet/get', query_string={"username": test_username},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheets = response.json
        self.assertEqual(3, len(timesheets))
        self.assertEqual(timesheets[0]["username"], test_username)
        self.assertEqual(timesheets[1]["username"], test_username)
        self.assertEqual(timesheets[2]["username"], test_username)

    def test_get_timesheets_by_month_year(self):
        """
        Test the get_timesheets_by_month_year method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwi1', 'test_password')
        test_data = {
            'username': 'testHiwi1',
            'month': 5,
            'year': 2024
        }
        response = self.client.get('/timesheet/getByMonthYear', query_string=test_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheets = response.json
        self.assertEqual(timesheets["username"], test_data["username"])
        self.assertEqual(timesheets["month"], test_data["month"])
        self.assertEqual(timesheets["year"], test_data["year"])

    def test_get_current_timesheet(self):
        """
        Test the get_current_timesheet method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwi1', 'test_password')
        response = self.client.get('/timesheet/getCurrentTimesheet', query_string={"username": "testHiwi1"}, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheet = response.json
        self.assertEqual("6679ca2935df0d8f7202c5fa", timesheet["_id"])

    def test_get_timesheets_by_username_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetController class.
        """
        access_token = self.authenticate('testSupervisor1', 'test_password')
        test_data = {
            "username": "testHiwi1",
            "status": "Complete"
        }
        response = self.client.get('/timesheet/getByUsernameStatus', query_string=test_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.json))
        self.assertEqual("Complete", response.json[0]["status"])
        self.assertEqual("Complete", response.json[1]["status"])



