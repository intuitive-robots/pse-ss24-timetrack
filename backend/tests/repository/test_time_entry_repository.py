
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
                                ]

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
        test_time_entry = TimeEntry.from_dict(test_time_entry_data)
        result_create = self.time_entry_repository.create_time_entry(test_time_entry)
        self.assertTrue(result_create.is_successful)
        result_delete = self.time_entry_repository.delete_time_entry(str(result_create.data['_id']))
        self.assertTrue(result_delete.is_successful)
        self.assertIsNone(self.time_entry_repository.get_time_entry_by_id(str(result_create.data['_id'])))

    if __name__ == '__main__':
        unittest.main()
