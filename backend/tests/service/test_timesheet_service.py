import datetime
import unittest

from app import app
from db import initialize_db
from model.repository.timesheet_repository import TimesheetRepository
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

    def setUp(self):
        self.test_timesheet_admin = {'username': 'testAdminTimesheetService',
                                    'passwordHash': 'testPasswordHash',
                                    'personalInfo': {
                                        'firstName': 'Test',
                                        'lastName': 'Admin',
                                        'email': 'test@gmail.com',
                                        'personalNumber': '1234567890',
                                        'instituteName': 'Test Institute'
                                    },
                                    'role': 'Admin',
                                    'accountCreation': datetime.datetime(2023, 6, 1, 8, 0, 0, 0),
                                    'lastLogin': datetime.datetime(2024, 6, 1, 8, 0, 0, 0),
                                    'slackId': 'testSlackId',
                                    'isArchived': False
                                    }
        self.test_timesheet_supervisor = {'username': 'testSupervisorTimesheetService',
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
                                         'hiwis': ['testHiwiTimesheetService']
                                         }
        self.test_timesheet_hiwi = {'username': 'testHiwiTimesheetService',
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
        self.test_timesheet_hiwi2 = {'username': 'testHiwi2TimesheetService',
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

        self.db.users.insert_one(self.test_timesheet_admin)
        self.db.users.insert_one(self.test_timesheet_supervisor)
        self.db.users.insert_one(self.test_timesheet_hiwi)
        self.db.users.insert_one(self.test_timesheet_hiwi2)
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
                                        'status': 'Complete',
                                        'totalTime': 0.0,
                                        'overtime': 0.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                        'vacationMinutes': 0.0}

        self.test_june_timesheet_data = {'username': 'testHiwiTimesheetService',
                                         'month': 6,
                                         'year': 2024,
                                         'status': 'Not Submitted',
                                         'totalTime': 1080.0,
                                         'overtime': 0.0,
                                         'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                         'vacationMinutes': 0.0}

        self.db.timesheets.insert_one(self.test_april_timesheet_data)
        self.db.timesheets.insert_one(self.test_may_timesheet_data)
        self.db.timesheets.insert_one(self.test_june_timesheet_data)

        self.test_april_1_time_entry_data = {'timesheetId': str(self.test_june_timesheet_data['_id']),
                                             'startTime': datetime.datetime(2024, 6, 1, 8, 0, 0, 0),
                                             'endTime': datetime.datetime(2024, 6, 1, 18, 0),
                                             'entryType': 'Work Entry',
                                             'breakTime': 60,
                                             'activity': 'timesheetServiceActivitiy',
                                             'activityType': 'Projektbesprechung',
                                             'projectName': 'timesheetServiceTest'}
        self.test_april_2_time_entry_data = {'timesheetId': str(self.test_june_timesheet_data['_id']),
                                             'startTime': datetime.datetime(2024, 6, 2, 8, 0, 0, 0),
                                             'endTime': datetime.datetime(2024, 6, 2, 18, 0),
                                             'entryType': 'Work Entry',
                                             'breakTime': 60,
                                             'activity': 'timesheetServiceActivitiy',
                                             'activityType': 'Projektbesprechung',
                                             'projectName': 'timesheetServiceTest'}
        self.db.timeEntries.insert_one(self.test_april_1_time_entry_data)
        self.db.timeEntries.insert_one(self.test_april_2_time_entry_data)

    def tearDown(self):
        self.db.timesheets.delete_many({'username': 'testHiwiTimesheetService'})
        self.db.timeEntries.delete_many({'timesheetId': str(self.test_june_timesheet_data['_id'])})
        self.db.users.delete_many({'username': 'testHiwiTimesheetService'})
        self.db.users.delete_many({'username': 'testHiwi2TimesheetService'})
        self.db.users.delete_many({'username': 'testSupervisorTimesheetService'})
        self.db.users.delete_many({'username': 'testAdminTimesheetService'})


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
        """
        Test the set_total_time method of the TimesheetService class.
        """
        result = self.timesheet_service.set_total_and_vacation_time(self.test_april_timesheet_data['_id'])
        self.assertEqual("Total time updated", result.message)
        self.assertTrue(result.is_successful)
        self.assertEqual(200, result.status_code)

    def test_set_total_time_invalid_id(self):
        """
        Test the set_total_time method of the TimesheetService class with an invalid timesheet ID.
        """
        result_invalid_timesheet_id = self.timesheet_service.set_total_and_vacation_time("666666666666666666666666")
        self.assertEqual("Timesheet not found", result_invalid_timesheet_id.message)
        self.assertFalse(result_invalid_timesheet_id.is_successful)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)

    def test_sign_timesheet(self):
        """
        Test the sign_timesheet method of the TimesheetService class.
        """
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimesheetService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                self.db.timesheets.update_one({'_id': self.test_june_timesheet_data['_id']}, {'$set': {'totalTime': 4200}})
                self.timesheet_service.sign_timesheet(str(self.test_june_timesheet_data['_id']))
                timesheet = self.timesheet_repository.get_timesheet_by_id(str(self.test_june_timesheet_data['_id']))
                self.assertEqual('Waiting for Approval', timesheet['status'])

    def test_sign_timesheet_already_signed(self):
        """
        Test the sign_timesheet method of the TimesheetService class for a timesheet that is already signed.
        """
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimesheetService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result = self.timesheet_service.sign_timesheet(str(self.test_april_timesheet_data['_id']))
                self.assertFalse(result.is_successful)

    def test_approve_timesheet(self):
        """
        Test the approve_timesheet method of the TimesheetService class.
        """
        with self.app.app_context():
            token = self.auth_service.create_token('testSupervisorTimesheetService', 'Supervisor')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                self.db.timesheets.update_one({'_id': self.test_june_timesheet_data['_id']}, {'$set': {'status': 'Waiting for Approval'}})
                self.timesheet_service.approve_timesheet(str(self.test_june_timesheet_data['_id']))
                timesheet = self.db.timesheets.find_one({'_id': self.test_june_timesheet_data['_id']})
                self.assertEqual('Complete', timesheet['status'])
                
    def test_approve_timesheet_not_submitted(self):
        """
        Test the approve_timesheet method of the TimesheetService class with a timesheet that hasn't been submitted.
        """

        with self.app.app_context():
            token = self.auth_service.create_token('testSupervisorTimesheetService', 'Supervisor')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result = self.timesheet_service.approve_timesheet(str(self.test_june_timesheet_data['_id']))
                self.assertFalse(result.is_successful)

    def test_request_change(self):
        """
        Test the request_timesheet method of the TimesheetService class.
        """
        with self.app.app_context():
            token = self.auth_service.create_token('testSupervisorTimesheetService', 'Supervisor')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                self.db.timesheets.update_one({'_id': self.test_june_timesheet_data['_id']}, {'$set': {'status': 'Waiting for Approval'}})
                self.timesheet_service.request_change(self.test_june_timesheet_data['_id'], "Test reason")
                timesheet = self.timesheet_repository.get_timesheet_by_id(str(self.test_june_timesheet_data['_id']))
                self.assertEqual('Revision', timesheet['status'])

    def test_request_change_complete_timesheet(self):
        """
        Test the request_timesheet method of the TimesheetService class with a complete timesheet.
        """
        with self.app.app_context():
            token = self.auth_service.create_token('testSupervisorTimesheetService', 'Supervisor')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result = self.timesheet_service.request_change(str(self.test_may_timesheet_data['_id']), "")
                self.assertFalse(result.is_successful)

    def test_calculate_overtime(self):
        """
        Test the calculate_overtime method of the TimesheetService class.
        """
        result = self.timesheet_service.calculate_overtime(str(self.test_june_timesheet_data['_id']))
        print(result.message)
        self.assertEqual("", result.message)
        self.assertTrue(result.is_successful)
        self.assertEqual(-3720.0, result.data)
        self.assertEqual(200, result.status_code)

    def test_calculate_overtime_invalid_id(self):
        """
        Test the calculate_overtime method of the TimesheetService class with an invalid timesheet ID.
        """
        result_invalid_timesheet_id = self.timesheet_service.calculate_overtime("666666666666666666666666")
        self.assertEqual("Timesheet not found", result_invalid_timesheet_id.message)
        self.assertFalse(result_invalid_timesheet_id.is_successful)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)

    def test_get_previous_overtime(self):
        result = self.timesheet_service.get_previous_overtime("testHiwiTimesheetService", 6, 2024)
        self.assertEqual(0.0, result)

    def test_delete_timesheet_by_id_invalid_id(self):
        result_invalid_timesheet_id = self.timesheet_service.delete_timesheet_by_id("666666666666666666666666")
        self.assertEqual("Timesheet not found", result_invalid_timesheet_id.message)
        self.assertFalse(result_invalid_timesheet_id.is_successful)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)

    def test_get_timesheet_by_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetService class.
        """
        result = self.timesheet_service.get_timesheet_by_id(str(self.test_june_timesheet_data['_id']))
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.db.timesheets.find_one({'_id': self.test_june_timesheet_data['_id']})

    def test_get_timesheet_by_id_invalid_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetService class.
        """
        result = self.timesheet_service.get_timesheet_by_id('666666666666666666666666')
        self.assertFalse(result.is_successful)

    def test_get_timesheets_by_username(self):
        """
        Test the get_timesheets_by_username method of the TimesheetService class.
        """
        result = self.timesheet_service.get_timesheets_by_username("testHiwiTimesheetService")
        self.assertTrue(result.is_successful)
        result_timesheets = [timesheet.to_dict() for timesheet in result.data]
        for timesheet in result_timesheets:
            self.assertIn(timesheet, [self.test_april_timesheet_data, self.test_may_timesheet_data, self.test_june_timesheet_data])

    def test_get_timesheets_by_username_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetService class.
        """
        result = self.timesheet_service.get_timesheets_by_username_status("testHiwiTimesheetService", TimesheetStatus.COMPLETE)
        self.assertTrue(result.is_successful)
        for timesheet in result.data:
            self.assertIn(timesheet.to_dict(), [self.test_april_timesheet_data, self.test_may_timesheet_data])

    def test_get_timesheets_by_username_status_invalid_username(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetService class with an invalid username.
        """
        result_invalid_username = self.timesheet_service.get_timesheets_by_username_status("", TimesheetStatus.COMPLETE)
        self.assertEqual("No timesheets found", result_invalid_username.message)
        self.assertFalse(result_invalid_username.is_successful)
        self.assertEqual(404, result_invalid_username.status_code)

    def test_get_timesheet_id(self):
        """
        Test the get_timesheet_id method of the TimesheetService class.
        """
        result = self.timesheet_service.get_timesheet_id(self.test_june_timesheet_data['username'],
                                                         self.test_june_timesheet_data['month'],
                                                         self.test_june_timesheet_data['year'])
        self.assertEqual(self.test_june_timesheet_data['_id'], result.data)

    def test_get_timesheet_id_invalid_timesheet(self):
        """
        Test the get_timesheet_id method of the TimesheetService class with an invalid timesheet.
        """
        fail_result = self.timesheet_service.get_timesheet_id("testHiwiNonexistent", 5, 2024)
        self.assertFalse(fail_result.is_successful)

    def test_get_timesheet_status(self):
        """
        Test the get_timesheet_status method of the TimesheetService class.
        """
        result = self.timesheet_service.get_timesheet_status(str(self.test_june_timesheet_data['_id']))
        self.assertEqual("", result.message)
        self.assertTrue(result.is_successful)
        self.assertEqual(200, result.status_code)
        self.assertEqual(TimesheetStatus(TimesheetStatus.NOT_SUBMITTED), result.data)

    def test_get_timesheet_status_invalid_id(self):
        """
        Test the get_timesheet_status method of the TimesheetService class with an invalid timesheet ID.
        """
        result_invalid_timesheet_id = self.timesheet_service.get_timesheet_status("666666666666666666666666")
        self.assertEqual("Timesheet not found", result_invalid_timesheet_id.message)
        self.assertFalse(result_invalid_timesheet_id.is_successful)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)

    def test_get_current_timesheet(self):
        """
        Test the get_current_timesheet method of the TimesheetService class.
        """
        result = self.timesheet_service.get_current_timesheet(self.test_june_timesheet_data['username'])
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(self.test_june_timesheet_data['_id'], result.data.timesheet_id)

    def test_get_current_timesheet_no_username(self):
        """
        Test the get_current_timesheet method of the TimesheetService class with no username.
        """
        result_no_username = self.timesheet_service.get_current_timesheet(None)
        self.assertEqual("Please provide a username to retrieve the timesheet", result_no_username.message)
        self.assertFalse(result_no_username.is_successful)
        self.assertEqual(400, result_no_username.status_code)

    def test_get_current_timesheet_no_timesheets(self):
        """
        Test the get_current_timesheet method of the TimesheetService class for a user with no timesheets.
        """
        fail_result = self.timesheet_service.get_current_timesheet("testHiwi2TimesheetService")
        self.assertFalse(fail_result.is_successful)

    def test_get_highest_priority_timesheet(self):
        """
        Test the get_highest_priority_timesheet method of the TimesheetService class.
        """
        result = self.timesheet_service.get_highest_priority_timesheet(self.test_june_timesheet_data['username'])
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(self.test_june_timesheet_data['_id'], result.data.timesheet_id)

    def test_get_highest_priority_timesheet_no_username(self):
        """
        Test the get_highest_priority_timesheet method of the TimesheetService class with no username.
        """
        result_no_username = self.timesheet_service.get_highest_priority_timesheet(None)
        self.assertEqual("Please provide a username to retrieve the timesheet", result_no_username.message)
        self.assertFalse(result_no_username.is_successful)
        self.assertEqual(400, result_no_username.status_code)

    def test_get_timesheet(self):
        """
        Test the get_timesheet method of the TimesheetService class.
        """
        result = self.timesheet_service.get_timesheet(self.test_june_timesheet_data['username'],
                                                      self.test_june_timesheet_data['month'],
                                                      self.test_june_timesheet_data['year'])
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(self.test_june_timesheet_data['_id'], result.data.timesheet_id)

    def test_get_timesheet_no_username(self):
        """
        Test the get_timesheet method of the TimesheetService class with no username.
        """
        result_no_username = self.timesheet_service.get_timesheet(None, 5, 2024)
        self.assertEqual("Please provide a username, month, and year to retrieve the timesheet", result_no_username.message)
        self.assertFalse(result_no_username.is_successful)
        self.assertEqual(400, result_no_username.status_code)

    def test_get_timesheet_nonexistent_username(self):
        """
        Test the get_timesheet method of the TimesheetService class with a nonexistent username.
        """
        test_nonexistent_username = "testHiwiNonexistent"
        result = self.timesheet_service.get_timesheet(test_nonexistent_username, 5, 2024)
        self.assertFalse(result.is_successful)

    if __name__ == '__main__':
        unittest.main()
