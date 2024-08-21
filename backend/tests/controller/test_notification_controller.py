import unittest

from app import app
from db import initialize_db
from model.notification.message_type import MessageType
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from model.repository.user_repository import UserRepository
from model.user.hiwi import Hiwi
from model.user.user import User
from service.notification_service import NotificationService
from utils.security_utils import SecurityUtils


class TestNotificationController(unittest.TestCase):

    def setUp(self):
        self.notification = NotificationMessage(
            sender="AdminNotificationController",
            receiver="HiwiNotificationController",
            message="Testing",
            message_type=MessageType.REMINDER,
        )
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = app.test_client()
        cls.db = initialize_db()
        cls.notification_repository = NotificationRepository.get_instance()
        cls.notification_service = NotificationService()
        slack_user_id = "U07BENARPHB"  # Replace this with your own slack user id

        cls.admin_user_data = {
            "username": "AdminNotificationController",
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
            "slackId": slack_user_id
        }
        admin_user = User.from_dict(cls.admin_user_data)
        user_repository = UserRepository.get_instance()
        user_repository.create_user(admin_user)
        cls.hiwi_user_data = {
            "username": "HiwiNotificationController",
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
            "slackId": slack_user_id,
            "accountCreation": None,
            "lastLogin": None
        }
        hiwi_user = Hiwi.from_dict(cls.hiwi_user_data)
        user_repository.create_user(hiwi_user)


    def tearDown(self):
        self.db.notifications.delete_many({"message": "Testing"})

    @classmethod
    def tearDownClass(cls):
        db = initialize_db()
        db.users.delete_many({"username": "HiwiNotificationController"})
        db.users.delete_many({"username": "AdminNotificationController"})

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

    def test_does_unread_messages_exist(self):
        with self.app.app_context():
            access_token = self._authenticate('HiwiNotificationController', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):

                creation_result = self.notification_repository.create_notification(self.notification)
                response = self.client.get('/notification/doesUnreadMessageExist',
                                           headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(True, response.json)
    def test_does_unread_messages_exist_no_unread_messages(self):
        with self.app.app_context():
            access_token = self._authenticate('HiwiNotificationController', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                response = self.client.get('/notification/doesUnreadMessageExist',
                                           headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(False, response.json)


    def test_read_all_notifications(self):
        with self.app.app_context():
            access_token = self._authenticate('HiwiNotificationController', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):

                creation_result = self.notification_repository.create_notification(self.notification)
                response = self.client.get('/notification/readAll',
                                           headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 200)
                does_unread_message_exist_response = self.client.get('/notification/doesUnreadMessageExist',
                                                                    headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(does_unread_message_exist_response.status_code, 200)
                self.assertEqual(False, does_unread_message_exist_response.json)

    def test_delete_notification(self):
        with self.app.app_context():
            access_token = self._authenticate('HiwiNotificationController', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):

                creation_result = self.notification_repository.create_notification(self.notification)
                response = self.client.delete('/notification/delete?id=' + creation_result.data.get("id"),
                                              headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual("Notification deleted successfully", response.json)
                response = self.client.delete('/notification/delete?id=' + creation_result.data.get("id"),
                                              headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 404)
                self.assertEqual("Notification not found", response.json)
