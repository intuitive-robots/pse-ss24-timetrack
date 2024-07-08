import datetime
import unittest
from unittest.mock import patch

from bson import ObjectId

from model.repository.time_entry_repository import TimeEntryRepository
from service.time_entry_service import TimeEntryService


class TestTimeEntryService(unittest.TestCase):

    def setUp(self):
        self.time_entry_service = TimeEntryService()
        self.time_entry_repository = TimeEntryRepository.get_instance()

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
        result = self.time_entry_service.update_time_entry(str(test_modified_time_entry_data['_id']), test_modified_time_entry_data)
        self.assertTrue(result.is_successful)
        self.assertEqual(test_modified_time_entry_data, self.time_entry_repository.get_time_entry_by_id(str(test_modified_time_entry_data['_id'])))
        # Reset database to original state
        resetResult = self.time_entry_service.update_time_entry(str(test_original_time_entry_data['_id']), test_original_time_entry_data)
        self.assertTrue(resetResult.is_successful)

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
        result = self.time_entry_service.create_work_entry(test_time_entry_data, 'testHiwi1')
        self.assertTrue(result.is_successful)
        test_time_entry_id = result.data["_id"]
        delete_result = self.time_entry_service.delete_time_entry(test_time_entry_id)
        self.assertTrue(delete_result.is_successful)
        self.assertIsNone(self.time_entry_repository.get_time_entry_by_id(test_time_entry_id))

    def test_get_entries_of_timesheet(self):
        """
        Test the get_entries_of_timesheet method of the TimeEntryService class.
        """
        test_timesheet_id = "6679ca2935df0d8f7202c5fa"
        test_time_entry1 = ObjectId("6679ce1b327b11ba6160cc1a")
        test_time_entry2 = ObjectId("666c9d6d6796c3856a1c5bdd")
        test_time_entry3 = ObjectId("666c020f7a409003113fedf9")
        result = self.time_entry_service.get_entries_of_timesheet(test_timesheet_id)
        self.assertTrue(result.is_successful)
        self.assertEqual(3, len(result.data))
        self.assertEqual(test_time_entry1, result.data[0].time_entry_id)
        self.assertEqual(test_time_entry2, result.data[1].time_entry_id)
        self.assertEqual(test_time_entry3, result.data[2].time_entry_id)

    if __name__ == '__main__':
        unittest.main()
