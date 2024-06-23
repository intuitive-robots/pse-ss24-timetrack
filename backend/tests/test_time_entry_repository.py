import datetime
import unittest

from bson import ObjectId

from model.repository.time_entry_repository import TimeEntryRepository
from model.time_entry import TimeEntry


class TestTimeEntryRepository(unittest.TestCase):

    def setUp(self):
        self.time_entry_repository = TimeEntryRepository.get_instance()

    def test_get_time_entry_by_id(self):
        """
        Test the get_time_entry_by_id method of the TimeEntryRepository class.
        """

        test_time_entry = {'_id': ObjectId('666a1ace21bc45a25b4263d8'), 'timesheetId': '666c1331d28499aff172091c',
                           'startTime': datetime.datetime(2022, 3, 1, 8, 18),
                           'endTime': datetime.datetime(2022, 3, 1, 10, 0),
                           'entryType': 'Work Entry', 'breakTime': 22,
                           'activity': 'Bissle Python Programmieren dies das',
                           'projectName': 'Python Projekt'}
        self.assertEqual(self.time_entry_repository.get_time_entry_by_id("666a1ace21bc45a25b4263d8"), test_time_entry)

    def test_get_time_entries_by_date(self):
        """
        Test the get_time_entries_by_date method of the TimeEntryRepository class.
        """
        test_time_entries = [
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
        self.assertEqual(self.time_entry_repository.get_time_entries_by_date(datetime.datetime(2022, 3, 1), "testHiWi"), test_time_entries)

    def test_get_time_entries_by_timesheet_id(self):
        """
        Test the get_time_entries_by_timesheet_id method of the TimeEntryRepository class.
        """
        test_time_entries = [
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

        self.assertEqual(self.time_entry_repository.get_time_entries_by_timesheet_id("666c1331d28499aff172091c"), test_time_entries)

    def test_update_time_entry(self):
        """
        Test the update_time_entry method of the TimeEntryRepository class.
        """
        test_original_time_entry = {'_id': ObjectId('666a1ace21bc45a25b4263d8'), 'timesheetId': '666c1331d28499aff172091c',
                           'startTime': datetime.datetime(2022, 3, 1, 8, 18),
                           'endTime': datetime.datetime(2022, 3, 1, 10, 0),
                           'entryType': 'Work Entry', 'breakTime': 22,
                           'activity': 'Bissle Python Programmieren dies das',
                           'projectName': 'Python Projekt'}
        test_modified_time_entry = {'_id': ObjectId('666a1ace21bc45a25b4263d8'),
                                    'timesheetId': '666c1331d28499aff172091c',
                                    'startTime': datetime.datetime(2022, 3, 1, 8, 18),
                                    'endTime': datetime.datetime(2022, 3, 1, 10, 0),
                                    'entryType': 'Work Entry', 'breakTime': 10,
                                    'activity': 'Bissle Java Programmieren dies das',
                                    'projectName': 'Java Projekt'}
        test_original_time_entry_object = TimeEntry.from_dict(test_original_time_entry)
        test_modified_time_entry_object = TimeEntry.from_dict(test_modified_time_entry)

        self.time_entry_repository.update_time_entry(test_modified_time_entry_object)
        self.assertEqual(self.time_entry_repository.get_time_entry_by_id("666a1ace21bc45a25b4263d8"), test_modified_time_entry)
        self.time_entry_repository.update_time_entry(test_original_time_entry_object)

    if __name__ == '__main__':
        unittest.main()
