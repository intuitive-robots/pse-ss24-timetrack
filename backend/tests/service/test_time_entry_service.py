import datetime
import unittest

from app import app
from db import initialize_db
from service.auth_service import AuthenticationService
from model.repository.time_entry_repository import TimeEntryRepository
from service.time_entry_service import TimeEntryService


class TestTimeEntryService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = initialize_db()
        cls.app = app
        cls.client = app.test_client()
        cls.time_entry_service = TimeEntryService()
        cls.time_entry_repository = TimeEntryRepository.get_instance()
        cls.auth_service = AuthenticationService()

    def setUp(self):
        self.test_timesheet_supervisor = {'username': 'testSupervisorTimeEntryService',
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
        self.test_timesheet_hiwi = {'username': 'testHiwiTimeEntryService',
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
                                    'supervisor': 'testSupervisorTimeEntryService',
                                    'contractInfo': {'hourlyWage': 15,
                                                     'workingHours': 80,
                                                     'vacationMinutes': 0,
                                                     'overtimeMinutes': 0}
                                    }
        self.test_timesheet_hiwi2 = {'username': 'testHiwi2TimeEntryService',
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
                                     'supervisor': 'testSupervisorTimeEntryService',
                                     'contractInfo': {'hourlyWage': 15,
                                                      'workingHours': 80,
                                                      'vacationMinutes': 0,
                                                      'overtimeMinutes': 0}
                                     }

        self.db.users.insert_one(self.test_timesheet_supervisor)
        self.db.users.insert_one(self.test_timesheet_hiwi)
        self.db.users.insert_one(self.test_timesheet_hiwi2)
        self.test_april_timesheet_data = {'username': 'testHiwiTimeEntryService',
                                          'month': 4,
                                          'year': 2024,
                                          'status': 'Complete',
                                          'totalTime': 0.0,
                                          'overtime': 0.0,
                                          'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                          'vacationMinutes': 0.0}

        self.test_may_timesheet_data = {'username': 'testHiwiTimeEntryService',
                                        'month': 5,
                                        'year': 2024,
                                        'status': 'Complete',
                                        'totalTime': 0.0,
                                        'overtime': 0.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                        'vacationMinutes': 0.0}

        self.test_june_timesheet_data = {'username': 'testHiwiTimeEntryService',
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

        self.test_june_1_time_entry_data = {'timesheetId': str(self.test_june_timesheet_data['_id']),
                                             'startTime': datetime.datetime(2024, 6, 1, 8, 0, 0, 0),
                                             'endTime': datetime.datetime(2024, 6, 1, 18, 0),
                                             'entryType': 'Work Entry',
                                             'breakTime': 60,
                                             'activity': 'timeEntryServiceActivitiy',
                                             'activityType': 'Projektbesprechung',
                                             'projectName': 'timeEntryServiceTest'}
        self.test_june_2_time_entry_data = {'timesheetId': str(self.test_june_timesheet_data['_id']),
                                             'startTime': datetime.datetime(2024, 6, 2, 8, 0, 0, 0),
                                             'endTime': datetime.datetime(2024, 6, 2, 18, 0),
                                             'entryType': 'Work Entry',
                                             'breakTime': 60,
                                             'activity': 'timeEntryServiceActivitiy',
                                             'activityType': 'Projektbesprechung',
                                             'projectName': 'timeEntryServiceTest'}
        self.test_june_vacation_entry_data = {'timesheetId': str(self.test_june_timesheet_data['_id']),
                                               'startTime': datetime.datetime(2024, 6, 5, 8, 0, 0, 0),
                                               'endTime': datetime.datetime(2024, 6, 5, 18, 0),
                                               'entryType': 'Vacation Entry'}
        self.db.timeEntries.insert_one(self.test_june_1_time_entry_data)
        self.db.timeEntries.insert_one(self.test_june_2_time_entry_data)
        self.db.timeEntries.insert_one(self.test_june_vacation_entry_data)

    def tearDown(self):
        self.db.timesheets.delete_many({'username': 'testHiwiTimeEntryService'})
        self.db.timeEntries.delete_many({'timesheetId': str(self.test_june_timesheet_data['_id'])})
        self.db.users.delete_many({'username': 'testHiwiTimeEntryService'})
        self.db.users.delete_many({'username': 'testHiwi2TimeEntryService'})
        self.db.users.delete_many({'username': 'testSupervisorTimeEntryService'})

    def test_create_work_entry(self):
        """
        Test the add_time_entry method of the TimeEntryService class.
        """
        test_time_entry_data = self.test_june_1_time_entry_data.copy()
        test_time_entry_data['startTime'] = datetime.datetime(2024, 6, 3, 8, 0, 0, 0)
        test_time_entry_data['endTime'] = datetime.datetime(2024, 6, 3, 18, 0, 0, 0)
        test_time_entry_data.pop('_id')
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result = self.time_entry_service.create_work_entry(test_time_entry_data, 'testHiwiTimeEntryService')
                self.assertTrue(result.is_successful)
                creation_result = self.time_entry_repository.get_time_entry_by_id(result.data['_id'])
                creation_result.pop('_id')
                self.assertEqual(test_time_entry_data, creation_result)

    def test_create_vacation_entry(self):
        """
        Test the add_time_entry method of the TimeEntryService class.
        """
        test_time_entry_data = self.test_june_1_time_entry_data.copy()
        test_time_entry_data['startTime'] = datetime.datetime(2024, 6, 3, 8, 0, 0, 0)
        test_time_entry_data['endTime'] = datetime.datetime(2024, 6, 3, 18, 0, 0, 0)
        test_time_entry_data.pop('_id')
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result = self.time_entry_service.create_work_entry(test_time_entry_data, 'testHiwiTimeEntryService')
                print(result.message)
                self.assertTrue(result.is_successful)
                creation_result = self.time_entry_repository.get_time_entry_by_id(result.data['_id'])
                creation_result.pop('_id')
                self.assertEqual(test_time_entry_data, creation_result)

    def test_update_time_entry(self):
        """
        Test the update_time_entry method of the TimeEntryService class.
        """
        test_modified_time_entry_data = self.test_june_1_time_entry_data.copy()
        test_modified_time_entry_data['startTime'] = datetime.datetime(2024, 6, 3, 8, 0, 0, 0)
        test_modified_time_entry_data['endTime'] = datetime.datetime(2024, 6, 3, 18, 0, 0, 0)
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result = self.time_entry_service.update_time_entry(str(self.test_june_1_time_entry_data['_id']),
                                                                   test_modified_time_entry_data)
                self.assertEqual(test_modified_time_entry_data,
                                 self.time_entry_repository.get_time_entry_by_id(str(test_modified_time_entry_data['_id'])))
                self.assertTrue(result.is_successful)

    def test_update_time_entry_invalid_id(self):
        """
        Test the update_time_entry method of the TimeEntryService class with an invalid id.
        """
        test_modified_time_entry_data = self.test_june_1_time_entry_data.copy()
        test_modified_time_entry_data['startTime'] = datetime.datetime(2024, 6, 3, 8, 0, 0, 0)
        test_modified_time_entry_data['endTime'] = datetime.datetime(2024, 6, 3, 18, 0, 0, 0)
        test_modified_time_entry_data.pop('_id')
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result_invalid_entry_id = self.time_entry_service.update_time_entry("666666666666666666666666",
                                                                                    test_modified_time_entry_data)
                self.assertFalse(result_invalid_entry_id.is_successful)
                self.assertEqual(404, result_invalid_entry_id.status_code)
                self.assertEqual("Time entry not found", result_invalid_entry_id.message)

    def test_update_time_entry_invalid_status(self):
        """
        Test the update_time_entry method of the TimeEntryService class with an invalid status.
        """
        self.db.timesheets.update_one({'_id': self.test_june_timesheet_data['_id']}, {'$set': {'status': 'Complete'}})
        test_modified_time_entry_data = self.test_june_1_time_entry_data.copy()
        test_modified_time_entry_data['startTime'] = datetime.datetime(2024, 6, 3, 8, 0, 0, 0)
        test_modified_time_entry_data['endTime'] = datetime.datetime(2024, 6, 3, 18, 0, 0, 0)
        test_modified_time_entry_data.pop('_id')
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result_invalid_timesheet_status = self.time_entry_service.update_time_entry(
                    str(self.test_june_1_time_entry_data['_id']),
                    test_modified_time_entry_data)
                self.assertFalse(result_invalid_timesheet_status.is_successful)
                self.assertEqual("Cannot update time entry of a submitted timesheet",
                                 result_invalid_timesheet_status.message)
                self.assertEqual(400, result_invalid_timesheet_status.status_code)

    def test_update_time_entry_invalid_type(self):
        """
        Test the update_time_entry method of the TimeEntryService class with an invalid type.
        """
        test_modified_time_entry_data = self.test_june_1_time_entry_data.copy()
        test_modified_time_entry_data['startTime'] = datetime.datetime(2024, 6, 3, 8, 0, 0, 0)
        test_modified_time_entry_data['endTime'] = datetime.datetime(2024, 6, 3, 18, 0, 0, 0)
        test_modified_time_entry_data['entryType'] = 'Test Entry'
        test_modified_time_entry_data.pop('_id')
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result_invalid_timesheet_status = self.time_entry_service.update_time_entry(
                    str(self.test_june_1_time_entry_data['_id']),
                    test_modified_time_entry_data)
                self.assertFalse(result_invalid_timesheet_status.is_successful)
                self.assertEqual("Invalid or unspecified entry type.",
                                 result_invalid_timesheet_status.message)
                self.assertEqual(400, result_invalid_timesheet_status.status_code)

    def test_update_time_entry_invalid_month(self):
        """
        Test the update_time_entry method of the TimeEntryService class with an invalid month.
        """
        test_modified_time_entry_data = self.test_june_1_time_entry_data.copy()
        test_modified_time_entry_data['startTime'] = datetime.datetime(2024, 5, 3, 8, 0, 0, 0)
        test_modified_time_entry_data['endTime'] = datetime.datetime(2024, 5, 3, 18, 0, 0, 0)
        test_modified_time_entry_data.pop('_id')
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result_invalid_month = self.time_entry_service.update_time_entry(
                    str(self.test_june_1_time_entry_data['_id']),
                    test_modified_time_entry_data)
                self.assertFalse(result_invalid_month.is_successful)
                self.assertEqual("Cannot update time entry to a different month or year",
                                 result_invalid_month.message)
                self.assertEqual(400, result_invalid_month.status_code)

    def test_update_time_entry_additional_field(self):
        """
        Test the update_time_entry method of the TimeEntryService class with an additional field.
        """
        test_modified_time_entry_data = self.test_june_1_time_entry_data.copy()
        test_modified_time_entry_data['startTime'] = datetime.datetime(2024, 6, 3, 8, 0, 0, 0)
        test_modified_time_entry_data['endTime'] = datetime.datetime(2024, 6, 3, 18, 0, 0, 0)
        test_modified_time_entry_data['additionalField'] = 'additional value'
        test_modified_time_entry_data.pop('_id')
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                result_additional_field = self.time_entry_service.update_time_entry(
                    str(self.test_june_1_time_entry_data['_id']),
                    test_modified_time_entry_data)
                print(result_additional_field.message)
                self.assertTrue(result_additional_field.is_successful)
                self.assertEqual("entry updated with warnings ´Skipped fields: additionalField´",
                                 result_additional_field.message)
                self.assertEqual(200, result_additional_field.status_code)

    def test_delete_time_entry(self):
        """
        Test the delete_time_entry method of the TimeEntryService class.
        """
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                delete_result = self.time_entry_service.delete_time_entry(str(self.test_june_1_time_entry_data['_id']))
                self.assertTrue(delete_result.is_successful)
                self.assertIsNone(self.time_entry_repository.get_time_entry_by_id(str(self.test_june_1_time_entry_data['_id'])))

    def test_delete_time_entry_no_id(self):
        """
        Test the delete_time_entry method of the TimeEntryService class with no id.
        """
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                delete_result_no_entry_id = self.time_entry_service.delete_time_entry("")
                self.assertEqual("Entry ID is None", delete_result_no_entry_id.message)
                self.assertEqual(400, delete_result_no_entry_id.status_code)
                self.assertFalse(delete_result_no_entry_id.is_successful)

    def test_delete_time_entry_invalid_id(self):
        """
        Test the delete_time_entry method of the TimeEntryService class with an invalid id.
        """
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):
                delete_result_invalid_entry_id = self.time_entry_service.delete_time_entry("666666666666666666666666")
                self.assertEqual("Time entry not found", delete_result_invalid_entry_id.message)
                self.assertEqual(404, delete_result_invalid_entry_id.status_code)
                self.assertFalse(delete_result_invalid_entry_id.is_successful)

    def test_delete_time_entry_invalid_status(self):
        """
        Test the delete_time_entry method of the TimeEntryService class with an invalid status.
        """
        self.db.timesheets.update_one({'_id': self.test_june_timesheet_data['_id']}, {'$set': {'status': 'Complete'}})
        with self.app.app_context():
            token = self.auth_service.create_token('testHiwiTimeEntryService', 'Hiwi')
            with self.app.test_request_context(headers={'Authorization': f'Bearer {token}'}):

                delete_result_invalid_timesheet_status = self.time_entry_service.delete_time_entry(
                    str(self.test_june_1_time_entry_data['_id']))
                self.assertEqual("Cannot delete time entry of a submitted timesheet",
                                 delete_result_invalid_timesheet_status.message)
                self.assertEqual(400, delete_result_invalid_timesheet_status.status_code)
                self.assertFalse(delete_result_invalid_timesheet_status.is_successful)

    def test_get_entries_of_timesheet(self):
        """
        Test the get_entries_of_timesheet method of the TimeEntryService class.
        """

        result = self.time_entry_service.get_entries_of_timesheet(str(self.test_june_timesheet_data['_id']))
        self.assertTrue(result.is_successful)
        for entry in result.data:
            self.assertIn(entry.to_dict(), [self.test_june_1_time_entry_data, self.test_june_2_time_entry_data,
                                            self.test_june_vacation_entry_data])

    def test_get_entries_of_timesheet_invalid_id(self):
        """
        Test the get_entries_of_timesheet method of the TimeEntryService class with an invalid id.
        """
        result_invalid_timesheet_id = self.time_entry_service.get_entries_of_timesheet("")
        self.assertEqual("No entries found", result_invalid_timesheet_id.message)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)
        self.assertFalse(result_invalid_timesheet_id.is_successful)

    if __name__ == '__main__':
        unittest.main()
