import os
import unittest
from datetime import datetime

from app import app
from controller.user_controller import UserController
from model.file.FileType import FileType
from model.repository.timesheet_repository import TimesheetRepository
from model.repository.user_repository import UserRepository
from model.timesheet_status import TimesheetStatus
from model.user.user import User
from service.document.document_service import DocumentService
from service.file_service import FileService
from service.time_entry_service import TimeEntryService
from service.timesheet_service import TimesheetService
from service.user_service import UserService
from utils.security_utils import SecurityUtils


class TestDocumentService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document_service = DocumentService()
        cls.app = app
        cls.client = app.test_client()
        cls.user_service = UserService()
        cls.user_controller = UserController()
        cls.file_service = FileService()
        cls.timesheet_service = TimesheetService()
        cls.timesheet_repository = TimesheetRepository.get_instance()
        cls.time_entry_service = TimeEntryService()
        cls.test_admin_user_data = {
            "username": "AdminDocService",
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
        admin_user = User.from_dict(cls.test_admin_user_data)
        cls.user_repository = UserRepository.get_instance()
        cls.user_repository.create_user(admin_user)

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            access_token = cls._authenticate( cls,'AdminDocService', 'test_password')
            with cls.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                cls.user_service.delete_user("testHiwiDocService")
                cls.user_service.delete_user("testSupervisorDocService")
                cls.user_service.delete_user("testAdminDocService")
                cls.file_service.delete_image("testHiwiDocService", FileType.SIGNATURE)
                cls.user_repository.delete_user("AdminDocService")

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

    def upload_signature(self, username):
        access_token = self._authenticate(username, "test_password")
        file_path = "../resources/testProfilePic.jpg"
        if not os.path.exists(file_path):
            file_path = "tests/resources/testProfilePic.jpg"
        file = open(file_path, "rb")
        response = self.client.post(f'/user/uploadFile?username={username}&fileType=Signature',
                                    data={"file": file},
                                    headers={"Authorization": f"Bearer {access_token}"})
    def tearDown(self):
        with self.app.app_context():
            access_token = self._authenticate('testHiwiDocService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.user_service.delete_user("testHiwiDocService")
                self.user_service.delete_user("testSupervisorDocService")
                self.user_service.delete_user("testAdminDocService")
                self.file_service.delete_image("testHiwiDocService", FileType.SIGNATURE)
                self.file_service.delete_image("testSupervisorDocService", FileType.SIGNATURE)
                self.timesheet_service.delete_timesheets_by_username("testHiwiDocService")
    def setUp(self):
        self.test_admin_user_data = {
            "username": "testAdminDocService",
            "password": "test_password",
            "role": "Admin",
            "personalInfo": {
                "firstName": "Paul",
                "lastName": "Admin",
                "email": "test@gmail.com",
                "personalNumber": "6981211",
                "instituteName": "Info Institute"
            },
            "lastLogin": None,
            "accountCreation": None,
            "slackId": None
        }
        self.test_supervisor_user_data = {
            "username": "testSupervisorDocService",
            "role": "Supervisor",
            "password": "test_password",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Supervisor",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None,
            "slackId": None
        }
        self.test_hiwi_user_data = {
            "username": "testHiwiDocService",
            "password": "test_password",
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
            "supervisor": "testSupervisorDocService",
            "slackId": None,
            "accountCreation": None,
            "lastLogin": None
        }
        self.user_service.create_user(self.test_supervisor_user_data)
        self.upload_signature("testSupervisorDocService")
        creation_result = self.user_service.create_user(self.test_hiwi_user_data)
        with self.app.app_context():
            access_token = self._authenticate('testHiwiDocService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                result = self.upload_signature("testHiwiDocService")
                self.user_service.create_user(self.test_admin_user_data)
                self.current_month = datetime.now().month
                self.current_year = datetime.now().year
                self.timesheet_service.ensure_timesheet_exists("testHiwiDocService", self.current_month, self.current_year)
                self.timesheet = self.timesheet_service.get_timesheet("testHiwiDocService", self.current_month, self.current_year).data
                self.timesheet.status = TimesheetStatus.COMPLETE
                self.timesheet_repository.update_timesheet(self.timesheet)
                self.test_time_entry_data = {'timesheetId': self.timesheet.timesheet_id,
                                             'startTime': datetime(self.current_year, self.current_month, 1, 8, 0, 0, 0),
                                             'endTime': datetime(self.current_year, self.current_month, 1, 16, 0),
                                             'entryType': 'Work Entry',
                                             'breakTime': 60,
                                             'activity': 'timeEntryServiceActivitiy',
                                             'activityType': 'Projektbesprechung',
                                             'projectName': 'timeEntryServiceTest'}
                self.time_entry_service.create_work_entry(self.test_time_entry_data, "testHiwiDocService")


    def test_generate_document(self):
        """
        Test the generate_document method of the DocumentService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiDocService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                generate_document_result = self.document_service.generate_document(self.current_month, self.current_year, "testHiwiDocService", "testHiwiDocService")
                self.assertTrue(generate_document_result.is_successful)
                self.assertEqual(generate_document_result.status_code, 200)
                self.assertIsNotNone(generate_document_result.message)

    def test_generate_multiple_documents(self):
        """
        Test the generate_multiple_documents method of the DocumentService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiDocService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                generate_document_result = self.document_service.generate_multiple_documents(["testHiwiDocService"], self.current_month, self.current_year, "testHiwiDocService")
                self.assertTrue(generate_document_result.is_successful)
                self.assertEqual(generate_document_result.status_code, 200)
                self.assertIsNotNone(generate_document_result.message)

    def test_generate_multiple_documents_by_ids(self):
        """
        Test the generate_multiple_documents_by_ids method of the DocumentService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiDocService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                generate_document_result = self.document_service.generate_multiple_documents_by_id([self.timesheet.timesheet_id], "testHiwiDocService")
                self.assertTrue(generate_document_result.is_successful)
                self.assertEqual(generate_document_result.status_code, 200)
                self.assertIsNotNone(generate_document_result.message)
    def test_generate_multiple_documents_by_date_range(self):
        """
        Test the generate_multiple_documents_by_date_range method of the DocumentService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiDocService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                start_date = datetime(self.current_year, self.current_month, 1)
                end_date = datetime(self.current_year, self.current_month, 1)
                generate_document_result = self.document_service.generate_document_in_date_range( start_date, end_date,
                                                                                                  "testHiwiDocService", "testHiwiDocService")
                self.assertTrue(generate_document_result.is_successful)
                self.assertEqual(generate_document_result.status_code, 200)
                self.assertIsNotNone(generate_document_result.message)