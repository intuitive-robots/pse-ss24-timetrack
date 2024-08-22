import unittest

from bson import ObjectId

from app import app
from db import initialize_db
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from model.repository.user_repository import UserRepository
from model.user.hiwi import Hiwi
from model.user.user import User
from service.notification_service import NotificationService
from utils.security_utils import SecurityUtils


class TestNotificationService(unittest.TestCase):
    """
    Test class for the NotificationService.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment.
        """
        cls.app = app
        cls.client = app.test_client()
        cls.db = initialize_db()
        cls.notification_repository = NotificationRepository.get_instance()
        cls.notification_service = NotificationService()
        slack_user_id = "U07BENARPHB"  # Replace this with your own slack user id
        cls.user_repository = UserRepository().get_instance()

        cls.admin_user_data = {
            "username": "AdminUserService",
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
        cls.user_repository.create_user(admin_user)

        cls.hiwi_user_data = {
            "username": "HiwiUserService",
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
        cls.user_repository.create_user(hiwi_user)

    def setUp(self):
        self.notification_data = {
            "receiver": "HiwiUserService",
            "sender": "AdminUserService",
            "message": "Test Notification Service",
            "message_type": "Reminder",
            "message_data": "Testing"
        }

    @classmethod
    def tearDownClass(cls):
        """
        Clean up the database after
        """
        cls.user_repository.delete_user("AdminUserService")
        cls.user_repository.delete_user("HiwiUserService")

    def tearDown(self):
        """
        Clean up the database after
        """
        self.db.notifications.delete_many({"messageData": "Testing"})

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


    def test_send_notification_system(self):
        """
        Test sending a notification with the sender as System.
        """
        with self.app.app_context():
            access_token = self._authenticate('HiwiUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification_data = self.notification_data
                notification_data["sender"] = "system"
                result = self.notification_service.send_notification(notification_data)
                self.assertTrue(result.is_successful)
                self.assertEqual(result.status_code, 200)
                self.notification_repository.delete_notification_by_id(result.data.message_id)


    def test_send_notification(self):
        """
        Test sending a notification.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                result = self.notification_service.send_notification(self.notification_data)
                self.assertTrue(result.is_successful)
                self.assertEqual(result.status_code, 200)
                self.notification_repository.delete_notification_by_id(result.data.message_id)

    def test_send_notification_message_none(self):
        """
        Test sending a notification with no message
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification_data = self.notification_data
                notification_data["message"] = None
                result = self.notification_service.send_notification(notification_data)
                self.assertTrue(result.is_successful)

    def test_send_notification_receiver_none(self):
        """
        Test sending a notification with no receiver
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification_data = self.notification_data
                notification_data["receiver"] = None
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Receiver is not specified", result.message)

    def test_send_notification_message_type_none(self):
        """
        Test sending a notification with no message type
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification_data = self.notification_data
                notification_data["message_type"] = None
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Message type is not specified", result.message)

    def test_send_notification_message_type_invalid(self):
        """
        Test sending a notification with an invalid message type
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification_data = self.notification_data
                notification_data["message_type"] = "Invalid"
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Invalid message type", result.message)

    def test_send_notification_receiver_invalid(self):
        """
        Test sending a notification to an invalid receiver
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification_data = self.notification_data
                notification_data["receiver"] = "Invalid"
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Receiver not found", result.message)

    def test_send_notification_system_sender(self):
        """
        Test sending a notification with the sender as System
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification_data = self.notification_data
                notification_data["sender"] = "System"
                result = self.notification_service.send_notification(notification_data)
                self.assertTrue(result.is_successful)
                self.notification_repository.delete_notification_by_id(result.data.message_id)

    def test_send_notification_data_none(self):
        """
        Test sending a notification with no data.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification_data = None
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Notification data is empty", result.message)

    def test_read_all_notifications(self):
        """
        Test reading all notifications for the user.
        """
        with self.app.app_context():
            access_token = self._authenticate('HiwiUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage.from_dict(self.notification_data)
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.read_all_notifications()
                self.assertEqual(response.status_code, 200)
                self.assertEqual(1, len(response.data))
                self.assertEqual(False, response.data[0].read)
                response = self.notification_service.read_all_notifications()
                self.assertEqual(True, response.data[0].read)
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))

    def test_does_unread_messages_exist(self):
        """
        Test if unread messages exist for the user.
        """
        with self.app.app_context():
            access_token = self._authenticate('HiwiUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage.from_dict(self.notification_data)
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.does_unread_message_exist()
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(True, response.data)
                # Test when no unread messages exist
                response = self.notification_service.does_unread_message_exist()
                self.assertEqual(response.status_code, 200)
                self.assertEqual(False, response.data)

    def test_delete_notification_not_found(self):
        """
        Test deleting a notification that does not exist
        """
        with self.app.app_context():
            access_token = self._authenticate('HiwiUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                response = self.notification_service.delete_notification(ObjectId("666c020f7a409003113fedf9"))
                self.assertEqual(response.status_code, 404)
                self.assertEqual("Notification not found", response.message)

    def test_delete_notification(self):
        """
        Test deleting a notification by the receiver.
        """
        with self.app.app_context():
            access_token = self._authenticate('HiwiUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage.from_dict(self.notification_data)
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.delete_notification(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual("Notification deleted successfully", response.message)

    def test_delete_notification_unauthorized(self):
        """
        Test deleting a notification by a user who is not the receiver.
        """
        with self.app.app_context():
            access_token = self._authenticate('HiwiUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage.from_dict(self.notification_data)
                notification.receiver = "otherReceiver"
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.delete_notification(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 403)
                self.assertEqual("You are not authorized to delete this notification", response.message)

    def test_delete_notification_id_none(self):
        """
        Test deleting a notification with an empty ID.
        """
        with self.app.app_context():
            access_token = self._authenticate('HiwiUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                response = self.notification_service.delete_notification(None)
                self.assertEqual(response.status_code, 400)
                self.assertEqual("Notification ID is empty", response.message)

    def test_send_scheduled_reminders(self):
        with self.app.app_context():
            access_token = self._authenticate('HiwiUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage.from_dict(self.notification_data)
                notification.sender = "System"
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.send_scheduled_reminders()
                self.assertEqual(response.status_code, 200)
                self.assertEqual("Reminders sent successfully", response.message)
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))
