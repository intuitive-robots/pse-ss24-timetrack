import datetime
import unittest

from bson import ObjectId

from app import app
from db import initialize_db
from model.repository.timesheet_repository import TimesheetRepository
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus
from service.auth_service import AuthenticationService
from service.timesheet_service import TimesheetService


class TestTimesheetService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = initialize_db()
        cls.timesheet_service = TimesheetService()
        cls.timesheet_repository = TimesheetRepository.get_instance()
        cls.app = app
        cls.auth_service = AuthenticationService()

        cls.test_timesheet_supervisor = {'username': 'testSupervisorTimesheetService',
                                         'passwordHash': 'testPasswordHash',
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
                                         'isArchived': False,
                                         'supervisor': 'testSupervisorTimesheetService',
                                         'hiwis': ['testHiwiTimesheetService']
                                         }
        cls.test_timesheet_hiwi = {'username': 'testHiwiTimesheetService',
                                   'passwordHash': 'testPasswordHash',
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
                                   'supervisor': 'testSupervisorTimesheetService',
                                   'contractInfo': {'hourlyWage': 15,
                                                    'workingHours': 80,
                                                    'vacationMinutes': 0,
                                                    'overtimeMinutes': 0}
                                   }
        cls.db.users.insert_one(cls.test_timesheet_supervisor)
        cls.db.users.insert_one(cls.test_timesheet_hiwi)

    def setUp(self):
        self.test_april_timesheet_data = {'username': 'testHiwiTimesheetService',
                                          'month': 4,
                                          'year': 2024,
                                          'status': 'Complete',
                                          'totalTime': 0.0,
                                          'overtime': 0.0,
                                          'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                          'vacationMinutes': 0.0}

        self.test_may_timesheet_data = {'username': 'testHiwiTimesheetService',
                                        'month': 5,
                                        'year': 2024,
                                        'status': 'Waiting for Approval',
                                        'totalTime': 0.0,
                                        'overtime': 0.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                        'vacationMinutes': 0.0}

        self.test_june_timesheet_data = {'username': 'testHiwiTimesheetService',
                                         'month': 6,
                                         'year': 2024,
                                         'status': 'Not Submitted',
                                         'totalTime': 0.0,
                                         'overtime': 0.0,
                                         'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                         'vacationMinutes': 0.0}

        self.db.timesheets.insert_one(self.test_april_timesheet_data)
        self.db.timesheets.insert_one(self.test_may_timesheet_data)
        self.db.timesheets.insert_one(self.test_june_timesheet_data)

    def tearDown(self):
        self.db.timesheets.delete_many({'username': 'testHiwiTimesheetService'})
        self.db.users.delete_many({'username': 'testHiwiTimesheetService'})
        self.db.users.delete_many({'username': 'testSupervisorTimesheetService'})


    def test_ensure_timesheet_exists(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetService class.
        """
        result = self.timesheet_service.ensure_timesheet_exists(self.test_april_timesheet_data['username'],
                                                                7, 2024)
        print(result.message)
        self.assertTrue(result.is_successful)
        self.assertEqual(result.status_code, 201)
        self.assertIsNotNone(self.timesheet_repository.get_timesheet(self.test_april_timesheet_data['username'], 7, 2024))

    def test_ensure_timesheet_exists_already_exists(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetService class with a timesheet that already exists.
        """
        result = self.timesheet_service.ensure_timesheet_exists(self.test_april_timesheet_data['username'],
                                                                self.test_april_timesheet_data['month'],
                                                                self.test_april_timesheet_data['year'])
        self.assertTrue(result.is_successful)
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(self.timesheet_repository.get_timesheet(self.test_april_timesheet_data['username'],
                                                                     self.test_april_timesheet_data['month'],
                                                                     self.test_april_timesheet_data['year']))

    def test_set_total_time(self):
        # Test invalid timesheet id
        result_invalid_timesheet_id = self.timesheet_service.set_total_and_vacation_time("666666666666666666666666")
        self.assertEqual("Timesheet not found", result_invalid_timesheet_id.message)
        self.assertFalse(result_invalid_timesheet_id.is_successful)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)

        result = self.timesheet_service.set_total_and_vacation_time(ObjectId('6679ca2935df0d8f7202c5fa'))
        self.assertEqual("Total time updated", result.message)
        self.assertTrue(result.is_successful)
        self.assertEqual(200, result.status_code)

    def test_sign_timesheet(self):
        """
        Test the sign_timesheet method of the TimesheetService class.
        """
        # Test signing a timesheet
        with self.app.app_context():
            token = self.auth_service.create_token("testAdmin1", "Admin")
            with self.app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
                test_timesheet_id = "6679ca2935df0d8f7202c5fa"
                self.timesheet_service.sign_timesheet(test_timesheet_id)
                timesheet = self.timesheet_repository.get_timesheet_by_id(test_timesheet_id)
                self.assertEqual("Waiting for Approval", timesheet["status"])
                self.timesheet_repository.set_timesheet_status(test_timesheet_id, TimesheetStatus.NOT_SUBMITTED)
                # Test signing a timesheet that is already signed
                test_signed_timesheet_id = "667bd050cf0aa6181e9c8dd9"
                result = self.timesheet_service.sign_timesheet(test_signed_timesheet_id)
                self.assertFalse(result.is_successful)

    def test_approve_timesheet(self):
        """
        Test the approve_timesheet method of the TimesheetService class.
        """

        with self.app.app_context():
            token = self.auth_service.create_token("testAdmin1", "Admin")
            with self.app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
                # Test approving a timesheet
                test_timesheet_id = "667bd177cf0aa6181e9c8ddb"
                self.timesheet_service.approve_timesheet(test_timesheet_id)
                timesheet = self.timesheet_repository.get_timesheet_by_id(test_timesheet_id)
                self.assertEqual("Complete", timesheet["status"])
                self.timesheet_repository.set_timesheet_status(test_timesheet_id, TimesheetStatus.WAITING_FOR_APPROVAL)
                # Test approving a timesheet that hasn't been submitted
                test_unsigned_timesheet_id = "6679ca2935df0d8f7202c5fa"
                result = self.timesheet_service.approve_timesheet(test_unsigned_timesheet_id)
                self.assertFalse(result.is_successful)

    def test_request_change(self):
        """
        Test the request_timesheet method of the TimesheetService class.
        """
        with self.app.app_context():
            token = self.auth_service.create_token("testAdmin1", "Admin")
            with self.app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
                # Test requesting a timesheet
                test_timesheet_id = "667bd177cf0aa6181e9c8ddb"
                self.timesheet_service.request_change(test_timesheet_id)
                timesheet = self.timesheet_repository.get_timesheet_by_id(test_timesheet_id)
                self.assertEqual("Revision", timesheet["status"])
                self.timesheet_repository.set_timesheet_status(test_timesheet_id, TimesheetStatus.WAITING_FOR_APPROVAL)
                # Test requesting a timesheet that is already complete
                test_completed_timesheet_id = "667bd050cf0aa6181e9c8dd9"
                result = self.timesheet_service.request_change(test_completed_timesheet_id)
                self.assertFalse(result.is_successful)

    def test_calculate_overtime(self):
        # Test for invalid timesheet id
        result_invalid_timesheet_id = self.timesheet_service.calculate_overtime("666666666666666666666666")
        self.assertEqual("Timesheet not found", result_invalid_timesheet_id.message)
        self.assertFalse(result_invalid_timesheet_id.is_successful)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)

        result = self.timesheet_service.calculate_overtime(ObjectId('6679ca2935df0d8f7202c5fa'))
        self.assertEqual("", result.message)
        self.assertTrue(result.is_successful)
        self.assertEqual(-4366, result.data)
        self.assertEqual(200, result.status_code)
    def test_get_previous_overtime(self):
        result = self.timesheet_service.get_previous_overtime("testHiwi1", 5, 2024)
        self.assertEqual(0.0, result)

    def test_delete_timesheet_by_id(self):
        # Test for invalid timesheet id
        result_invalid_timesheet_id = self.timesheet_service.delete_timesheet_by_id("666666666666666666666666")
        self.assertEqual("Timesheet not found", result_invalid_timesheet_id.message)
        self.assertFalse(result_invalid_timesheet_id.is_successful)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)

    def test_get_timesheet_by_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetService class.
        """
        # Test getting a timesheet by ID
        test_timesheet_data = {"_id": ObjectId("6679ca2935df0d8f7202c5fa"),
                               "username": "testHiwi1",
                               "month": 5,
                               "year": 2024,
                               "status": "Not Submitted",
                               "totalTime": 0.0,
                               "overtime": 0.0,
                               "lastSignatureChange": datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}
        test_timesheet_id = str(test_timesheet_data["_id"])
        result = self.timesheet_service.get_timesheet_by_id(test_timesheet_id)
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(result.data.timesheet_id, test_timesheet_data["_id"])
        # Test getting a nonexistent timesheet by ID
        test_nonexistent_timesheet_id = "000000000000000000000000"
        result = self.timesheet_service.get_timesheet_by_id(test_nonexistent_timesheet_id)
        self.assertFalse(result.is_successful)

    def test_get_timesheets_by_username(self):
        """
        Test the get_timesheets_by_username method of the TimesheetService class.
        """
        # Test getting timesheets by username
        test_timesheet_data = [{'_id': ObjectId('66b089067cee7e4835986c86'),
                                'lastSignatureChange': datetime.datetime(2024, 8, 5, 10, 9, 10, 663000),
                                'month': 9,
                                'overtime': 0.0,
                                'status': 'Waiting for Approval',
                                'totalTime': 0.0,
                                'username': 'testHiwi1',
                                'year': 2024},
                               {'_id': ObjectId('66ad4b1436d802667b0970c7'),
                                'lastSignatureChange': datetime.datetime(2024, 8, 2, 23, 7, 58, 788000),
                                'month': 6,
                                'overtime': 0.0,
                                'status': 'Complete',
                                'totalTime': 0.0,
                                'username': 'testHiwi1',
                                'year': 2024},
                               {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                                'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                'month': 5,
                                'overtime': -4366.0,
                                'status': 'Not Submitted',
                                'totalTime': 434,
                                'username': 'testHiwi1',
                                'year': 2024}]
        result = self.timesheet_service.get_timesheets_by_username("testHiwi1")
        self.assertTrue(result.is_successful)
        result_timesheets = [timesheet.to_dict() for timesheet in result.data]
        self.assertEqual(test_timesheet_data, result_timesheets[:3])

    def test_get_timesheets_by_username_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetService class.
        """
        test_timesheet_data = [
            {"_id": ObjectId("667bd050cf0aa6181e9c8dd9"), "username": "testHiwi1", "month": 4, "year": 2024,
             "status": "Complete", "totalTime": 0.0, "overtime": 0.0,
             "lastSignatureChange": datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)},
            {"_id": ObjectId("667bd14ecf0aa6181e9c8dda"), "username": "testHiwi1", "month": 3, "year": 2024,
             "status": "Complete", "totalTime": 0.0, "overtime": 0.0,
             "lastSignatureChange": datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)}]

        # Test for invalid username
        result_invalid_username = self.timesheet_service.get_timesheets_by_username_status("", TimesheetStatus.COMPLETE)
        self.assertEqual("No timesheets found", result_invalid_username.message)
        self.assertFalse(result_invalid_username.is_successful)
        self.assertEqual(404, result_invalid_username.status_code)

        result = self.timesheet_service.get_timesheets_by_username_status("testHiwi1", TimesheetStatus.COMPLETE)
        self.assertTrue(result.is_successful)
        self.assertEqual(result.data[0].timesheet_id, test_timesheet_data[0]["_id"])
        self.assertEqual(result.data[1].timesheet_id, test_timesheet_data[1]["_id"])

    def test_get_timesheet_id(self):
        """
        Test the get_timesheet_id method of the TimesheetService class.        :return:
        """
        # Test existing timesheet
        test_timesheet_data = {"_id": ObjectId("667bd050cf0aa6181e9c8dd9"),
                               "username": "testHiwi1",
                               "month": 4,
                               "year": 2024,
                               "status": "Complete",
                               "totalTime": 0.0,
                               "overtime": 0.0,
                               "lastSignatureChange": datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)}
        result = self.timesheet_service.get_timesheet_id(test_timesheet_data["username"], test_timesheet_data["month"], test_timesheet_data["year"])
        self.assertEqual(test_timesheet_data["_id"], result.data)
        # Test nonexistent timesheet
        fail_result = self.timesheet_service.get_timesheet_id("testHiwiNonexistent", 5, 2024)
        self.assertFalse(fail_result.is_successful)

    def test_get_timesheet_status(self):
        # Test for invalid timesheet id
        result_invalid_timesheet_id = self.timesheet_service.get_timesheet_status("666666666666666666666666")
        self.assertEqual("Timesheet not found", result_invalid_timesheet_id.message)
        self.assertFalse(result_invalid_timesheet_id.is_successful)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)

        result = self.timesheet_service.get_timesheet_status(ObjectId("6679ca2935df0d8f7202c5fa"))
        self.assertEqual("", result.message)
        self.assertTrue(result.is_successful)
        self.assertEqual(200, result.status_code)
        self.assertEqual(TimesheetStatus(TimesheetStatus.NOT_SUBMITTED), result.data)

    def test_get_current_timesheet(self):
        """
        Test the get_current_timesheet method of the TimesheetService class.
        """
        # Test for no username
        result_no_username = self.timesheet_service.get_current_timesheet(None)
        self.assertEqual("Please provide a username to retrieve the timesheet", result_no_username.message)
        self.assertFalse(result_no_username.is_successful)
        self.assertEqual(400, result_no_username.status_code)



        # Test getting the current timesheet for a user
        test_username = "testHiwi1"
        test_timesheet_id = ObjectId("6679ca2935df0d8f7202c5fa")
        result = self.timesheet_service.get_current_timesheet(test_username)
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(result.data.timesheet_id, test_timesheet_id)
        # Test getting current timesheet of a user that has no unsubmitted timesheets
        test_fail_username = "testHiwi3"
        fail_result = self.timesheet_service.get_current_timesheet(test_fail_username)
        self.assertFalse(fail_result.is_successful)

    def test_get_highest_priority_timesheet(self):
        """
        Test the get_highest_priority_timesheet method of the TimesheetService class.
        """
        # Test for no username
        result_no_username = self.timesheet_service.get_highest_priority_timesheet(None)
        self.assertEqual("Please provide a username to retrieve the timesheet", result_no_username.message)
        self.assertFalse(result_no_username.is_successful)
        self.assertEqual(400, result_no_username.status_code)

        # Test getting the current timesheet for a user
        test_username = "testHiwi1"
        test_timesheet_id = ObjectId("6679ca2935df0d8f7202c5fa")
        result = self.timesheet_service.get_highest_priority_timesheet(test_username)
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(result.data.timesheet_id, test_timesheet_id)

    def test_get_timesheet(self):
        """
        Test the get_timesheet method of the TimesheetService class.
        """
        # Test for no username
        result_no_username = self.timesheet_service.get_timesheet(None, 5, 2024)
        self.assertEqual("Please provide a username, month, and year to retrieve the timesheet", result_no_username.message)
        self.assertFalse(result_no_username.is_successful)
        self.assertEqual(400, result_no_username.status_code)

        # Test getting a timesheet for a user
        test_username = "testHiwi1"
        test_month = 5
        test_year = 2024
        test_timesheet_id = ObjectId("6679ca2935df0d8f7202c5fa")
        result = self.timesheet_service.get_timesheet(test_username, test_month, test_year)
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(test_timesheet_id, result.data.timesheet_id)
        # Test getting a nonexistent timesheet for a user
        test_nonexistent_username = "testHiwiNonexistent"
        result = self.timesheet_service.get_timesheet(test_nonexistent_username, test_month, test_year)
        self.assertFalse(result.is_successful)

    if __name__ == '__main__':
        unittest.main()
