import datetime
import unittest
from unittest.mock import patch

from bson import ObjectId

from app import app
from model.repository.time_entry_repository import TimeEntryRepository
from service.time_entry_service import TimeEntryService


class TestTimeEntryService(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.time_entry_service = TimeEntryService()
        self.time_entry_repository = TimeEntryRepository.get_instance()

    def authenticate(self, username, password):
        """
        Authenticate the user.
        """
        user = {
            "username": username,
            "password": password
        }
        response = self.client.post('/user/login', json=user)
        return response.json['accessToken']


    # @patch('service.time_entry_service.TimeEntryService.get_jwt_identity', 'testHiwi1')
    # @patch('flask_jwt_extended.view_decorators.verify_jwt_in_request')
    def test_create_work_entry(self):
        """
        Test the add_time_entry method of the TimeEntryService class.
        """
        # Test creating entry for existing timesheet
        test_time_entry_data = {'timesheetId': '6679ca2935df0d8f7202c5fa',
                                'startTime': '2024-05-22T09:20:30.656Z',
                                'endTime': '2024-05-22T12:00:00Z',
                                'entryType': 'Work Entry',
                                'breakTime': 30,
                                'activity': 'testAddTimeEntry of Hiwi1',
                                'projectName': 'timeeEntryServiceTesting'}
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                result = self.time_entry_service.create_work_entry(test_time_entry_data, 'testHiwi1')
                self.assertTrue(result.is_successful)
                creation_result = self.time_entry_repository.get_time_entry_by_id(result.data['_id'])
                creation_result.pop('_id')
                self.assertEqual(test_time_entry_data, creation_result)
                # Reset database to original state
                delete_result = self.time_entry_service.delete_time_entry(result.data["_id"])
                self.assertTrue(delete_result.is_successful)

    def test_create_vacation_entry(self):
        """
        Test the add_time_entry method of the TimeEntryService class.
        """
        # Test creating entry for existing timesheet
        test_time_entry_data = {'timesheetId': '6679ca2935df0d8f7202c5fa',
                                'startTime': '2024-05-22T09:20:30.656Z',
                                'endTime': '2024-05-22T12:00:00Z',
                                'entryType': 'Vacation Entry'}
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                result = self.time_entry_service.create_vacation_entry(test_time_entry_data, 'testHiwi1')
                self.assertTrue(result.is_successful)
                creation_result = self.time_entry_repository.get_time_entry_by_id(result.data['_id'])
                creation_result.pop('_id')
                self.assertEqual(test_time_entry_data, creation_result)
                # Reset database to original state
                delete_result = self.time_entry_service.delete_time_entry(result.data["_id"])
                self.assertTrue(delete_result.is_successful)

    def test_update_time_entry(self):
        """
        Test the update_time_entry method of the TimeEntryService class.
        """
        # Test updating an existing time entry
        test_original_time_entry_data = {'_id': ObjectId('666c020f7a409003113fedf9'),
                                         'timesheetId': '6679ca2935df0d8f7202c5fa',
                                         'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                         'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                         'entryType': 'Work Entry',
                                         'breakTime': 22,
                                         'activity': 'timeEntry1 of Hiwi1',
                                         'projectName': 'testing'}

        test_modified_time_entry_data = {'_id': ObjectId('666c020f7a409003113fedf9'),
                                         'timesheetId': '6679ca2935df0d8f7202c5fa',
                                         'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                         'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                         'entryType': 'Work Entry',
                                         'breakTime': 22,
                                         'activity': 'testUpdateTimeEntry of Hiwi1',
                                         'projectName': 'timeEntryServiceTesting'}

        test_invalid_entry_type_data = {'_id': ObjectId('666c020f7a409003113fedf9'),
                                         'timesheetId': '6679ca2935df0d8f7202c5fa',
                                         'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                         'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                         'entryType': 'Entry',
                                         'breakTime': 22,
                                         'activity': 'testUpdateTimeEntry of Hiwi1',
                                         'projectName': 'timeEntryServiceTesting'}

        test_invalid_month_data = {'_id': ObjectId('666c020f7a409003113fedf9'),
                                        'timesheetId': '6679ca2935df0d8f7202c5fa',
                                        'startTime': datetime.datetime(2024, 6, 1, 8, 20, 30, 656000),
                                        'endTime': datetime.datetime(2024, 6, 1, 10, 0),
                                        'entryType': 'Work Entry',
                                        'breakTime': 22,
                                        'activity': 'testUpdateTimeEntry of Hiwi1',
                                        'projectName': 'timeEntryServiceTesting'}

        test_additional_field_data = {'_id': ObjectId('666c020f7a409003113fedf9'),
                                   'timesheetId': '6679ca2935df0d8f7202c5fa',
                                   'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                   'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                   'entryType': 'Work Entry',
                                    'additionalField': 'additional value',
                                   'breakTime': 22,
                                   'activity': 'testUpdateTimeEntry of Hiwi1',
                                   'projectName': 'timeEntryServiceTesting'}

        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                # Test for invalid entry id
                result_invalid_entry_id = self.time_entry_service.update_time_entry("666666666666666666666666", test_modified_time_entry_data)
                self.assertFalse(result_invalid_entry_id.is_successful)
                self.assertEqual(404, result_invalid_entry_id.status_code)
                self.assertEqual("Time entry not found", result_invalid_entry_id.message)

                # Test for invalid timesheet status
                result_invalid_timesheet_status = self.time_entry_service.update_time_entry(ObjectId('667bd41ed3c08a396da0598c'),
                                                                                    test_modified_time_entry_data)
                self.assertFalse(result_invalid_timesheet_status.is_successful)
                self.assertEqual("Cannot update time entry of a submitted timesheet", result_invalid_timesheet_status.message)
                self.assertEqual(400, result_invalid_timesheet_status.status_code)

                # Test for invalid entry type
                result_invalid_timesheet_status = self.time_entry_service.update_time_entry(str(test_invalid_entry_type_data['_id']),
                                                                                            test_invalid_entry_type_data)
                self.assertFalse(result_invalid_timesheet_status.is_successful)
                self.assertEqual("Invalid or unspecified entry type.",
                                 result_invalid_timesheet_status.message)
                self.assertEqual(400, result_invalid_timesheet_status.status_code)

                # Test for invalid month
                result_invalid_month = self.time_entry_service.update_time_entry(
                    str(test_invalid_month_data['_id']),
                    test_invalid_month_data)
                self.assertFalse(result_invalid_month.is_successful)
                self.assertEqual("Cannot update time entry to a different month or year",
                                 result_invalid_month.message)
                self.assertEqual(400, result_invalid_month.status_code)

                # Test for additional fields in user data
                result_additional_field = self.time_entry_service.update_time_entry(str(test_additional_field_data['_id']),
                                                                   test_additional_field_data)
                self.assertTrue(result_additional_field.is_successful)
                self.assertEqual("entry updated with warnings ´Skipped fields: additionalField´", result_additional_field.message)
                self.assertEqual(200, result_additional_field.status_code)

                # Reset database to original state
                reset_result_additional_field = self.time_entry_service.update_time_entry(str(test_additional_field_data['_id']),
                                                                         test_original_time_entry_data)
                self.assertTrue(reset_result_additional_field.is_successful)

                result = self.time_entry_service.update_time_entry(str(test_modified_time_entry_data['_id']), test_modified_time_entry_data)
                self.assertEqual(test_modified_time_entry_data, self.time_entry_repository.get_time_entry_by_id(str(test_modified_time_entry_data['_id'])))
                self.assertTrue(result.is_successful)

                # Reset database to original state
                reset_result = self.time_entry_service.update_time_entry(str(test_original_time_entry_data['_id']), test_original_time_entry_data)
                self.assertTrue(reset_result.is_successful)

    def test_delete_time_entry(self):
        """
        Test the delete_time_entry method of the TimeEntryService class.
        """

        test_time_entry_data = {'timesheetId': '6679ca2935df0d8f7202c5fa',
                                'startTime': '2024-05-22T09:20:30.656Z',
                                'endTime': '2024-05-22T12:00:00Z',
                                'entryType': 'Work Entry',
                                'breakTime': 30,
                                'activity': 'testAddTimeEntry of Hiwi1',
                                'projectName': 'timeeEntryServiceTesting'}

        test_complete_timesheet_data = {'timesheetId': '667bd050cf0aa6181e9c8dd9',
                                'startTime': '2024-04-22T09:20:30.656Z',
                                'endTime': '2024-04-22T12:00:00Z',
                                'entryType': 'Work Entry',
                                'breakTime': 30,
                                'activity': 'testAddTimeEntry of Hiwi1',
                                'projectName': 'timeeEntryServiceTesting'}
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                result = self.time_entry_service.create_work_entry(test_time_entry_data, 'testHiwi1')
                self.assertTrue(result.is_successful)
                test_time_entry_id = result.data["_id"]

                # Test for no entry id
                delete_result_no_entry_id = self.time_entry_service.delete_time_entry("")
                self.assertEqual("Entry ID is None", delete_result_no_entry_id.message)
                self.assertEqual(400, delete_result_no_entry_id.status_code)
                self.assertFalse(delete_result_no_entry_id.is_successful)

                # Test for invalid entry id
                delete_result_invalid_entry_id = self.time_entry_service.delete_time_entry("666666666666666666666666")
                self.assertEqual("Time entry not found", delete_result_invalid_entry_id.message)
                self.assertEqual(404, delete_result_invalid_entry_id.status_code)
                self.assertFalse(delete_result_invalid_entry_id.is_successful)

                # Test for invalid timesheet status
                test_complete_timesheet_id = ObjectId('667bd41ed3c08a396da0598c')

                delete_result_invalid_timesheet_status = self.time_entry_service.delete_time_entry(test_complete_timesheet_id)
                self.assertEqual("Cannot delete time entry of a submitted timesheet", delete_result_invalid_timesheet_status.message)
                self.assertEqual(400, delete_result_invalid_timesheet_status.status_code)
                self.assertFalse(delete_result_invalid_timesheet_status.is_successful)

                delete_result = self.time_entry_service.delete_time_entry(test_time_entry_id)
                self.assertTrue(delete_result.is_successful)
                self.assertIsNone(self.time_entry_repository.get_time_entry_by_id(test_time_entry_id))

    def test_get_entries_of_timesheet(self):
        """
        Test the get_entries_of_timesheet method of the TimeEntryService class.
        """
        test_timesheet_id = "6679ca2935df0d8f7202c5fa"
        test_time_entry1 = ObjectId("669170e266478a23c93df4bc")
        test_time_entry2 = ObjectId("66929016ff10a0caf0aedf40")
        test_time_entry3 = ObjectId("6679ce1b327b11ba6160cc1a")

        # Test for invalid timesheet id
        result_invalid_timesheet_id = self.time_entry_service.get_entries_of_timesheet("")
        self.assertEqual("No entries found", result_invalid_timesheet_id.message)
        self.assertEqual(404, result_invalid_timesheet_id.status_code)
        self.assertFalse(result_invalid_timesheet_id.is_successful)

        result = self.time_entry_service.get_entries_of_timesheet(test_timesheet_id)
        self.assertTrue(result.is_successful)
        #for entry in result.data:
        #    print(entry.to_dict())
        self.assertEqual(5, len(result.data))
        self.assertEqual(test_time_entry1, result.data[0].time_entry_id)
        self.assertEqual(test_time_entry2, result.data[1].time_entry_id)
        self.assertEqual(test_time_entry3, result.data[2].time_entry_id)

    if __name__ == '__main__':
        unittest.main()