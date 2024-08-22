import unittest
import datetime
from unittest import TestCase

from bson import ObjectId

from db import initialize_db
from model.repository.timesheet_repository import TimesheetRepository
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus


class TestTimesheetRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = initialize_db()
        cls.timesheet_repository = TimesheetRepository.get_instance()

    def setUp(self):
        self.test_april_timesheet_data = {'username': 'testHiwiTimesheetRepo',
                                         'month': 4,
                                         'year': 2024,
                                         'status': 'Complete',
                                         'totalTime': 0.0,
                                         'overtime': 0.0,
                                         'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                         'vacationMinutes': 0.0}

        self.test_may_timesheet_data = {'username': 'testHiwiTimesheetRepo',
                                       'month': 5,
                                       'year': 2024,
                                       'status': 'Waiting for Approval',
                                       'totalTime': 0.0,
                                       'overtime': 0.0,
                                       'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                       'vacationMinutes': 0.0}

        self.test_june_timesheet_data = {'username': 'testHiwiTimesheetRepo',
                                        'month': 6,
                                        'year': 2024,
                                        'status': 'Not Submitted',
                                        'totalTime': 0.0,
                                        'overtime': 0.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                                        'vacationMinutes': 0.0}

        self.db.timesheets.insert_one(self.test_april_timesheet_data)
        self.db.timesheets.insert_one(self.test_may_timesheet_data)
        self.db.timesheets.insert_one(self.test_june_timesheet_data)

    def tearDown(self):
        self.db.timesheets.delete_many({"username": "testHiwiTimesheetRepo"})

    def test_test(self):
        pass

    def test_get_timesheet_by_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetRepository class.
        """
        self.assertEqual(self.test_may_timesheet_data,
                         self.timesheet_repository.get_timesheet_by_id(str(self.test_may_timesheet_data['_id'])))

    def test_get_timesheet_by_id_no_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetRepository class with no id.
        """
        response_no_timesheet_id = self.timesheet_repository.get_timesheet_by_id(None)
        self.assertIsNone(response_no_timesheet_id)

    def test_get_timesheet_by_id_invalid_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetRepository class with an invalid id.
        """
        response_invalid_timesheet_id = self.timesheet_repository.get_timesheet_by_id("666666666666666666666666")
        self.assertIsNone(response_invalid_timesheet_id)

    def test_get_timesheet(self):
        """
        Test the get_timesheet method of the TimesheetRepository class.
        """
        self.assertEqual(self.test_may_timesheet_data, self.timesheet_repository.
                         get_timesheet(self.test_may_timesheet_data['username'],self.test_may_timesheet_data['month'],
                                       self.test_may_timesheet_data['year']))

    def test_get_timesheet_no_username(self):
        """
        Test the get_timesheet method of the TimesheetRepository class with no username.
        """
        response_no_username = self.timesheet_repository.get_timesheet(None, 5, 2024)
        self.assertIsNone(response_no_username)

    def test_get_current_timesheet(self):
        """
        Test the get_current_timesheet method of the TimesheetRepository class.
        """
        self.assertEqual(self.test_june_timesheet_data,
                         self.timesheet_repository.get_current_timesheet(self.test_june_timesheet_data['username']))

    def test_get_current_timesheet_no_username(self):
        """
        Test the get_current_timesheet method of the TimesheetRepository class.
        """
        response_no_username = self.timesheet_repository.get_current_timesheet(None)
        self.assertIsNone(response_no_username)

    def test_get_timesheets_by_time_period(self):
        """
        Test the get_timesheets_by_time_period method of the TimesheetRepository class.
        """
        timesheets = self.timesheet_repository.get_timesheets_by_time_period(self.test_april_timesheet_data['username'],
                                                                             datetime.date(2024, 4, 12),
                                                                             datetime.date(2024, 5, 12))
        for timesheet in timesheets:
            self.assertIn(timesheet, [self.test_april_timesheet_data, self.test_may_timesheet_data])

    def test_get_timesheets_by_time_period_no_username(self):
        """
        Test the get_timesheets_by_time_period method of the TimesheetRepository class with no username.
        """
        response_no_username = self.timesheet_repository.get_timesheets_by_time_period(None,
                                                                                       datetime.date(2024, 4, 12),
                                                                                       datetime.date(2024, 5, 12))
        self.assertIsNone(response_no_username)

    def test_get_timesheets(self):
        """
        Test the get_timesheets method of the TimesheetRepository class.
        """
        timesheets = self.timesheet_repository.get_timesheets()
        for timesheet in timesheets:
            self.assertIn(timesheet, [self.test_may_timesheet_data, self.test_april_timesheet_data,
                                      self.test_june_timesheet_data])

    def test_get_timesheets_by_status(self):
        """
        Test the get_timesheet_by_status method of the TimesheetRepository class.
        """
        self.assertEqual([self.test_june_timesheet_data],
                         self.timesheet_repository.get_timesheets_by_status(TimesheetStatus.NOT_SUBMITTED))

    def test_get_timesheets_by_status_no_status(self):
        """
        Test the get_timesheet_by_status method of the TimesheetRepository class with no status.
        """
        response_no_status = self.timesheet_repository.get_timesheets_by_status(None)
        self.assertIsNone(response_no_status)

    def test_get_timesheet_id(self):
        """
        Test the get_timesheet_id method of the TimesheetRepository class.
        """
        self.assertEqual(self.test_may_timesheet_data['_id'],
                         self.timesheet_repository.get_timesheet_id(self.test_may_timesheet_data['username'],
                                                                    self.test_may_timesheet_data['month'],
                                                                    self.test_may_timesheet_data['year']))

    def test_get_timesheet_id_no_username(self):
        """
        Test the get_timesheet_id method of the TimesheetRepository class with no username.
        """
        response_no_username = self.timesheet_repository.get_timesheet_id(None, 5, 2024)
        self.assertIsNone(response_no_username)

    def test_get_timesheets_by_username_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetRepository class.
        """
        self.assertEqual([self.test_june_timesheet_data],
                         self.timesheet_repository.
                         get_timesheets_by_username_status(self.test_june_timesheet_data['username'],
                                                           TimesheetStatus.NOT_SUBMITTED))

    def test_get_timesheets_by_username_status_no_username(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetRepository class with no username.
        """
        response_no_username = (self.timesheet_repository.
                                get_timesheets_by_username_status(None, TimesheetStatus.NOT_SUBMITTED))
        self.assertIsNone(response_no_username)

    def test_get_timesheets_by_username(self):
        """
        Test the get_timesheets_by_username method of the TimesheetRepository class.
        """
        timesheets = self.timesheet_repository.get_timesheets_by_username(self.test_april_timesheet_data['username'])
        for timesheet in timesheets:
            self.assertIn(timesheet, [self.test_april_timesheet_data, self.test_may_timesheet_data,
                                      self.test_june_timesheet_data])

    def test_get_timesheets_by_username_no_username(self):
        """
        Test the get_timesheets_by_username method of the TimesheetRepository class with no username.
        """
        response_no_username = self.timesheet_repository.get_timesheets_by_username(None)
        self.assertIsNone(response_no_username)

    def test_update_timesheet_by_dict(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_modified_timesheet_data = self.test_may_timesheet_data.copy()
        test_modified_timesheet_data['totalTime'] = 1.0

        # Test update_timesheet_by_dict method
        response = self.timesheet_repository.update_timesheet_by_dict(test_modified_timesheet_data)
        self.assertEqual("Timesheet updated successfully", response.message)
        self.assertEqual(True, response.is_successful)
        self.assertEqual(200, response.status_code)

        modified_timesheet = self.timesheet_repository.get_timesheet_by_id(test_modified_timesheet_data['_id'])
        self.assertEqual(test_modified_timesheet_data, modified_timesheet)

    def test_update_timesheet_by_dict_no_timesheet(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class with no timesheet data.
        """
        response_no_data = self.timesheet_repository.update_timesheet_by_dict(None)
        self.assertEqual("Please provide a timesheet to update.", response_no_data.message)
        self.assertEqual(False, response_no_data.is_successful)
        self.assertEqual(400, response_no_data.status_code)

    def test_update_timesheet_by_dict_invalid_data(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class with invalid timesheet data.
        """
        test_invalid_timesheet_data = self.test_may_timesheet_data.copy()
        test_invalid_timesheet_data['_id'] = ObjectId('666666666666666666666666')

        response_invalid_data = self.timesheet_repository.update_timesheet_by_dict(test_invalid_timesheet_data)
        self.assertEqual("Timesheet not found", response_invalid_data.message)
        self.assertEqual(False, response_invalid_data.is_successful)
        self.assertEqual(404, response_invalid_data.status_code)

    def test_update_timesheet(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_modified_timesheet_data = self.test_may_timesheet_data.copy()
        test_modified_timesheet_data['totalTime'] = 1.0

        response = self.timesheet_repository.update_timesheet(Timesheet.from_dict(test_modified_timesheet_data))
        self.assertEqual("Timesheet updated successfully", response.message)
        self.assertEqual(True, response.is_successful)
        self.assertEqual(200, response.status_code)

        modified_timesheet = self.timesheet_repository.get_timesheet_by_id(test_modified_timesheet_data['_id'])
        self.assertEqual(test_modified_timesheet_data, modified_timesheet)

    def test_update_timesheet_no_data(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class with no data.
        """
        response_no_userdata = self.timesheet_repository.update_timesheet(None)
        self.assertEqual("Please provide a timesheet to update.", response_no_userdata.message)
        self.assertEqual(False, response_no_userdata.is_successful)
        self.assertEqual(400, response_no_userdata.status_code)

    def test_update_timesheet_invalid_data(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class with invalid timesheet data.
        """
        test_invalid_timesheet_data = self.test_may_timesheet_data.copy()
        test_invalid_timesheet_data['_id'] = ObjectId('666666666666666666666666')

        response_no_userdata = self.timesheet_repository.update_timesheet(Timesheet.from_dict(test_invalid_timesheet_data))
        self.assertEqual("Timesheet not found", response_no_userdata.message)
        self.assertEqual(False, response_no_userdata.is_successful)
        self.assertEqual(404, response_no_userdata.status_code)

    def test_set_timesheet_status(self):
        """
        Test the set_timesheet_status method of the TimesheetRepository class.
        """
        self.timesheet_repository.set_timesheet_status(str(self.test_june_timesheet_data['_id']), TimesheetStatus.COMPLETE)
        self.assertEqual(str(TimesheetStatus.COMPLETE), self.db.timesheets.find_one({'_id': self.test_june_timesheet_data['_id']})['status'])

    def test_set_timesheet_status_no_data(self):
        """
        Test the set_timesheet_status method of the TimesheetRepository class with no data.
        """
        response_no_timesheet_data = self.timesheet_repository.set_timesheet_status(None, TimesheetStatus.COMPLETE)
        self.assertEqual("Please provide a timesheet ID and status to update the timesheet status.", response_no_timesheet_data.message)
        self.assertEqual(False, response_no_timesheet_data.is_successful)
        self.assertEqual(400, response_no_timesheet_data.status_code)

    def test_set_timesheet_status_invalid_data(self):
        """
        Test the set_timesheet_status method of the TimesheetRepository class.
        """
        response_invalid_timesheet_data = self.timesheet_repository.set_timesheet_status("666666666666666666666666", TimesheetStatus.COMPLETE)
        self.assertEqual("Timesheet not found", response_invalid_timesheet_data.message)
        self.assertEqual(False, response_invalid_timesheet_data.is_successful)
        self.assertEqual(404, response_invalid_timesheet_data.status_code)

    def test_create_timesheet_by_dict(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_timesheet_data = self.test_june_timesheet_data.copy()
        test_timesheet_data.pop('_id')
        test_timesheet_data['month'] = 7
        result = self.timesheet_repository.create_timesheet_by_dict(test_timesheet_data)
        test_timesheet_data['_id'] = result.data['_id']
        self.assertEqual(test_timesheet_data, self.db.timesheets.find_one({'_id': result.data['_id']}))

    def test_create_timesheet_by_dict_no_data(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class with no data.
        """
        response_no_timesheet_data = self.timesheet_repository.create_timesheet_by_dict(None)
        self.assertEqual("Please provide a timesheet to create.", response_no_timesheet_data.message)
        self.assertEqual(False, response_no_timesheet_data.is_successful)
        self.assertEqual(400, response_no_timesheet_data.status_code)

    def test_create_timesheet_by_dict_already_exists(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class with a timesheet that already exists.
        """
        response_already_exists = self.timesheet_repository.create_timesheet_by_dict(self.test_june_timesheet_data)
        self.assertEqual("Timesheet already exists", response_already_exists.message)
        self.assertEqual(False, response_already_exists.is_successful)
        self.assertEqual(409, response_already_exists.status_code)

    def test_create_timesheet(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_timesheet_data = self.test_june_timesheet_data.copy()
        test_timesheet_data.pop('_id')
        test_timesheet_data['month'] = 7
        result = self.timesheet_repository.create_timesheet(Timesheet.from_dict(test_timesheet_data))
        test_timesheet_data['_id'] = result.data['_id']
        self.assertEqual(test_timesheet_data, self.db.timesheets.find_one({'_id': result.data['_id']}))

    def test_create_timesheet_no_data(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class with no data.
        """
        response_no_timesheet_data = self.timesheet_repository.create_timesheet(None)
        self.assertEqual("Please provide a timesheet to create.", response_no_timesheet_data.message)
        self.assertEqual(False, response_no_timesheet_data.is_successful)
        self.assertEqual(400, response_no_timesheet_data.status_code)

    def test_create_timesheet_already_exists(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class with a timesheet that already exists.
        """
        response_already_exists = self.timesheet_repository.create_timesheet(
            Timesheet.from_dict(self.test_june_timesheet_data))
        self.assertEqual("Timesheet already exists", response_already_exists.message)
        self.assertEqual(False, response_already_exists.is_successful)
        self.assertEqual(409, response_already_exists.status_code)

    def test_delete_timesheet(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class.
        """
        self.timesheet_repository.delete_timesheet(self.test_june_timesheet_data['_id'])
        self.assertIsNone(self.db.timesheets.find_one({'_id': self.test_june_timesheet_data['_id']}))

    def test_delete_timesheet_no_data(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class with no data.
        """
        response_no_timesheet_id = self.timesheet_repository.delete_timesheet(None)
        self.assertEqual("Please provide a timesheet ID to delete the timesheet.", response_no_timesheet_id.message)
        self.assertEqual(False, response_no_timesheet_id.is_successful)
        self.assertEqual(400, response_no_timesheet_id.status_code)

    if __name__ == '__main__':
        unittest.main()
