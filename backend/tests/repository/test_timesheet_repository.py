import unittest
import datetime
from unittest import TestCase

from bson import ObjectId

from model.repository.timesheet_repository import TimesheetRepository
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus


class TestTimesheetRepository(unittest.TestCase):

    def setUp(self):
        self.timesheet_repository = TimesheetRepository.get_instance()

    def test_get_timesheet_by_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                               'username': 'testHiwi1',
                               'month': 5,
                               'year': 2024,
                               'status': 'Not Submitted',
                               'totalTime': 0.0,
                               'overtime': 0.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no timesheet_id
        response_no_timesheet_id = self.timesheet_repository.get_timesheet_by_id(None)
        self.assertIsNone(response_no_timesheet_id)

        # Test for invalid timesheet_id
        response_invalid_timesheet_id = self.timesheet_repository.get_timesheet_by_id("666666666666666666666666")
        self.assertIsNone(response_invalid_timesheet_id)

        self.assertEqual(test_timesheet_data,
                         self.timesheet_repository.get_timesheet_by_id(str(test_timesheet_data['_id'])))

    def test_get_timesheet(self):
        """
        Test the get_timesheet method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                               'username': 'testHiwi1',
                               'month': 5,
                               'year': 2024,
                               'status': 'Not Submitted',
                               'totalTime': 0.0,
                               'overtime': 0.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no username
        response_no_username = self.timesheet_repository.get_timesheet(None, 5, 2024)
        self.assertIsNone(response_no_username)

        self.assertEqual(test_timesheet_data, self.timesheet_repository.get_timesheet(test_timesheet_data['username'],
                                                                                      test_timesheet_data['month'],
                                                                                      test_timesheet_data['year']))

    def test_get_current_timesheet(self):
        """
        Test the get_current_timesheet method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                               'username': 'testHiwi1',
                               'month': 5,
                               'year': 2024,
                               'status': 'Not Submitted',
                               'totalTime': 0.0,
                               'overtime': 0.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no username
        response_no_username = self.timesheet_repository.get_current_timesheet(None)
        self.assertIsNone(response_no_username)

        self.assertEqual(test_timesheet_data,
                         self.timesheet_repository.get_current_timesheet(test_timesheet_data['username']))

    def test_get_timesheets_by_time_period(self):
        test_timesheet_data = [
            {'_id': ObjectId('667bd050cf0aa6181e9c8dd9'),
             'username': 'testHiwi1',
             'month': 4,
             'year': 2024,
             'status': 'Complete',
             'totalTime': 0.0,
             'overtime': 0.0,
             'lastSignatureChange': datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)},
            {'_id': ObjectId('667bd14ecf0aa6181e9c8dda'),
             'username': 'testHiwi1',
             'month': 3,
             'year': 2024,
             'status': 'Complete',
             'totalTime': 0.0,
             'overtime': 0.0,
             'lastSignatureChange': datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)}]

        # Test for no username
        response_no_username = self.timesheet_repository.get_timesheets_by_time_period(None,
                                                                                       datetime.date(2024, 3, 12),
                                                                                       datetime.date(2024, 4, 12))
        self.assertIsNone(response_no_username)

        self.assertEqual(test_timesheet_data,
                         self.timesheet_repository.get_timesheets_by_time_period(test_timesheet_data[0]['username'],
                                                                                 datetime.date(2024, 3, 12),
                                                                                 datetime.date(2024, 4, 12)))

    def test_get_timesheets(self):
        timesheets = self.timesheet_repository.get_timesheets()
        self.assertIsNotNone(timesheets)

    def test_get_timesheets_by_status(self):
        """
        Test the get_timesheet_by_status method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                               'username': 'testHiwi1',
                               'month': 5,
                               'year': 2024,
                               'status': 'Not Submitted',
                               'totalTime': 0.0,
                               'overtime': 0.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no status
        response_no_status = self.timesheet_repository.get_timesheets_by_status(None)
        self.assertIsNone(response_no_status)

        self.assertEqual(test_timesheet_data,
                         self.timesheet_repository.get_timesheets_by_status(TimesheetStatus.NOT_SUBMITTED)[0])

    def test_get_timesheet_id(self):
        """
        Test the get_timesheet_id method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                               'username': 'testHiwi1',
                               'month': 5,
                               'year': 2024,
                               'status': 'Not Submitted',
                               'totalTime': 0.0,
                               'overtime': 0.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no username
        response_no_username = self.timesheet_repository.get_timesheet_id(None, 5, 2024)
        self.assertIsNone(response_no_username)

        self.assertEqual(test_timesheet_data['_id'],
                         self.timesheet_repository.get_timesheet_id(test_timesheet_data['username'],
                                                                    test_timesheet_data['month'],
                                                                    test_timesheet_data['year']))

    def test_get_timesheets_by_username_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetRepository class.
        """
        test_timesheet_data = [{'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                                'username': 'testHiwi1',
                                'month': 5,
                                'year': 2024,
                                'status': 'Not Submitted',
                                'totalTime': 0.0,
                                'overtime': 0.0,
                                'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}]

        # Test for no username
        response_no_username = self.timesheet_repository.get_timesheets_by_username_status(None, TimesheetStatus.NOT_SUBMITTED)
        self.assertIsNone(response_no_username)

        self.assertEqual(test_timesheet_data,
                         self.timesheet_repository.get_timesheets_by_username_status(test_timesheet_data[0]['username'],
                                                                                     TimesheetStatus.NOT_SUBMITTED))

    def test_get_timesheets_by_username(self):
        test_timesheet_data = [
            {'_id': ObjectId('6679ca2935df0d8f7202c5fa'), 'username': 'testHiwi1', 'month': 5, 'year': 2024,
             'status': 'Not Submitted', 'totalTime': 0.0, 'overtime': 0.0,
             'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)},
            {'_id': ObjectId('667bd050cf0aa6181e9c8dd9'), 'username': 'testHiwi1', 'month': 4, 'year': 2024,
             'status': 'Complete', 'totalTime': 0.0, 'overtime': 0.0,
             'lastSignatureChange': datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)},
            {'_id': ObjectId('667bd14ecf0aa6181e9c8dda'), 'username': 'testHiwi1', 'month': 3, 'year': 2024,
             'status': 'Complete', 'totalTime': 0.0, 'overtime': 0.0,
             'lastSignatureChange': datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)}]

        # Test for no username
        response_no_username = self.timesheet_repository.get_timesheets_by_username(None)
        self.assertIsNone(response_no_username)

        self.assertEqual(test_timesheet_data,
                         self.timesheet_repository.get_timesheets_by_username(test_timesheet_data[0]['username']))

    def test_update_timesheet_by_dict(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_original_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                                        'username': 'testHiwi1',
                                        'month': 5,
                                        'year': 2024,
                                        'status': 'Not Submitted',
                                        'totalTime': 0.0,
                                        'overtime': 0.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}
        test_modified_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                                        'username': 'testHiwi1',
                                        'month': 5,
                                        'year': 2024,
                                        'status': 'Not Submitted',
                                        'totalTime': 1.0,
                                        'overtime': 1.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}
        invalid_timesheet_data = {'_id': ObjectId('666666666666666666666666'),
                                        'username': 'testHiwi1',
                                        'month': 5,
                                        'year': 2024,
                                        'status': 'Not Submitted',
                                        'totalTime': 1.0,
                                        'overtime': 1.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no timesheet data
        response_no_userdata = self.timesheet_repository.update_timesheet_by_dict(None)
        self.assertEqual("Please provide a timesheet to update.", response_no_userdata.message)
        self.assertEqual(False, response_no_userdata.is_successful)
        self.assertEqual(400, response_no_userdata.status_code)

        # Test for invalid timesheet data
        response_no_userdata = self.timesheet_repository.update_timesheet_by_dict(invalid_timesheet_data)
        self.assertEqual("Timesheet not found", response_no_userdata.message)
        self.assertEqual(False, response_no_userdata.is_successful)
        self.assertEqual(404, response_no_userdata.status_code)

        # Test update_timesheet_by_dict method
        response = self.timesheet_repository.update_timesheet_by_dict(test_modified_timesheet_data)
        self.assertEqual("Timesheet updated successfully", response.message)
        self.assertEqual(True, response.is_successful)
        self.assertEqual(200, response.status_code)

        modified_timesheet = self.timesheet_repository.get_timesheet_by_id(test_modified_timesheet_data['_id'])
        self.assertEqual(test_modified_timesheet_data, modified_timesheet)

        # Reset the database to its original state
        response_reset = self.timesheet_repository.update_timesheet_by_dict(test_original_timesheet_data)
        self.assertEqual("Timesheet updated successfully", response_reset.message)
        self.assertEqual(True, response_reset.is_successful)
        self.assertEqual(200, response_reset.status_code)

    def test_update_timesheet(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_original_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                                        'username': 'testHiwi1',
                                        'month': 5,
                                        'year': 2024,
                                        'status': 'Not Submitted',
                                        'totalTime': 0.0,
                                        'overtime': 0.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}
        test_modified_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                                        'username': 'testHiwi1',
                                        'month': 5,
                                        'year': 2024,
                                        'status': 'Not Submitted',
                                        'totalTime': 1.0,
                                        'overtime': 1.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}
        invalid_timesheet_data = {'_id': ObjectId('666666666666666666666666'),
                                  'username': 'testHiwi1',
                                  'month': 5,
                                  'year': 2024,
                                  'status': 'Not Submitted',
                                  'totalTime': 1.0,
                                  'overtime': 1.0,
                                  'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no timesheet data
        response_no_userdata = self.timesheet_repository.update_timesheet(None)
        self.assertEqual("Please provide a timesheet to update.", response_no_userdata.message)
        self.assertEqual(False, response_no_userdata.is_successful)
        self.assertEqual(400, response_no_userdata.status_code)

        # Test for invalid timesheet data
        response_no_userdata = self.timesheet_repository.update_timesheet(Timesheet.from_dict(invalid_timesheet_data))
        self.assertEqual("Timesheet not found", response_no_userdata.message)
        self.assertEqual(False, response_no_userdata.is_successful)
        self.assertEqual(404, response_no_userdata.status_code)

        # Test update_timesheet method
        response = self.timesheet_repository.update_timesheet(Timesheet.from_dict(test_modified_timesheet_data))
        self.assertEqual("Timesheet updated successfully", response.message)
        self.assertEqual(True, response.is_successful)
        self.assertEqual(200, response.status_code)

        modified_timesheet = self.timesheet_repository.get_timesheet_by_id(test_modified_timesheet_data['_id'])
        self.assertEqual(test_modified_timesheet_data, modified_timesheet)

        # Reset the database to its original state
        response_reset = self.timesheet_repository.update_timesheet(Timesheet.from_dict(test_original_timesheet_data))
        self.assertEqual("Timesheet updated successfully", response_reset.message)
        self.assertEqual(True, response_reset.is_successful)
        self.assertEqual(200, response_reset.status_code)

    def test_set_timesheet_status(self):
        """
        Test the set_timesheet_status method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                               'username': 'testHiwi1',
                               'month': 5,
                               'year': 2024,
                               'status': 'Not Submitted',
                               'totalTime': 0.0,
                               'overtime': 0.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no timesheet data
        response_no_timeheet_data = self.timesheet_repository.set_timesheet_status(None, TimesheetStatus.COMPLETE)
        self.assertEqual("Please provide a timesheet ID and status to update the timesheet status.", response_no_timeheet_data.message)
        self.assertEqual(False, response_no_timeheet_data.is_successful)
        self.assertEqual(400, response_no_timeheet_data.status_code)

        # Test for invalid timesheet data
        response_invalid_timesheet_data = self.timesheet_repository.set_timesheet_status("666666666666666666666666", TimesheetStatus.COMPLETE)
        self.assertEqual("Timesheet not found", response_invalid_timesheet_data.message)
        self.assertEqual(False, response_invalid_timesheet_data.is_successful)
        self.assertEqual(404, response_invalid_timesheet_data.status_code)

        # Test set_timesheet_status method
        self.timesheet_repository.set_timesheet_status(str(test_timesheet_data['_id']), TimesheetStatus.COMPLETE)
        self.assertEqual(str(TimesheetStatus.COMPLETE),
                         self.timesheet_repository.get_timesheet_by_id(str(test_timesheet_data['_id']))['status'])
        self.timesheet_repository.set_timesheet_status(str(test_timesheet_data['_id']), TimesheetStatus.NOT_SUBMITTED)

    def test_create_timesheet_by_dict(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': None,
                               'username': 'testCreateUser',
                               'month': 4,
                               'year': 2024,
                               'status': 'Complete',
                               'totalTime': 1.0,
                               'overtime': 1.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 13, 23, 41, 45, 279000)}
        already_exists_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                                        'username': 'testHiwi1',
                                        'month': 5,
                                        'year': 2024,
                                        'status': 'Not Submitted',
                                        'totalTime': 0.0,
                                        'overtime': 0.0,
                                        'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no timesheet data
        response_no_timesheet_data = self.timesheet_repository.create_timesheet_by_dict(None)
        self.assertEqual("Please provide a timesheet to create.", response_no_timesheet_data.message)
        self.assertEqual(False, response_no_timesheet_data.is_successful)
        self.assertEqual(400, response_no_timesheet_data.status_code)

        # Test for timesheet already exists
        response_already_exists = self.timesheet_repository.create_timesheet_by_dict(already_exists_timesheet_data)
        self.assertEqual("Timesheet already exists", response_already_exists.message)
        self.assertEqual(False, response_already_exists.is_successful)
        self.assertEqual(409, response_already_exists.status_code)

        # Test create_timesheet_by_dict method
        result = self.timesheet_repository.create_timesheet_by_dict(test_timesheet_data)
        test_timesheet_data['_id'] = result.data['_id']
        self.assertEqual(test_timesheet_data, self.timesheet_repository.get_timesheet_by_id(str(result.data['_id'])))
        # Delete Timesheet and return database to its original state
        self.timesheet_repository.delete_timesheet(str(result.data['_id']))


    def test_create_timesheet(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': None,
                               'username': 'testCreateUser',
                               'month': 4,
                               'year': 2024,
                               'status': 'Complete',
                               'totalTime': 1.0,
                               'overtime': 1.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 13, 23, 41, 45, 279000)}
        already_exists_timesheet_data = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                                         'username': 'testHiwi1',
                                         'month': 5,
                                         'year': 2024,
                                         'status': 'Not Submitted',
                                         'totalTime': 0.0,
                                         'overtime': 0.0,
                                         'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}

        # Test for no timesheet data
        response_no_timesheet_data = self.timesheet_repository.create_timesheet(None)
        self.assertEqual("Please provide a timesheet to create.", response_no_timesheet_data.message)
        self.assertEqual(False, response_no_timesheet_data.is_successful)
        self.assertEqual(400, response_no_timesheet_data.status_code)

        # Test for timesheet already exists
        response_already_exists = self.timesheet_repository.create_timesheet(Timesheet.from_dict(already_exists_timesheet_data))
        self.assertEqual("Timesheet already exists", response_already_exists.message)
        self.assertEqual(False, response_already_exists.is_successful)
        self.assertEqual(409, response_already_exists.status_code)

        # Test create_timesheet method
        result = self.timesheet_repository.create_timesheet(Timesheet.from_dict(test_timesheet_data))
        test_timesheet_data['_id'] = result.data['_id']
        self.assertEqual(test_timesheet_data, self.timesheet_repository.get_timesheet_by_id(str(result.data['_id'])))
        # Delete Timesheet and return database to its original state
        self.timesheet_repository.delete_timesheet(str(result.data['_id']))

    def test_delete_timesheet(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': None,
                               'username': 'testCreateUser',
                               'month': 4,
                               'year': 2024,
                               'status': 'Complete',
                               'totalTime': 1.0,
                               'overtime': 1.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 13, 23, 41, 45, 279000)}

        # Test for no timesheet data
        response_no_timesheet_id = self.timesheet_repository.delete_timesheet(None)
        self.assertEqual("Please provide a timesheet ID to delete the timesheet.", response_no_timesheet_id.message)
        self.assertEqual(False, response_no_timesheet_id.is_successful)
        self.assertEqual(400, response_no_timesheet_id.status_code)

        result = self.timesheet_repository.create_timesheet(Timesheet.from_dict(test_timesheet_data))
        self.timesheet_repository.delete_timesheet(str(result.data['_id']))
        self.assertIsNone(self.timesheet_repository.get_timesheet_by_id(str(result.data['_id'])))

    if __name__ == '__main__':
        unittest.main()

