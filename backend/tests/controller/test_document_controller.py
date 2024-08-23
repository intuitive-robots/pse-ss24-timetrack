import unittest
from datetime import datetime, timezone

from app import app
from db import initialize_db
from model.repository.user_repository import UserRepository
from model.user.hiwi import Hiwi
from model.user.user import User
from service.timesheet_service import TimesheetService
from utils.security_utils import SecurityUtils


class TestDocumentController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.app = app
        cls.admin_user_data = {
            "username": "AdminDocumentController",
            "role": "Admin",
            "passwordHash": SecurityUtils.hash_password("test_password"),
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Admin",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None,
            "isArchived": False,
            "slackId": None
        }
        admin_user = User.from_dict(cls.admin_user_data)
        user_repository = UserRepository.get_instance()
        user_repository.create_user(admin_user)
        cls.hiwi_user_data = {
            "username": "HiwiDocumentController",
            "passwordHash": SecurityUtils.hash_password("test_password"),
            "role": "Hiwi",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "LastName",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "contractInfo": {
                "hourlyWage": 12.40,
                "workingHours": 80
            },
            "supervisor": "testSupervisorUserService",
            "slackId": None,
            "accountCreation": None,
            "lastLogin": None
        }
        hiwi_user = Hiwi.from_dict(cls.hiwi_user_data)
        user_repository.create_user(hiwi_user)
        cls.timesheet_service = TimesheetService()
        current_month = datetime.now(timezone.utc).month
        current_year = datetime.now(timezone.utc).year
        cls.timesheet_service.ensure_timesheet_exists("HiwiDocumentController", current_month , current_year)

    @classmethod
    def tearDownClass(cls):
        db = initialize_db()
        db.timesheets.delete_many({"username": "HiwiDocumentController"})
        db.users.delete_many({"username": "HiwiDocumentController"})
        db.users.delete_many({"username": "AdminDocumentController"})



    def _authenticate(self, username, password):
        """
        Authenticate the user.
        """
        user = {
            "username": username,
            "password": password
        }
        response = self.client.post('/user/login', json=user)
        return response.json['accessToken']

    def test_generate_document_no_username(self):
        """
        Test the generate_document method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")

        response = self.client.get('/document/generateDocument?month=6&year=2024',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual("No username provided", response.json)

    def test_generate_document_no_month(self):
        """
        Test the generate_document method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")

        response = self.client.get('/document/generateDocument?year=2024&username=HiwiDocumentController',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual("No month provided", response.json)

    def test_generate_document_no_year(self):
        """
        Test the generate_document method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")

        response = self.client.get('/document/generateDocument?month=6&username=HiwiDocumentController',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual("No year provided", response.json)


    def test_generate_document(self):
        """
        Test the generate_document method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")

        response = self.client.get('/document/generateDocument?month=6&year=2024&username=HiwiDocumentController',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(response.data)

    def test_generate_multiple_documents_no_usernames(self):
        """
        Test the generate_multiple_documents method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")

        response = self.client.get('/document/generateMultipleDocuments?month=6&year=2024',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Missing required fields", response.json)

    def test_generate_multiple_documents_no_month(self):
        """
        Test the generate_multiple_documents method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")

        response = self.client.get('/document/generateMultipleDocuments?year=2024&usernames=testHiwi1',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Missing required fields", response.json)

    def test_generate_multiple_documents_no_year(self):
        """
        Test the generate_multiple_documents method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")

        response = self.client.get('/document/generateMultipleDocuments?month=6&usernames=testHiwi1',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual("Missing required fields", response.json)

    def test_generate_multiple_documents_ids(self):
        """
        Test the generate_multiple_documents method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")

        timesheet_id = self.timesheet_service.get_timesheet_id("HiwiDocumentController", 6, 2024)
        response = self.client.get(f'/document/generateMultipleDocuments?month=6&year=2024&timesheetIds={timesheet_id}',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(response.data)

    def test_generate_multiple_documents(self):
        """
        Test the generate_multiple_documents method of the DocumentController class.
        """
        access_token = self._authenticate("HiwiDocumentController", "test_password")


        responseIds = self.client.get(
            '/document/generateMultipleDocuments?timesheetIds=667bd050cf0aa6181e9c8dd9&timesheetIds=667bd14ecf0aa6181e9c8dda',
            headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(responseIds.data)


        responseDates = self.client.get(
            '/document/generateMultipleDocuments?username=testHiwi1&startDate=01-03-24&endDate=01-04-24',
            headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(responseDates.data)

        responseError = self.client.get(
            '/document/generateMultipleDocuments?username=testHiwi1',
            headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(responseError.status_code, 400)
