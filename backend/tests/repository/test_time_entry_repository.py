
import datetime
import unittest

from bson import ObjectId

from model.repository.time_entry_repository import TimeEntryRepository
from model.repository.timesheet_repository import TimesheetRepository
from model.time_entry import TimeEntry


class TestTimeEntryRepository(unittest.TestCase):

    def setUp(self):
        self.time_entry_repository = TimeEntryRepository.get_instance()

    def test_get_time_entry_by_id(self):
        """
        Test the get_time_entry_by_id method of the TimeEntryRepository class.
        """
        test_time_entry_data = {'_id': ObjectId('666c020f7a409003113fedf9'),
                                'timesheetId': '6679ca2935df0d8f7202c5fa',
                                'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                'entryType': 'Work Entry',
                                'breakTime': 22,
                                'activity': 'timeEntry1 of Hiwi1',
                                'projectName': 'testing'}

        self.assertEqual(test_time_entry_data, self.time_entry_repository.get_time_entry_by_id(test_time_entry_data['_id']))

    def test_get_time_entries_by_date(self):
        """
        Test the get_time_entries_by_date method of the TimeEntryRepository class.
        """
        test_time_entry_data = [
            {'_id': ObjectId('666c020f7a409003113fedf9'),
             'timesheetId': '6679ca2935df0d8f7202c5fa',
             'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
             'endTime': datetime.datetime(2024, 5, 1, 10, 0),
             'entryType': 'Work Entry',
             'breakTime': 22,
             'activity': 'timeEntry1 of Hiwi1',
             'projectName': 'testing'}
        ]
        # Test for no username
        response_no_username = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 5, 1), None)
        self.assertIsNone(response_no_username)

        # Test get_time_entries_by_date method
        self.assertEqual(test_time_entry_data, self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 5, 1), 'testHiwi1'))

    def test_get_time_entries_by_timesheet_id(self):
        """
        Test the get_time_entries_by_timesheet_id method of the TimeEntryRepository class.
        """
        test_time_entry_data = [{'_id': ObjectId('666c020f7a409003113fedf9'),
                                  'activity': 'timeEntry1 of Hiwi1',
                                  'breakTime': 22,
                                  'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                  'entryType': 'Work Entry',
                                  'projectName': 'testing',
                                  'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                  'timesheetId': '6679ca2935df0d8f7202c5fa'},
                                 {'_id': ObjectId('666c9d6d6796c3856a1c5bdd'),
                                  'activity': 'timeEntry2 of Hiwi1',
                                  'breakTime': 22,
                                  'endTime': datetime.datetime(2024, 5, 12, 16, 0),
                                  'entryType': 'Work Entry',
                                  'projectName': 'testing',
                                  'startTime': datetime.datetime(2024, 5, 12, 14, 20, 30, 656000),
                                  'timesheetId': '6679ca2935df0d8f7202c5fa'},
                                 {'_id': ObjectId('6679ce1b327b11ba6160cc1a'),
                                  'activity': 'timeEntry3 of Hiwi1',
                                  'breakTime': 22,
                                  'endTime': datetime.datetime(2024, 5, 13, 14, 0),
                                  'entryType': 'Work Entry',
                                  'projectName': 'testing',
                                  'startTime': datetime.datetime(2024, 5, 13, 12, 0, 0, 656000),
                                  'timesheetId': '6679ca2935df0d8f7202c5fa'},
                                 {'_id': ObjectId('669170e266478a23c93df4bc'),
                                  'endTime': datetime.datetime(2024, 5, 14, 20, 0),
                                  'entryType': 'Vacation Entry',
                                  'startTime': datetime.datetime(2024, 5, 14, 18, 0, 20),
                                  'timesheetId': '6679ca2935df0d8f7202c5fa'},
                                 {'_id': ObjectId('66929016ff10a0caf0aedf40'),
                                  'activity': 'testWorkEntry',
                                  'breakTime': 0,
                                  'endTime': datetime.datetime(2024, 5, 13, 18, 0),
                                  'entryType': 'Work Entry',
                                  'projectName': 'testing',
                                  'startTime': datetime.datetime(2024, 5, 13, 17, 0),
                                  'timesheetId': '6679ca2935df0d8f7202c5fa'}]

        # Test for no timesheet id
        response_no_timesheet_id = self.time_entry_repository.get_time_entries_by_timesheet_id(None)
        self.assertEqual([], response_no_timesheet_id)

        # Test get_time_entries_by_timesheet_id method
        self.assertEqual(test_time_entry_data,
                         self.time_entry_repository.get_time_entries_by_timesheet_id(test_time_entry_data[0]['timesheetId']))

    def test_update_time_entry(self):
        """
        Test the update_time_entry method of the TimeEntryRepository class.
        """
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
                                         'startTime': datetime.datetime(2024, 5, 20, 8, 20, 30, 656000),
                                         'endTime': datetime.datetime(2024, 5, 20, 10, 0),
                                         'entryType': 'Work Entry',
                                         'breakTime': 22,
                                         'activity': 'modified timeEntry1 of Hiwi1',
                                         'projectName': 'modified testing'}
        invalid_time_entry_data = {'_id': '666666666666666666666666',
                                         'timesheetId': '6679ca2935df0d8f7202c5fa',
                                         'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                         'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                         'entryType': 'Work Entry',
                                         'breakTime': 22,
                                         'activity': 'timeEntry1 of Hiwi1',
                                         'projectName': 'testing'}

        # Test for no time entry
        response_no_time_entry = self.time_entry_repository.update_time_entry(None)
        self.assertEqual("Time entry object is None", response_no_time_entry.message)
        self.assertEqual(False, response_no_time_entry.is_successful)
        self.assertEqual(400, response_no_time_entry.status_code)

        # Test for invalid time entry id
        response_invalid_time_entry = self.time_entry_repository.update_time_entry(TimeEntry.from_dict(invalid_time_entry_data))
        self.assertEqual("Entry not found", response_invalid_time_entry.message)
        self.assertEqual(False, response_invalid_time_entry.is_successful)
        self.assertEqual(404, response_invalid_time_entry.status_code)

        # Test for time entry not changed
        response_no_change = self.time_entry_repository.update_time_entry(TimeEntry.from_dict(test_original_time_entry_data))
        self.assertEqual("Entry update failed (Not Modified)", response_no_change.message)
        self.assertEqual(False, response_no_change.is_successful)
        self.assertEqual(500, response_no_change.status_code)

        # Test update_time_entry method
        test_original_time_entry = TimeEntry.from_dict(test_original_time_entry_data)
        test_modified_time_entry = TimeEntry.from_dict(test_modified_time_entry_data)

        self.time_entry_repository.update_time_entry(test_modified_time_entry)

        self.assertEqual(test_modified_time_entry_data,
                         self.time_entry_repository.get_time_entry_by_id(test_original_time_entry_data['_id']))
        # Reset the time entry to its original state
        self.time_entry_repository.update_time_entry(test_original_time_entry)

    def test_create_time_entry(self):
        """
        Test the create_time_entry method of the TimeEntryRepository class.
        """
        self.timesheet_repository = TimesheetRepository.get_instance()
        test_time_entry_data = {'timesheetId': '6679ca2935df0d8f7202c5fa',
                                'startTime': datetime.datetime(2024, 5, 21, 8, 20, 30, 656000),
                                'endTime': datetime.datetime(2024, 5, 21, 10, 0),
                                'entryType': 'Work Entry',
                                'breakTime': 22,
                                'activity': 'timeEntryCreateTest of Hiwi1',
                                'projectName': 'testing'}
        already_exists_entry_data = {'_id': ObjectId('666c020f7a409003113fedf9'),
                                         'timesheetId': '6679ca2935df0d8f7202c5fa',
                                         'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                         'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                         'entryType': 'Work Entry',
                                         'breakTime': 22,
                                         'activity': 'timeEntry1 of Hiwi1',
                                         'projectName': 'testing'}
        invalid_entry_data = {'_id': None,
                                     'timesheetId': None,
                                     'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                                     'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                                     'entryType': 'Work Entry',
                                     'breakTime': 22,
                                     'activity': 'timeEntry1 of Hiwi1',
                                     'projectName': 'testing'}
        # Test for no time entry
        response_no_time_entry = self.time_entry_repository.create_time_entry(None)
        self.assertEqual("Time entry object is None", response_no_time_entry.message)
        self.assertEqual(False, response_no_time_entry.is_successful)
        self.assertEqual(400, response_no_time_entry.status_code)

        # Test for time entry already exists
        response_time_entry_already_exists = self.time_entry_repository.create_time_entry(TimeEntry.from_dict(already_exists_entry_data))
        self.assertEqual("Time entry already exists", response_time_entry_already_exists.message)
        self.assertEqual(False, response_time_entry_already_exists.is_successful)
        self.assertEqual(409, response_time_entry_already_exists.status_code)

        # Test for invalid time entry
        response_invalid_time_entry = self.time_entry_repository.create_time_entry(
            TimeEntry.from_dict(invalid_entry_data))
        self.assertEqual("Timesheet not found", response_invalid_time_entry.message)
        self.assertEqual(False, response_invalid_time_entry.is_successful)
        self.assertEqual(404, response_invalid_time_entry.status_code)

        test_time_entry = TimeEntry.from_dict(test_time_entry_data)
        result = self.time_entry_repository.create_time_entry(test_time_entry)
        self.assertTrue(result.is_successful)
        test_time_entry_data['_id'] = result.data['_id']
        self.assertEqual(test_time_entry_data,
                         self.time_entry_repository.get_time_entry_by_id(str(result.data['_id'])))
        # delete time entry to reset the database to its orginal state
        result_delete = self.time_entry_repository.delete_time_entry(str(result.data['_id']))
        self.assertTrue(result_delete.is_successful)

    def test_delete_time_entry(self):
        """
        Test the delete_time_entry method of the TimeEntryRepository class.
        """
        self.timesheet_repository = TimesheetRepository.get_instance()
        test_time_entry_data = {'timesheetId': '6679ca2935df0d8f7202c5fa',
                                'startTime': datetime.datetime(2024, 5, 21, 8, 20, 30, 656000),
                                'endTime': datetime.datetime(2024, 5, 21, 10, 0),
                                'entryType': 'Work Entry',
                                'breakTime': 22,
                                'activity': 'timeEntryDeleteTest of Hiwi1',
                                'projectName': 'testing'}
        invalid_entry_data = {'_id': '666666666666666666666666',
                              'timesheetId': '6679ca2935df0d8f7202c5fa',
                              'startTime': datetime.datetime(2024, 5, 1, 8, 20, 30, 656000),
                              'endTime': datetime.datetime(2024, 5, 1, 10, 0),
                              'entryType': 'Work Entry',
                              'breakTime': 22,
                              'activity': 'timeEntry1 of Hiwi1',
                              'projectName': 'testing'}

        # Test for no time entry id
        response_no_time_entry_id = self.time_entry_repository.delete_time_entry(None)
        self.assertEqual("Entry ID is None", response_no_time_entry_id.message)
        self.assertEqual(False, response_no_time_entry_id.is_successful)
        self.assertEqual(400, response_no_time_entry_id.status_code)

        # Test for invalid time entry id
        response_invalid_time_entry_id = self.time_entry_repository.delete_time_entry(invalid_entry_data['_id'])
        self.assertEqual("Time Entry not found", response_invalid_time_entry_id.message)
        self.assertEqual(False, response_invalid_time_entry_id.is_successful)
        self.assertEqual(404, response_invalid_time_entry_id.status_code)

        test_time_entry = TimeEntry.from_dict(test_time_entry_data)
        result_create = self.time_entry_repository.create_time_entry(test_time_entry)
        self.assertTrue(result_create.is_successful)
        result_delete = self.time_entry_repository.delete_time_entry(str(result_create.data['_id']))
        self.assertTrue(result_delete.is_successful)
        self.assertIsNone(self.time_entry_repository.get_time_entry_by_id(str(result_create.data['_id'])))

    if __name__ == '__main__':
        unittest.main()
