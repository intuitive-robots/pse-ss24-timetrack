import datetime
import unittest
from app import app
from db import initialize_db
from model.repository.time_entry_repository import TimeEntryRepository
from service.time_entry_service import TimeEntryService
from service.timesheet_service import TimesheetService
from service.user_service import UserService


class TestTimeEntryController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = initialize_db()
        cls.client = app.test_client()
        cls.time_entry_service = TimeEntryService()
        cls.user_service = UserService()
        cls.timesheet_service = TimesheetService()
        cls.app = app
        cls.time_entry_repository = TimeEntryRepository.get_instance()

        cls.test_timesheet_supervisor = {'username': 'testSupervisorTimeEntryController',
                                         'password': 'testPassword',
                                         'personalInfo': {
                                             'firstName': 'Test',
                                             'lastName': 'Supervisor',
                                             'email': 'test@gmail.com',
                                             'personalNumber': '1234567890',
                                             'instituteName': 'Test Institute'
                                         },
                                         'role': 'Supervisor',
                                         'accountCreation': datetime.datetime(2023, 6, 1, 8, 0, 0, 0),
                                         'lastLogin': datetime.datetime(2024, 6, 1, 8, 0, 0, 0),
                                         'slackId': 'testSlackId',
                                         'isArchived': False
                                         }
        cls.test_timesheet_hiwi = {'username': 'testHiwiTimeEntryController',
                                   'password': 'testPassword',
                                   'personalInfo': {
                                       'firstName': 'Test',
                                       'lastName': 'Hiwi',
                                       'email': 'test@gmail.com',
                                       'personalNumber': '1234567890',
                                       'instituteName': 'Test Institute'
                                   },
                                   'role': 'Hiwi',
                                   'accountCreation': datetime.datetime(2023, 6, 1, 8, 0, 0, 0),
                                   'lastLogin': datetime.datetime(2024, 6, 1, 8, 0, 0, 0),
                                   'slackId': 'testSlackId',
                                   'isArchived': False,
                                   'supervisor': 'testSupervisorTimeEntryController',
                                   'contractInfo': {'hourlyWage': 15,
                                                    'workingHours': 80,
                                                    'vacationMinutes': 0,
                                                    'overtimeMinutes': 0}
                                   }

        cls.test_june_3_time_entry_data = {'startTime': '2024-06-03T10:00:00Z',
                                           'endTime': '2024-06-03T20:00:00Z',
                                           'breakTime': 60,
                                           'activity': 'TimeEntryControllerActivitiy',
                                           'activityType': 'Projektbesprechung',
                                           'projectName': 'timesheetServiceTest'}
        cls.test_june_4_time_entry_data = {'startTime': '2024-06-04T10:00:00Z',
                                           'endTime': '2024-06-04T20:00:00Z',
                                           'breakTime': 60,
                                           'activity': 'timeEntryControllerActivitiy',
                                           'activityType': 'Projektbesprechung',
                                           'projectName': 'TimeEntryControllerTest'}
        
    def setUp(self):
        self.user_service.create_user(self.test_timesheet_supervisor.copy())
        self.user_service.create_user(self.test_timesheet_hiwi.copy())
        self.timesheet_service.ensure_timesheet_exists('testHiwiTimeEntryController', 6, 2024)
        self.time_entry_service.create_work_entry(self.test_june_3_time_entry_data.copy(), 'testHiwiTimeEntryController')
        self.time_entry_service.create_work_entry(self.test_june_4_time_entry_data.copy(), 'testHiwiTimeEntryController')

    def tearDown(self):
        timesheet_id = self.timesheet_service.get_timesheet_id('testHiwiTimeEntryController', 6, 2024).data
        self.db.users.delete_many({'username': 'testHiwiTimeEntryController'})
        self.db.users.delete_many({'username': 'testSupervisorTimeEntryController'})
        self.db.timesheets.delete_many({'username': 'testHiwiTimeEntryController'})
        self.db.timeEntries.delete_many({'timesheetId': str(timesheet_id)})
        self.db.notifications.delete_many({'receiver': 'testHiwiTimeEntryController'})
        self.db.notifications.delete_many({'receiver': 'testSupervisorTimeEntryController'})

        files_id = self.db.fs.files.find_one({'filename': 'testHiwiTimeEntryController_Signature'})
        if files_id:
            files_id = files_id['_id']
        else:
            files_id = None
        self.db.file_metadata.delete_many({'username': 'testHiwiTimeEntryController'})
        self.db.fs.files.delete_many({'filename': 'testHiwiTimeEntryController_Signature'})
        self.db.fs.chunks.delete_many({'files_id': files_id})

        files_id2 = self.db.fs.files.find_one({'filename': 'testSupervisorTimeEntryController'})
        if files_id2:
            files_id2 = files_id2['_id']
        else:
            files_id2 = None
        self.db.file_metadata.delete_many({'username': 'testSupervisorTimeEntryController'})
        self.db.fs.files.delete_many({'filename': 'testSupervisorTimeEntryController_Signature'})
        self.db.fs.chunks.delete_many({'files_id': files_id2})
        

    def authenticate(self,username, password):
        """
        Helper method to authenticate a user.
        """
        user = {
            "username": username,
            "password": password
        }
        response = self.client.post('/user/login', json=user)
        return response.json['accessToken']

    def test_create_work_entry(self):
        """
        Test the create_work_entry method of the TimeEntryController class.
        """
        test_time_entry_data = {'startTime': '2024-06-20T10:00:00Z',
                                'endTime': '2024-06-20T20:00:00Z',
                                'breakTime': 60,
                                'activity': 'timeEntryControllerActivitiy',
                                'activityType': 'Projektbesprechung',
                                'projectName': 'TimeEntryControllerTest'}
        access_token = self.authenticate('testHiwiTimeEntryController', 'testPassword')
        response = self.client.post('/timeEntry/createWorkEntry', json=test_time_entry_data, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        work_entry = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 6,20), 'testHiwiTimeEntryController')[0]
        self.assertIsNotNone(work_entry)

    def test_create_vacation_entry(self):
        """
        Test the create_vacation_entry method of the TimeEntryController class.
        """
        test_time_entry_data = {
            'startTime': '2024-06-20T08:00:00',
            'endTime': '2024-06-20T12:00:00'
        }
        access_token = self.authenticate('testHiwiTimeEntryController', 'testPassword')
        response = self.client.post('/timeEntry/createVacationEntry', json=test_time_entry_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        vacation_entry = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 6, 20), 'testHiwiTimeEntryController')[0]
        self.assertIsNotNone(vacation_entry)

    def test_update_time_entry(self):
        """
        Test the update_time_entry method of the TimeEntryController class.
        """
        access_token = self.authenticate('testHiwiTimeEntryController', 'testPassword')
        test_time_entry_modified_data = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 6, 3), 'testHiwiTimeEntryController')[0]
        test_time_entry_modified_data['activity'] = 'UpdatedActivity'
        test_time_entry_modified_data['_id'] = str(test_time_entry_modified_data['_id'])
        test_time_entry_modified_data.pop('startTime')
        test_time_entry_modified_data.pop('endTime')

        response = self.client.post('/timeEntry/updateTimeEntry', json=test_time_entry_modified_data,
                                    headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        time_entry = self.time_entry_repository.get_time_entry_by_id(test_time_entry_modified_data['_id'])
        self.assertEqual(test_time_entry_modified_data['activity'], time_entry['activity'])
        self.assertEqual(test_time_entry_modified_data['projectName'], time_entry['projectName'])

    def test_delete_time_entry(self):
        """
        `Test the delete_time_entry method of the TimeEntryController class.
        """
        access_token = self.authenticate("testHiwiTimeEntryController", "testPassword")

        time_entry = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 6, 3),
                                                                         'testHiwiTimeEntryController')[0]
        response = self.client.post('/timeEntry/deleteTimeEntry', json={"timeEntryId": str(time_entry["_id"])},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.time_entry_repository.get_time_entry_by_id((time_entry["_id"])))

    def test_get_entries_by_timesheet_id(self):
        """
        Test the get_entries_by_timesheet_id method of the TimeEntryController class.
        """
        access_token = self.authenticate("testHiwiTimeEntryController", "testPassword")
        timesheet_id = self.timesheet_service.get_timesheet_id("testHiwiTimeEntryController", 6, 2024).data
        response = self.client.get(f'/timeEntry/getEntriesByTimesheetId?timesheetId={timesheet_id}',
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.json))
        
    if __name__ == '__main__':
        unittest.main()
