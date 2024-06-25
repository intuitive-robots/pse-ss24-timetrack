import unittest
import datetime

from bson import ObjectId

from model.repository.timesheet_repository import TimesheetRepository
from model.timesheet_status import TimesheetStatus


class TestSheetRepository(unittest.TestCase):

    def setUp(self):
        self.timesheet_repository = TimesheetRepository.get_instance()

    def test_get_timesheet_by_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': ObjectId('666c1331d28499aff172091c'),
                               'username': 'testHiWi',
                               'month': 3,
                               'year': 2022,
                               'status': 'Not Submitted',
                               'totalTime': 0,
                               'overtime': 0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 12, 17, 22, 32, 468000),
                               'timeEntryIds': [ObjectId('666a1ace21bc45a25b4263d8'),
                                                ObjectId('666c020f7a409003113fedf9'),
                                                ObjectId('666c022a7a409003113fedfb')]}
        self.assertEqual(test_timesheet_data, self.timesheet_repository.get_timesheet_by_id(str(test_timesheet_data['_id'])))

    def test_get_timesheet(self):
        """
        Test the get_timesheet method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': ObjectId('666c1331d28499aff172091c'),
                               'username': 'testHiWi',
                               'month': 3,
                               'year': 2022,
                               'status': 'Not Submitted',
                               'totalTime': 0,
                               'overtime': 0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 12, 17, 22, 32, 468000),
                               'timeEntryIds': [ObjectId('666a1ace21bc45a25b4263d8'),
                                                ObjectId('666c020f7a409003113fedf9'),
                                                ObjectId('666c022a7a409003113fedfb')]}
        self.assertEqual(test_timesheet_data, self.timesheet_repository.get_timesheet(test_timesheet_data['username'],
                                                                                      test_timesheet_data['month'],
                                                                                      test_timesheet_data['year']))

    #TODO: check if only most recent one is returned, in case there are multiple not complete timesheets (update database)
    def test_get_current_timesheet(self):
        """
        Test the get_current_timesheet method of the TimesheetRepository class.
        """
        print(self.timesheet_repository.get_timesheet_by_id('6669be2d8e45219d011d6e15'))
        test_timesheet_data = {'_id': ObjectId('6669be2d8e45219d011d6e15'),
                               'username': 'test1',
                               'month': 5,
                               'year': 2024,
                               'status': 'Not Submitted',
                               'totalTime': 0.0,
                               'overtime': 0.0,
                               'lastSignatureChange': datetime.datetime(2024, 6, 12, 17, 22, 32, 468000),
                               'timeEntryIds': [ObjectId('666c022a7a409003113fedfb'),
                                                ObjectId('666c9d816796c3856a1c5bde'),
                                                ObjectId('666ca0f9036a5486bc54ad98'),
                                                ObjectId('666ca119036a5486bc54ad99')]}
        self.assertEqual(test_timesheet_data, self.timesheet_repository.get_current_timesheet(test_timesheet_data['username']))

    #TODO: change get_timesheet_by_time_period, since it assumes that a date type is stored in the database
    def test_get_timesheet_by_time_period(self):
        test_timesheet = [{'_id': ObjectId('666a161bb46b51b1f8526b85'),
                           'username': 'test1',
                           'month': 4,
                           'year': 2024,
                           'status': 'Complete',
                           'totalTime': 0.0,
                           'overtime': 0.0,
                           'lastSignatureChange': datetime.datetime(2024, 6, 12, 23, 41, 45, 279000),
                           'timeEntryIds': []}]

        self.assertEqual(test_timesheet, self.timesheet_repository.get_timesheet_by_time_period('test1',
                                                                                                datetime.datetime(2022, 6, 12, 0, 0, 0, 0),
                                                                                                datetime.datetime(2024, 4, 12, 0, 0, 0, 0)))

    def test_get_timesheets(self):
        print(self.timesheet_repository.get_timesheets())
        test_timesheets_data = [{'_id': ObjectId('6669be2d8e45219d011d6e15'), 'username': 'test1', 'month': 5, 'year': 2024,
                 'status': 'Not Submitted', 'totalTime': 0.0, 'overtime': 0.0,
                 'lastSignatureChange': datetime.datetime(2024, 6, 12, 17, 22, 32, 468000),
                 'timeEntryIds': [ObjectId('666c022a7a409003113fedfb'), ObjectId('666c9d816796c3856a1c5bde'),
                                  ObjectId('666ca0f9036a5486bc54ad98'), ObjectId('666ca119036a5486bc54ad99')]},
                {'_id': ObjectId('666a161bb46b51b1f8526b85'), 'username': 'test1', 'month': 4, 'year': 2024,
                 'status': 'Complete', 'totalTime': 0.0, 'overtime': 0.0,
                 'lastSignatureChange': datetime.datetime(2024, 6, 12, 23, 41, 45, 279000), 'timeEntryIds': []},
                {'_id': ObjectId('666b66b37435ad8c9e23304a'), 'username': 'test123', 'month': 8, 'year': 2008,
                 'status': 'Not Submitted', 'totalTime': 0.0, 'overtime': 0.0,
                 'lastSignatureChange': datetime.datetime(2024, 6, 13, 23, 35, 24, 216000), 'timeEntryIds': []},
                {'_id': ObjectId('666c1331d28499aff172091c'), 'username': 'testHiWi', 'month': 3, 'year': 2022,
                 'status': 'Not Submitted', 'totalTime': 0, 'overtime': 0,
                 'lastSignatureChange': datetime.datetime(2024, 6, 12, 17, 22, 32, 468000),
                 'timeEntryIds': [ObjectId('666a1ace21bc45a25b4263d8'), ObjectId('666c020f7a409003113fedf9'),
                                  ObjectId('666c022a7a409003113fedfb')]}]
        self.assertEqual(test_timesheets_data, self.timesheet_repository.get_timesheets())

    def test_get_timesheet_by_status(self):
        """
        Test the get_timesheet_by_status method of the TimesheetRepository class.
        """
        test_timesheets = [{'_id': ObjectId('6669be2d8e45219d011d6e15'), 'username': 'test1', 'month': 5, 'year': 2024,
                            'status': 'Not Submitted', 'totalTime': 0.0, 'overtime': 0.0,
                            'lastSignatureChange': datetime.datetime(2024, 6, 12, 17, 22, 32, 468000),
                            'timeEntryIds': [ObjectId('666c022a7a409003113fedfb'), ObjectId('666c9d816796c3856a1c5bde'),
                                             ObjectId('666ca0f9036a5486bc54ad98'),
                                             ObjectId('666ca119036a5486bc54ad99')]},
                           {'_id': ObjectId('666b66b37435ad8c9e23304a'), 'username': 'test123', 'month': 8,
                            'year': 2008, 'status': 'Not Submitted', 'totalTime': 0.0, 'overtime': 0.0,
                            'lastSignatureChange': datetime.datetime(2024, 6, 13, 23, 35, 24, 216000),
                            'timeEntryIds': []},
                           {'_id': ObjectId('666c1331d28499aff172091c'), 'username': 'testHiWi', 'month': 3,
                            'year': 2022, 'status': 'Not Submitted', 'totalTime': 0, 'overtime': 0,
                            'lastSignatureChange': datetime.datetime(2024, 6, 12, 17, 22, 32, 468000),
                            'timeEntryIds': [ObjectId('666a1ace21bc45a25b4263d8'), ObjectId('666c020f7a409003113fedf9'),
                                             ObjectId('666c022a7a409003113fedfb')]}]

        self.assertEqual(test_timesheets, self.timesheet_repository.get_timesheet_by_status(TimesheetStatus.NOT_SUBMITTED))
        self.assertEqual([], self.timesheet_repository.get_timesheet_by_status(TimesheetStatus.REVISION))

    def test_get_timesheet_id(self):
        """
        Test the get_timesheet_id method of the TimesheetRepository class.
        """
        test_timesheet = {'_id': ObjectId('666a161bb46b51b1f8526b85'),
                          'username': 'test1',
                          'month': 4,
                          'year': 2024,
                          'status': 'Complete',
                          'totalTime': 0.0,
                          'overtime': 0.0,
                          'lastSignatureChange': datetime.datetime(2024, 6, 12, 23, 41, 45, 279000),
                          'timeEntryIds': []}
        self.assertEqual(test_timesheet['_id'], self.timesheet_repository.get_timesheet_id(test_timesheet['username'],
                                                                                           test_timesheet['month'],
                                                                                           test_timesheet['year']))

    def test_get_timesheets_by_username_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetRepository class.
        """


    def test_update_timesheet_by_dict(self):
        """
        Test the update_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_original_timesheet = {'_id': ObjectId('666a161bb46b51b1f8526b85'),
                                   'username': 'test1',
                                   'month': 4,
                                   'year': 2024,
                                   'status': 'Complete',
                                   'totalTime': 0.0,
                                   'overtime': 0.0,
                                   'lastSignatureChange': datetime.datetime(2024, 6, 12, 23, 41, 45, 279000),
                                   'timeEntryIds': []}
        test_modified_timesheet = {'_id': ObjectId('666a161bb46b51b1f8526b85'),
                                   'username': 'test1',
                                   'month': 4,
                                   'year': 2024,
                                   'status': 'Complete',
                                   'totalTime': 1.0,
                                   'overtime': 1.0,
                                   'lastSignatureChange': datetime.datetime(2024, 6, 13, 23, 41, 45, 279000),
                                   'timeEntryIds': []}
        self.timesheet_repository.update_timesheet_by_dict(test_modified_timesheet)
        self.assertEqual(test_modified_timesheet, self.timesheet_repository.get_timesheet_by_id('666a161bb46b51b1f8526b85'))
        self.timesheet_repository.update_timesheet_by_dict(test_original_timesheet)

    #TODO: test_update_timesheet (by Timesheet)?
    def test_set_timesheet_status(self):
        """
        Test the set_timesheet_status method of the TimesheetRepository class.
        """
        print(self.timesheet_repository.get_timesheet_by_id('6679ca2935df0d8f7202c5fa'))
        test_timesheet = {'_id': ObjectId('6679ca2935df0d8f7202c5fa'),
                          'username': 'testHiWi',
                          'month': 5,
                          'year': 2024,
                          'status': 'Not Submitted',
                          'totalTime': 0.0,
                          'overtime': 0.0,
                          'lastSignatureChange': datetime.datetime(2024, 6, 24, 21, 22, 35, 855000),
                          'timeEntryIds': [ObjectId('6679ce1b327b11ba6160cc1a')]}
        self.timesheet_repository.set_timesheet_status(str(test_timesheet['_id']), TimesheetStatus.COMPLETE)
        self.assertEqual(str(TimesheetStatus.COMPLETE), self.timesheet_repository.get_timesheet_by_id(str(test_timesheet['_id']))['status'])
        self.timesheet_repository.set_timesheet_status(str(test_timesheet['_id']), TimesheetStatus.NOT_SUBMITTED)

    def test_create_timesheet_by_dict(self):
        """
        Test the create_timesheet_by_dict method of the TimesheetRepository class.
        """
        test_timesheet_data = {'_id': None,
                                   'username': 'test1',
                                   'month': 4,
                                   'year': 2024,
                                   'status': 'Complete',
                                   'totalTime': 1.0,
                                   'overtime': 1.0,
                                   'lastSignatureChange': datetime.datetime(2024, 6, 13, 23, 41, 45, 279000),
                                   'timeEntryIds': []}
        result = self.timesheet_repository.create_timesheet_by_dict(test_timesheet_data)
        test_timesheet_data['_id'] = result.data['_id']
        self.assertEqual(test_timesheet_data, self.timesheet_repository.get_timesheet_by_id(str(result.data['_id'])))
        self.timesheet_repository.delete_timesheet(str(test_timesheet_data['_id']))

    if __name__ == '__main__':
        unittest.main()
