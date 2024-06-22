import datetime
import unittest

from bson import ObjectId

from model.repository.time_entry_repository import TimeEntryRepository


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
                           'projectName': 'Python Projekt', 'usedInTests': True}
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

    if __name__ == '__main__':
        unittest.main()
