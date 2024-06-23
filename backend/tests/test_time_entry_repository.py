import datetime
import unittest

from bson import ObjectId

from model.repository.time_entry_repository import TimeEntryRepository
from model.repository.timesheet_repository import TimesheetRepository
from model.time_entry import TimeEntry
from model.work_entry import WorkEntry


class TestTimeEntryRepository(unittest.TestCase):

    def setUp(self):
        self.time_entry_repository = TimeEntryRepository.get_instance()

    def test_get_time_entry_by_id(self):
        """
        Test the get_time_entry_by_id method of the TimeEntryRepository class.
        """

        test_time_entry_data = {'_id': ObjectId('666a1ace21bc45a25b4263d8'), 'timesheetId': '666c1331d28499aff172091c',
                           'startTime': datetime.datetime(2022, 3, 1, 8, 18),
                           'endTime': datetime.datetime(2022, 3, 1, 10, 0),
                           'entryType': 'Work Entry', 'breakTime': 22,
                           'activity': 'Bissle Python Programmieren dies das',
                           'projectName': 'Python Projekt'}
        self.assertEqual(test_time_entry_data, self.time_entry_repository.get_time_entry_by_id("666a1ace21bc45a25b4263d8"))

    def test_get_time_entries_by_date(self):
        """
        Test the get_time_entries_by_date method of the TimeEntryRepository class.
        """
        test_time_entry_data = [
                {'_id': ObjectId('666a1ace21bc45a25b4263d8'), 'timesheetId': '666c1331d28499aff172091c',
                    'startTime': datetime.datetime(2022, 3, 1, 8, 18),
                    'endTime': datetime.datetime(2022, 3, 1, 10, 0),
                    'entryType': 'Work Entry', 'breakTime': 22, 'activity': 'Bissle Python Programmieren dies das',
                    'projectName': 'Python Projekt'},
                {'_id': ObjectId('666c020f7a409003113fedf9'),
                    'timesheetId': '666c1331d28499aff172091c',
                    'startTime': datetime.datetime(2022, 3, 1, 12, 20, 30, 656000),
                    'endTime': datetime.datetime(2022, 3, 1, 10, 0,0),
                    'entryType': 'Work Entry', 'breakTime': 22,
                    'activity': 'Bissle Python Programmieren dies das aktuell',
                    'projectName': 'Es ist bald Zeit für einen neuen Pull'}
            ]
        self.assertEqual(test_time_entry_data, self.time_entry_repository.get_time_entries_by_date(datetime.datetime(2022, 3, 1), "testHiWi"))

    def test_get_time_entries_by_timesheet_id(self):
        """
        Test the get_time_entries_by_timesheet_id method of the TimeEntryRepository class.
        """
        test_time_entry_data = [
                {'_id': ObjectId('666a1ace21bc45a25b4263d8'),
                    'timesheetId': '666c1331d28499aff172091c',
                    'startTime': datetime.datetime(2022, 3, 1, 8, 18),
                    'endTime': datetime.datetime(2022, 3, 1, 10, 0),
                    'entryType': 'Work Entry', 'breakTime': 22, 'activity': 'Bissle Python Programmieren dies das',
                    'projectName': 'Python Projekt'},
                {'_id': ObjectId('666c020f7a409003113fedf9'),
                    'timesheetId': '666c1331d28499aff172091c',
                    'startTime': datetime.datetime(2022, 3, 1, 12, 20, 30, 656000),
                    'endTime': datetime.datetime(2022, 3, 1, 10, 0,0),
                    'entryType': 'Work Entry', 'breakTime': 22,
                    'activity': 'Bissle Python Programmieren dies das aktuell',
                    'projectName': 'Es ist bald Zeit für einen neuen Pull'},
                {'_id': ObjectId('666c9d6d6796c3856a1c5bdd'),
                    'timesheetId': '666c1331d28499aff172091c',
                    'startTime': datetime.datetime(2008, 8, 12, 14, 20, 30, 656000),
                    'endTime': datetime.datetime(2022, 3, 1, 10, 0,0),
                    'entryType': 'Work Entry', 'breakTime': 22,
                    'activity': 'Bissle Python Programmieren dies das aktuell',
                    'projectName': 'Bug Fix Delete'},
            ]

        self.assertEqual(test_time_entry_data,
                         self.time_entry_repository.get_time_entries_by_timesheet_id("666c1331d28499aff172091c"))

    def test_update_time_entry(self):
        """
        Test the update_time_entry method of the TimeEntryRepository class.
        """
        test_original_time_entry_data = {'_id': ObjectId('666a1ace21bc45a25b4263d8'),
                           'timesheetId': '666c1331d28499aff172091c',
                           'startTime': datetime.datetime(2022, 3, 1, 8, 18),
                           'endTime': datetime.datetime(2022, 3, 1, 10, 0),
                           'entryType': 'Work Entry', 'breakTime': 22,
                           'activity': 'Bissle Python Programmieren dies das',
                           'projectName': 'Python Projekt'}
        test_modified_time_entry_data = {'_id': ObjectId('666a1ace21bc45a25b4263d8'),
                           'timesheetId': '666c1331d28499aff172091c',
                           'startTime': datetime.datetime(2022, 3, 1, 8, 18),
                           'endTime': datetime.datetime(2022, 3, 1, 10, 0),
                           'entryType': 'Work Entry', 'breakTime': 10,
                           'activity': 'Bissle Java Programmieren dies das',
                           'projectName': 'Java Projekt'}
        test_original_time_entry = TimeEntry.from_dict(test_original_time_entry_data)
        test_modified_time_entry = TimeEntry.from_dict(test_modified_time_entry_data)

        self.time_entry_repository.update_time_entry(test_modified_time_entry)

        self.assertEqual(test_modified_time_entry_data,
                         self.time_entry_repository.get_time_entry_by_id("666a1ace21bc45a25b4263d8"))
        # Reset the time entry to its original state
        self.time_entry_repository.update_time_entry(test_original_time_entry)

    def test_create_time_entry(self):
        """
        Test the create_time_entry method of the TimeEntryRepository class.
        """
        self.timesheet_repository = TimesheetRepository.get_instance()
        test_time_entry_data = {'timesheetId': '666c1331d28499aff172091c',
                            'startTime': datetime.datetime(2022, 3, 7, 7, 0),
                            'endTime': datetime.datetime(2022, 3, 7, 10, 30),
                            'entryType': 'Work Entry',
                            'breakTime': 40,
                            'activity': 'This WorkEntry is a test used in test_create_time_entry.',
                            'projectName': 'Test Project'}
        test_time_entry = WorkEntry.from_dict(test_time_entry_data)
        result = self.time_entry_repository.create_time_entry(test_time_entry)
        self.assertTrue(result.is_successful)
        test_time_entry_data['_id'] = result.data['_id']
        self.assertEqual(test_time_entry_data,
                         self.time_entry_repository.get_time_entry_by_id(str(result.data['_id'])))
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(test_time_entry_data['timesheetId'])
        self.assertIn(result.data['_id'], timesheet_data['timeEntryIds'])
        result_delete = self.time_entry_repository.delete_time_entry(str(result.data['_id']))
        self.assertTrue(result_delete.is_successful)

    def test_delete_time_entry(self):
        """
        Test the delete_time_entry method of the TimeEntryRepository class.
        """
        self.timesheet_repository = TimesheetRepository.get_instance()
        test_time_entry_data = {'timesheetId': '666c1331d28499aff172091c',
                                'startTime': datetime.datetime(2022, 3, 7, 7, 0),
                                'endTime': datetime.datetime(2022, 3, 7, 10, 30),
                                'entryType': 'Work Entry',
                                'breakTime': 40,
                                'activity': 'This WorkEntry is a test used in test_create_time_entry.',
                                'projectName': 'Test Project'}
        test_time_entry = WorkEntry.from_dict(test_time_entry_data)
        result_create = self.time_entry_repository.create_time_entry(test_time_entry)
        self.assertTrue(result_create.is_successful)
        result_delete = self.time_entry_repository.delete_time_entry(str(result_create.data['_id']))
        self.assertTrue(result_delete.is_successful)
        self.assertIsNone(self.time_entry_repository.get_time_entry_by_id(str(result_create.data['_id'])))
        self.assertNotIn(result_create.data['_id'],
                         self.timesheet_repository.get_timesheet_by_id(test_time_entry_data['timesheetId'])['timeEntryIds'])

    if __name__ == '__main__':
        unittest.main()
