
import datetime
import unittest

from bson import ObjectId

from db import initialize_db
from model.repository.time_entry_repository import TimeEntryRepository
from model.repository.timesheet_repository import TimesheetRepository
from model.time_entry import TimeEntry


class TestTimeEntryRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = initialize_db()
        cls.time_entry_repository = TimeEntryRepository.get_instance()

    def setUp(self):
        self.test_april_timesheet_data = {'username': 'testHiwiTimeEntryRepo',
                                          'month': 4,
                                          'year': 2024,
                                          'status': 'Complete',
                                          'totalTime': 0.0,
                                          'overtime': 0.0,
                                          'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                          'vacationMinutes': 0.0}

        self.db.timesheets.insert_one(self.test_april_timesheet_data)

        self.test_april_1_time_entry_data = {'timesheetId': str(self.test_april_timesheet_data['_id']),
                                             'startTime': datetime.datetime(2024, 4, 1, 8, 0, 0, 0),
                                             'endTime': datetime.datetime(2024, 4, 1, 10, 0),
                                             'entryType': 'Work Entry',
                                             'breakTime': 10,
                                             'activity': 'timeEntryRepoActivitiy',
                                             'activityType': 'Projektbesprechung',
                                             'projectName': 'timeEntryRepoTest'}

        self.test_april_8_time_entry_data = {'timesheetId': str(self.test_april_timesheet_data['_id']),
                                             'startTime': datetime.datetime(2024, 4, 8, 8, 0, 0, 0),
                                             'endTime': datetime.datetime(2024, 4, 8, 10, 0),
                                             'entryType': 'Work Entry',
                                             'breakTime': 10,
                                             'activity': 'timeEntryRepoActivitiy',
                                             'activityType': 'Projektbesprechung',
                                             'projectName': 'timeEntryRepoTest'}

        self.db.timeEntries.insert_one(self.test_april_1_time_entry_data)
        self.db.timeEntries.insert_one(self.test_april_8_time_entry_data)

    def tearDown(self):
        self.db.timesheets.delete_many({'username': 'testHiwiTimeEntryRepo'})
        self.db.timeEntries.delete_many({'projectName': 'timeEntryRepoTest'})

    def test_get_time_entry_by_id(self):
        """
        Test the get_time_entry_by_id method of the TimeEntryRepository class.
        """
        self.assertEqual(self.test_april_1_time_entry_data, self.time_entry_repository.get_time_entry_by_id(
            self.test_april_1_time_entry_data['_id']))

    def test_get_time_entries_by_date(self):
        """
        Test the get_time_entries_by_date method of the TimeEntryRepository class.
        """
        self.assertEqual([self.test_april_1_time_entry_data], self.time_entry_repository.get_time_entries_by_date(
            datetime.date(2024, 4, 1), self.test_april_timesheet_data['username']))

    def test_get_time_entries_by_date_no_username(self):
        """
        Test get_time_entries_by_date method with no username.
        """
        response_no_username = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 5, 1), None)
        self.assertIsNone(response_no_username)

    def test_get_time_entries_by_timesheet_id(self):
        """
        Test the get_time_entries_by_timesheet_id method of the TimeEntryRepository class.
        """
        self.assertEqual([self.test_april_1_time_entry_data, self.test_april_8_time_entry_data],
                         self.time_entry_repository.get_time_entries_by_timesheet_id(
                             self.test_april_1_time_entry_data['timesheetId']))

    def test_get_time_entries_by_timesheet_id_no_id(self):
        """
        Test the get_time_entries_by_timesheet_id method of the TimeEntryRepository class with no id.
        """
        response_no_timesheet_id = self.time_entry_repository.get_time_entries_by_timesheet_id(None)
        self.assertEqual([], response_no_timesheet_id)

    def test_update_time_entry(self):
        """
        Test the update_time_entry method of the TimeEntryRepository class.
        """
        self.test_april_1_time_entry_data['activity'] = 'timeEntryRepoUpdateActivity'
        test_modified_time_entry = TimeEntry.from_dict(self.test_april_1_time_entry_data)

        self.time_entry_repository.update_time_entry(test_modified_time_entry)

        self.assertEqual(self.test_april_1_time_entry_data,
                         self.db.timeEntries.find_one({'_id': self.test_april_1_time_entry_data['_id']}))

    def test_update_time_entry_no_data(self):
        """
        Test the update_time_entry method of the TimeEntryRepository class with no data.
        """
        response_no_time_entry = self.time_entry_repository.update_time_entry(None)
        self.assertEqual("Time entry object is None", response_no_time_entry.message)
        self.assertEqual(False, response_no_time_entry.is_successful)
        self.assertEqual(400, response_no_time_entry.status_code)

    def test_update_time_entry_invalid_id(self):
        """
        Test the update_time_entry method of the TimeEntryRepository class with an invalid id.
        """
        self.test_april_1_time_entry_data['_id'] = ObjectId('666666666666666666666666')
        response_invalid_time_entry = self.time_entry_repository.update_time_entry(
            TimeEntry.from_dict(self.test_april_1_time_entry_data))
        self.assertEqual("Entry not found", response_invalid_time_entry.message)
        self.assertEqual(False, response_invalid_time_entry.is_successful)
        self.assertEqual(404, response_invalid_time_entry.status_code)

    def test_update_time_entry_no_change(self):
        """
        Test the update_time_entry method of the TimeEntryRepository class with no change.
        """
        response_no_change = self.time_entry_repository.update_time_entry(
            TimeEntry.from_dict(self.test_april_1_time_entry_data))
        self.assertEqual("Entry update failed (Not Modified)", response_no_change.message)
        self.assertEqual(False, response_no_change.is_successful)
        self.assertEqual(500, response_no_change.status_code)

    def test_create_time_entry(self):
        """
        Test the create_time_entry method of the TimeEntryRepository class.
        """
        test_time_entry = self.test_april_1_time_entry_data.copy()
        test_time_entry['_id'] = None
        test_time_entry['activity'] = 'timeEntryRespoCreateActivity'
        result = self.time_entry_repository.create_time_entry(TimeEntry.from_dict(test_time_entry))
        self.assertTrue(result.is_successful)
        test_time_entry['_id'] = result.data['_id']
        self.assertEqual(test_time_entry,
                         self.db.timeEntries.find_one({'_id': result.data['_id']}))

    def test_create_time_entry_no_data(self):
        """
        Test the create_time_entry method of the TimeEntryRepository class with no data.
        """
        response_no_time_entry = self.time_entry_repository.create_time_entry(None)
        self.assertEqual("Time entry object is None", response_no_time_entry.message)
        self.assertEqual(False, response_no_time_entry.is_successful)
        self.assertEqual(400, response_no_time_entry.status_code)

    def test_create_time_entry_already_exists(self):
        """
        Test the create_time_entry method of the TimeEntryRepository class with an already existing entry.
        """
        response_time_entry_already_exists = self.time_entry_repository.create_time_entry(
            TimeEntry.from_dict(self.test_april_1_time_entry_data))
        self.assertEqual("Time entry already exists", response_time_entry_already_exists.message)
        self.assertEqual(False, response_time_entry_already_exists.is_successful)
        self.assertEqual(409, response_time_entry_already_exists.status_code)

    def test_create_time_entry_invalid_data(self):
        """
        Test the create_time_entry method of the TimeEntryRepository class with invalid data.
        """
        self.test_april_1_time_entry_data['_id'] = None
        self.test_april_1_time_entry_data['timesheetId'] = None
        response_invalid_time_entry = self.time_entry_repository.create_time_entry(
            TimeEntry.from_dict(self.test_april_1_time_entry_data))
        self.assertEqual("Timesheet not found", response_invalid_time_entry.message)
        self.assertEqual(False, response_invalid_time_entry.is_successful)
        self.assertEqual(404, response_invalid_time_entry.status_code)

    def test_delete_time_entry(self):
        """
        Test the delete_time_entry method of the TimeEntryRepository class.
        """
        result_delete = self.time_entry_repository.delete_time_entry(str(self.test_april_1_time_entry_data['_id']))
        self.assertTrue(result_delete.is_successful)
        self.assertIsNone(self.db.timeEntries.find_one({'_id': self.test_april_1_time_entry_data['_id']}))

    def test_delete_time_entry_no_id(self):
        """
        Test the delete_time_entry method of the TimeEntryRepository class with no id.
        """
        response_no_time_entry_id = self.time_entry_repository.delete_time_entry(None)
        self.assertEqual("Entry ID is None", response_no_time_entry_id.message)
        self.assertEqual(False, response_no_time_entry_id.is_successful)
        self.assertEqual(400, response_no_time_entry_id.status_code)

    def test_delete_time_entry_invalid_data(self):
        """
        Test the delete_time_entry method of the TimeEntryRepository class with an invalid id.
        """
        self.test_april_1_time_entry_data['_id'] = ObjectId('666666666666666666666666')
        response_invalid_time_entry_id = self.time_entry_repository.delete_time_entry(self.test_april_1_time_entry_data['_id'])
        self.assertEqual("Time Entry not found", response_invalid_time_entry_id.message)
        self.assertEqual(False, response_invalid_time_entry_id.is_successful)
        self.assertEqual(404, response_invalid_time_entry_id.status_code)

    if __name__ == '__main__':
        unittest.main()
