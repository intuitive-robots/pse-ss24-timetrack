import datetime
import unittest
from app import app
from model.repository.time_entry_repository import TimeEntryRepository
from service.time_entry_service import TimeEntryService


class TestTimeEntryController(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.time_entry_service = TimeEntryService()
        self.app = app
        self.time_entry_repository = TimeEntryRepository.get_instance()

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
        test_time_entry_data = {
            'startTime': '2024-05-22T10:00:00',
            'endTime': '2024-05-22T12:00:00',
            'breakTime': 30,
            'activity': 'testCreateWorkEntry of Hiwi1',
            'projectName': 'timeEntryControllerTesting'
        }
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                response = self.client.post('/timeEntry/createWorkEntry', json=test_time_entry_data, headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 200)
                work_entry = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 5,22), 'testHiwi1')[0]
                self.assertIsNotNone(work_entry)
                # Reset database to original state
                self.time_entry_service.delete_time_entry(work_entry['_id'])

    def test_create_vacation_entry(self):
        """
        Test the create_vacation_entry method of the TimeEntryController class.
        """
        test_time_entry_data = {

            'startTime': '2024-05-22T08:20:30.656',
            'endTime': '2024-05-22T12:00:00'
        }
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                response = self.client.post('/timeEntry/createVacationEntry', json=test_time_entry_data,
                                            headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 200)
                vacation_entry = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 5, 22), 'testHiwi1')[0]
                self.assertIsNotNone(vacation_entry)
                # Reset database to original state
                self.time_entry_service.delete_time_entry(vacation_entry['_id'])

    def test_update_time_entry(self):
        """
        Test the update_time_entry method of the TimeEntryController class.
        """
        access_token = self.authenticate("testHiwi1", "test_password")
        test_time_entry_original_data = {
            "_id": "666c020f7a409003113fedf9",
            "activity": "timeEntry1 of Hiwi1",
            "projectName": "testing"
        }
        test_time_entry_modified_data = {
            "_id": "666c020f7a409003113fedf9",
            "activity": "Updated activity",
            "projectName": "TimeEntryController Testing"
        }
        response = self.client.post('/timeEntry/updateTimeEntry', json=test_time_entry_modified_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        time_entry = self.time_entry_repository.get_time_entry_by_id(test_time_entry_original_data["_id"])
        self.assertEqual(test_time_entry_modified_data["activity"], time_entry["activity"])
        self.assertEqual(test_time_entry_modified_data["projectName"], time_entry["projectName"])
        # Reset database to original state
        resetResponse = self.client.post('/timeEntry/updateTimeEntry', json=test_time_entry_original_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(resetResponse.status_code, 200)

    def test_delete_time_entry(self):
        """
        `Test the delete_time_entry method of the TimeEntryController class.
        """
        access_token = self.authenticate("testHiwi1", "test_password")
        test_time_entry_data = {
            "timesheetId": "6679ca2935df0d8f7202c5fa",
            "startTime": "2024-05-22T09:20:30.656Z",
            "endTime": "2024-05-22T12:00:00Z",
            "breakTime": 30,
            "activity": "testDeleteTimeEntry of Hiwi1",
            "projectName": "TimeEntryController Testing"
        }
        create_result = self.time_entry_service.create_work_entry(test_time_entry_data, "testHiwi1")
        self.assertTrue(create_result.is_successful)
        time_entry = self.time_entry_repository.get_time_entries_by_date(datetime.date(2024, 5, 22), 'testHiwi1', )[0]
        response = self.client.post('/timeEntry/deleteTimeEntry', json={"timeEntryId": str(time_entry["_id"])},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.time_entry_repository.get_time_entry_by_id((time_entry["_id"])))

    def test_get_entries_by_timesheet_id(self):
        """
        Test the get_entries_by_timesheet_id method of the TimeEntryController class.
        """
        access_token = self.authenticate("testHiwi1", "test_password")
        response = self.client.get('/timeEntry/getEntriesByTimesheetId?timesheetId=6679ca2935df0d8f7202c5fa',
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.time_entry_repository.get_time_entries_by_timesheet_id("6679ca2935df0d8f7202c5fa")), len(response.json))
        
    if __name__ == '__main__':
        unittest.main()