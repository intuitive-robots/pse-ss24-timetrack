import unittest
import datetime

from app import app
from db import initialize_db
from model.timesheet_status import TimesheetStatus
from service.time_entry_service import TimeEntryService

from service.timesheet_service import TimesheetService
from service.user_service import UserService


class TestTimesheetController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = initialize_db()
        cls.client = app.test_client()
        cls.timesheet_service = TimesheetService()
        cls.user_service = UserService()
        cls.time_entry_service = TimeEntryService()

        cls.test_timesheet_supervisor = {'username': 'testSupervisorTimesheetController',
                                         'password': 'testPassword',
                                         'personalInfo': {
                                             'firstName': 'Test',
                                             'lastName': 'Supervisor',
                                             'email': 'test@gmail.com',
                                             'personalNumber': '1234567890',
                                             'instituteName': 'Test Institute'
                                         },
                                         'role': 'Supervisor',
                                         'accountCreation': datetime.datetime(2023, 6, 1, 8, 0, 0, 0),
                                         'lastLogin': datetime.datetime(2024, 6, 1, 8, 0, 0, 0),
                                         'slackId': 'testSlackId',
                                         'isArchived': False
                                         }
        cls.test_timesheet_hiwi = {'username': 'testHiwiTimesheetController',
                                   'password': 'testPassword',
                                   'personalInfo': {
                                       'firstName': 'Test',
                                       'lastName': 'Hiwi',
                                       'email': 'test@gmail.com',
                                       'personalNumber': '1234567890',
                                       'instituteName': 'Test Institute'
                                   },
                                   'role': 'Hiwi',
                                   'accountCreation': datetime.datetime(2023, 6, 1, 8, 0, 0, 0),
                                   'lastLogin': datetime.datetime(2024, 6, 1, 8, 0, 0, 0),
                                   'slackId': 'testSlackId',
                                   'isArchived': False,
                                   'supervisor': 'testSupervisorTimesheetController',
                                   'contractInfo': {'hourlyWage': 15,
                                                    'workingHours': 80,
                                                    'vacationMinutes': 0,
                                                    'overtimeMinutes': 0}
                                   }

        cls.test_june_3_time_entry_data = {'startTime': '2024-06-03T10:00:00Z',
                                           'endTime': '2024-06-03T20:00:00Z',
                                           'breakTime': 60,
                                           'activity': 'timesheetControllerActivitiy',
                                           'activityType': 'Projektbesprechung',
                                           'projectName': 'timesheetControllerTest'}
        cls.test_june_4_time_entry_data = {'startTime': '2024-06-04T10:00:00Z',
                                           'endTime': '2024-06-04T20:00:00Z',
                                           'breakTime': 60,
                                           'activity': 'timesheetControllerActivitiy',
                                           'activityType': 'Projektbesprechung',
                                           'projectName': 'timesheetControllerTest'}

    def setUp(self):
        self.user_service.create_user(self.test_timesheet_supervisor.copy())
        self.user_service.create_user(self.test_timesheet_hiwi.copy())
        self.timesheet_service.ensure_timesheet_exists('testHiwiTimesheetController', 6, 2024)
        self.time_entry_service.create_work_entry(self.test_june_3_time_entry_data.copy(), 'testHiwiTimesheetController')
        self.time_entry_service.create_work_entry(self.test_june_4_time_entry_data.copy(), 'testHiwiTimesheetController')

    def tearDown(self):
        timesheet_id = self.timesheet_service.get_timesheet_id('testHiwiTimesheetController', 6, 2024).data
        self.db.users.delete_many({'username': 'testHiwiTimesheetController'})
        self.db.users.delete_many({'username': 'testSupervisorTimesheetController'})
        self.db.timesheets.delete_many({'username': 'testHiwiTimesheetController'})
        self.db.timeEntries.delete_many({'timesheetId': str(timesheet_id)})
        self.db.notifications.delete_many({'receiver': 'testHiwiTimesheetController'})
        self.db.notifications.delete_many({'receiver': 'testSupervisorTimesheetController'})

        files_id = self.db.fs.files.find_one({'filename': 'testHiwiTimesheetController_Signature'})
        if files_id:
            files_id = files_id['_id']
        else:
            files_id = None
        self.db.file_metadata.delete_many({'username': 'testHiwiTimesheetController'})
        self.db.fs.files.delete_many({'filename': 'testHiwiTimesheetController_Signature'})
        self.db.fs.chunks.delete_many({'files_id': files_id})

        files_id2 = self.db.fs.files.find_one({'filename': 'testSupervisorTimesheetController_Signature'})
        if files_id2:
            files_id2 = files_id2['_id']
        else:
            files_id2 = None
        self.db.file_metadata.delete_many({'username': 'testSupervisorTimesheetController'})
        self.db.fs.files.delete_many({'filename': 'testSupervisorTimesheetController_Signature'})
        self.db.fs.chunks.delete_many({'files_id': files_id2})

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
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_non_existing_timesheet_data = {
            'username': 'testHiwiTimesheetController',
            'month': 7,
            'year': 2024
        }
        non_existing_response = self.client.post('/timesheet/ensureExists', json=test_non_existing_timesheet_data,
                                                 headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(201, non_existing_response.status_code)
        timesheet = self.timesheet_service.get_timesheet('testHiwiTimesheetController', 7, 2024).data
        self.assertIsNotNone(timesheet)

    def test_ensure_timesheet_exists_no_json(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetController class with no json format.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        # Test for no json format
        no_json_format_response = self.client.post('/timesheet/ensureExists',
                                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_format_response.status_code)
        self.assertEqual('Request must be in JSON format', no_json_format_response.json)

    def test_ensure_timesheet_exists_no_username(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetController class with no username.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_no_username_data = {
            'month': 5,
            'year': 2024
        }
        no_username_response = self.client.post('/timesheet/ensureExists', json=test_no_username_data,
                                                headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_username_response.status_code)
        self.assertEqual('No username provided', no_username_response.json)

    def test_ensure_timesheet_exists_no_month(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetController class with no month.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_no_month_data = {
            'username': 'testHiwiTimesheetController',
            'year': 2024
        }
        no_month_response = self.client.post('/timesheet/ensureExists', json=test_no_month_data,
                                             headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_month_response.status_code)
        self.assertEqual('No month provided', no_month_response.json)

    def test_ensure_timesheet_exists_no_year(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetController class with no year.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_no_year_data = {
            'username': 'testHiwi1',
            'month': 5,
        }
        no_year_response = self.client.post('/timesheet/ensureExists', json=test_no_year_data,
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_year_response.status_code)
        self.assertEqual('No year provided', no_year_response.json)

    def test_ensure_timesheet_exists_already_exists(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetController class with a timesheet that already exists.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_existing_timesheet_data = {
            'username': 'testHiwiTimesheetController',
            'month': 6,
            'year': 2024
        }
        existing_response = self.client.post('/timesheet/ensureExists', json=test_existing_timesheet_data,
                                             headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, existing_response.status_code)

    def test_sign_timesheet(self):
        """
        Test the sign_timesheet method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        file = open('../resources/testProfilePic.jpg', 'rb')
        self.client.post('/user/uploadFile?username=testHiwiTimesheetController&fileType=Signature',
                         data={'file': file},
                         headers={'Authorization': f'Bearer {access_token}'})
        file.close()
        self.db.timesheets.update_one({'username': 'testHiwiTimesheetController', 'month': 6, 'year': 2024},
                                      {'$set': {'totalTime': 4200}})
        timesheet_id = self.timesheet_service.get_timesheet_id('testHiwiTimesheetController', 6, 2024).data
        response = self.client.patch('/timesheet/sign', json={'_id': str(timesheet_id)},
                                     headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(200, response.status_code)
        timesheet = self.timesheet_service.get_timesheet('testHiwiTimesheetController', 6, 2024).data
        self.assertEqual(timesheet.status, TimesheetStatus.WAITING_FOR_APPROVAL)

    def test_sign_timesheet_no_json(self):
        """
        Test the sign_timesheet method of the TimesheetController class with no json format.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        no_json_response = self.client.patch('/timesheet/sign',
                                             headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_response.status_code)
        self.assertEqual('Request data must be in JSON format', no_json_response.json)

    def test_approve_timesheet(self):
        """
        Test the approve_timesheet method of the TimesheetController class.
        """
        access_token = self.authenticate('testSupervisorTimesheetController', 'testPassword')

        file = open('../resources/testProfilePic.jpg', 'rb')
        self.client.post('/user/uploadFile?username=testSupervisorTimesheetController&fileType=Signature',
                         data={'file': file},
                         headers={'Authorization': f'Bearer {access_token}'})
        file.close()

        test_timesheet_id = str(self.timesheet_service.get_timesheet_id('testHiwiTimesheetController', 6, 2024).data)
        self.db.timesheets.update_one({'username': 'testHiwiTimesheetController', 'month': 6, 'year': 2024},
                                      {'$set': {'status': 'Waiting for Approval'}})

        response = self.client.patch('/timesheet/approve', json={"_id": test_timesheet_id},
                                     headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheet = self.timesheet_service.get_timesheet_by_id(test_timesheet_id).data
        self.assertEqual(TimesheetStatus.COMPLETE, timesheet.status)

    def test_approve_timesheet_no_json(self):
        """
        Test the approve_timesheet method of the TimesheetController class with no json.
        """
        access_token = self.authenticate('testSupervisorTimesheetController', 'testPassword')

        response = self.client.patch('/timesheet/approve',
                                     headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data must be in JSON format', response.json)

    def test_request_change(self):
        """
        Test the request_change method of the TimesheetController class.
        """
        access_token = self.authenticate('testSupervisorTimesheetController', 'testPassword')

        file = open('../resources/testProfilePic.jpg', 'rb')
        self.client.post('/user/uploadFile?username=testSupervisorTimesheetController&fileType=Signature',
                         data={'file': file},
                         headers={'Authorization': f'Bearer {access_token}'})
        file.close()

        self.db.timesheets.update_one({'username': 'testHiwiTimesheetController', 'month': 6, 'year': 2024},
                                      {'$set': {'status': 'Waiting for Approval'}})
        test_timesheet_id = str(self.timesheet_service.get_timesheet_id('testHiwiTimesheetController', 6, 2024).data)

        response = self.client.patch('/timesheet/requestChange',
                                     json={'_id': test_timesheet_id, 'message': 'testMessage'},
                                     headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(200, response.status_code)
        timesheet = self.timesheet_service.get_timesheet_by_id(test_timesheet_id).data
        self.assertEqual(TimesheetStatus.REVISION, timesheet.status)

    def test_request_change_no_json(self):
        """
        Test the request_change method of the TimesheetController class with no json.
        """
        access_token = self.authenticate('testSupervisorTimesheetController', 'testPassword')

        response = self.client.patch('/timesheet/requestChange',
                                     headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data must be in JSON format', response.json)

    def test_get_timesheets(self):
        """
        Test the get_timesheets method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        response = self.client.get('/timesheet/get', query_string={'username': 'testHiwiTimesheetController'},
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(200, response.status_code)
        timesheets = response.json
        for timesheet in timesheets:
            self.assertEqual(timesheet['username'], 'testHiwiTimesheetController')

    def test_get_timesheets_no_username(self):
        """
        Test the get_timesheets method of the TimesheetController class with no username.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        no_username_response = self.client.get('/timesheet/get', query_string={},
                                               headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_username_response.status_code)
        self.assertEqual('No username provided', no_username_response.json)

    def test_get_timesheets_by_month_year(self):
        """
        Test the get_timesheets_by_month_year method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_data = {
            'username': 'testHiwiTimesheetController',
            'month': 6,
            'year': 2024
        }
        response = self.client.get('/timesheet/getByMonthYear', query_string=test_data,
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheet = response.json
        self.assertEqual(timesheet["username"], test_data["username"])
        self.assertEqual(timesheet["month"], test_data["month"])
        self.assertEqual(timesheet["year"], test_data["year"])

    def test_get_timesheets_by_month_year_no_username(self):
        """
        Test the get_timesheets_by_month_year method of the TimesheetController class with no username.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_no_username_data = {
            'month': 6,
            'year': 2024
        }
        no_username_response = self.client.get('/timesheet/getByMonthYear', query_string=test_no_username_data,
                                               headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_username_response.status_code)
        self.assertEqual('No username provided', no_username_response.json)

    def test_get_timesheets_by_month_year_no_month(self):
        """
        Test the get_timesheets_by_month_year method of the TimesheetController class with no month.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_no_month_data = {
            'username': 'testHiwiTimesheetController',
            'year': 2024
        }
        no_month_response = self.client.get('/timesheet/getByMonthYear', query_string=test_no_month_data,
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_month_response.status_code)
        self.assertEqual('No month provided', no_month_response.json)

    def test_get_timesheets_by_month_year_no_year(self):
        """
        Test the get_timesheets_by_month_year method of the TimesheetController class with no year.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        test_no_month_data = {
            'username': 'testHiwiTimesheetController',
            'month': 6
        }
        no_month_response = self.client.get('/timesheet/getByMonthYear', query_string=test_no_month_data,
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_month_response.status_code)
        self.assertEqual('No year provided', no_month_response.json)

    def test_get_current_timesheet(self):
        """
        Test the get_current_timesheet method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        response = self.client.get('/timesheet/getCurrentTimesheet', query_string={"username":
                                                                                       "testHiwiTimesheetController"},
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        timesheet = response.json
        timesheet_id = self.timesheet_service.get_timesheet_id('testHiwiTimesheetController', 6, 2024).data
        self.assertEqual(str(timesheet_id), timesheet["_id"])

    def test_get_current_timesheet_no_username(self):
        """
        Test the get_current_timesheet method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        no_username_response = self.client.get('/timesheet/getCurrentTimesheet', query_string={},
                                               headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_username_response.status_code)
        self.assertEqual('No username provided', no_username_response.json)

    def test_get_highest_priority_timesheet(self):
        """
        Test the get_highest_priority_timesheet method of the TimesheetController class.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        response = self.client.get('/timesheet/getHighestPriorityTimesheet', query_string={
            'username': 'testHiwiTimesheetController'},
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(200, response.status_code)
        timesheet = response.json
        timesheet_id = self.timesheet_service.get_timesheet_id('testHiwiTimesheetController', 6, 2024).data
        self.assertEqual(str(timesheet_id), timesheet['_id'])

    def test_get_highest_priority_timesheet_no_username(self):
        """
        Test the get_highest_priority_timesheet method of the TimesheetController class with no username.
        """
        access_token = self.authenticate('testHiwiTimesheetController', 'testPassword')

        no_username_response = self.client.get('/timesheet/getHighestPriorityTimesheet', query_string={},
                                               headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_username_response.status_code)
        self.assertEqual('No username provided', no_username_response.json)

    def test_get_timesheets_by_username_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetController class.
        """
        access_token = self.authenticate('testSupervisorTimesheetController', 'testPassword')
        test_data = {
            "username": "testHiwiTimesheetController",
            "status": "Not Submitted"
        }
        response = self.client.get('/timesheet/getByUsernameStatus', query_string=test_data,
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        for timesheet in response.json:
            self.assertEqual("Not Submitted", timesheet["status"])

    def test_get_timesheets_by_username_status_no_username(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetController class with no username.
        """
        access_token = self.authenticate('testSupervisorTimesheetController', 'testPassword')

        no_username_data = {
            'status': 'Not Submitted'
        }
        responseNoUsername = self.client.get('/timesheet/getByUsernameStatus', query_string=no_username_data,
                                             headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual('No username provided', responseNoUsername.json)
        self.assertEqual(responseNoUsername.status_code, 400)

    def test_get_timesheets_by_username_status_no_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetController class with no username.
        """
        access_token = self.authenticate('testSupervisorTimesheetController', 'testPassword')

        no_status_data = {
            'username': 'testHiwiTimesheetController',
        }
        responseNoStatus = self.client.get('/timesheet/getByUsernameStatus', query_string=no_status_data,
                                           headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual('No status provided', responseNoStatus.json)
        self.assertEqual(responseNoStatus.status_code, 400)

    def test_get_timesheets_by_username_status_no_timesheet(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetController class with no username.
        """
        access_token = self.authenticate('testSupervisorTimesheetController', 'testPassword')

        no_timesheets_data = {
            "username": "testHiwiTimesheetController",
            "status": "Complete"
        }
        responseNoStatus = self.client.get('/timesheet/getByUsernameStatus', query_string=no_timesheets_data,
                                           headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual("No timesheets found", responseNoStatus.json)
        self.assertEqual(responseNoStatus.status_code, 404)
