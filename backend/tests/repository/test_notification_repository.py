import unittest

from app import app
from db import initialize_db
from model.notification.message_type import MessageType
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from service.notification_service import NotificationService
from utils.security_utils import SecurityUtils


class TestNotificationRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.db = initialize_db()
        cls.client = app.test_client()
        cls.notification_repository = NotificationRepository.get_instance()
        cls.notification_service = NotificationService()
        cls.notification = NotificationMessage(
            receiver="receiver",
            sender="sender",
            message="message",
            message_type=MessageType.TIMESHEET_STATUS_CHANGE
        )
        cls.created_notifications = []
        cls.create_hiwi()

    def tearDown(self):
        self.notification.message_id = None

    @classmethod
    def tearDownClass(cls):
        for notification_id in cls.created_notifications:
            cls.notification_repository.delete_notification_by_id(notification_id)
        cls.db.users.delete_one({"username": "testHiwiNotificationRepo"})

    @classmethod
    def create_hiwi(cls):
        """
        Create a new Hiwi.
        """
        test_hiwi_data = {
            "username": "testHiwiNotificationRepo",
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
                "workingHours": 18,
                "vacationMinutes": 19,
                "overtimeMinutes": 0
            },
            "supervisor": "testSupervisor1",
            "lastLogin": None,
            "isArchived": False,
            "slackId": None
        }
        cls.db.users.insert_one(test_hiwi_data)

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

    def test_create_notification_none(self):
        """
        Test create_notification with None as input.
        """
        create_result = self.notification_repository.create_notification(None)
        self.assertFalse(create_result.is_successful)
        self.assertEqual(create_result.status_code, 400)
        self.assertEqual(create_result.message, "Notification is None")

    def test_create_notification(self):

        create_result = self.notification_repository.create_notification(self.notification)
        self.assertTrue(create_result.is_successful)
        self.assertEqual(create_result.status_code, 201)
        self.assertIsNotNone(create_result.data.get("id"))
        self.created_notifications.append(create_result.data.get("id"))

    def test_get_notification_by_id_none(self):
        """
        Test get_notification_by_id with None as input.
        """
        get_result = self.notification_repository.get_notification_by_id(None)
        self.assertFalse(get_result.is_successful)
        self.assertEqual(get_result.status_code, 400)
        self.assertEqual(get_result.message, "Given notification ID is None")

    def test_get_notification_by_id(self):

        create_result = self.notification_repository.create_notification(self.notification)
        notification_id = create_result.data.get("id")
        self.created_notifications.append(notification_id)
        get_result = self.notification_repository.get_notification_by_id(notification_id)
        self.assertTrue(get_result.is_successful)
        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.data.receiver, "receiver")
        self.assertEqual(get_result.data.sender, "sender")
        self.assertEqual(get_result.data.message, "message")
        self.assertEqual(get_result.data.message_type, MessageType.TIMESHEET_STATUS_CHANGE)
        self.notification_repository.delete_notification_by_id(notification_id)


    def test_update_notification_none(self):
        """
        Test update_notification with None as input.
        """
        update_result = self.notification_repository.update_notification(None)
        self.assertFalse(update_result.is_successful)
        self.assertEqual(update_result.status_code, 400)
        self.assertEqual(update_result.message, "Notification is None")
    def test_update_notification_no_changes(self):
        create_result = self.notification_repository.create_notification(self.notification)
        notification_id = create_result.data.get("id")
        self.created_notifications.append(notification_id)

        update_result = self.notification_repository.update_notification(self.notification)
        self.assertFalse(update_result.is_successful)
        self.assertEqual(update_result.status_code, 500)
        self.assertEqual(update_result.message, "Notification update failed")

    def test_update_notification_invalid_id(self):
        self.notification.message_id = "66b93261831dca1c45d90a01"
        self.notification.message = "new message"
        update_result = self.notification_repository.update_notification(self.notification)
        self.assertFalse(update_result.is_successful)
        self.assertEqual(update_result.status_code, 404)
        self.assertEqual(update_result.message, "Notification not found")

    def test_update_notification(self):

        create_result = self.notification_repository.create_notification(self.notification)
        notification_id = create_result.data.get("id")
        self.created_notifications.append(notification_id)
        self.notification.message = "new message"
        update_result = self.notification_repository.update_notification(self.notification)
        self.assertTrue(update_result.is_successful)
        self.assertEqual(update_result.status_code, 200)
        self.assertEqual(update_result.message, "Notification updated successfully")



    def test_does_unread_message_exist_none(self):
        """
        Test does_unread_message_exist with None as input.
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiNotificationRepo', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                unread_message = self.notification_repository.does_unread_message_exist(None)
                self.assertFalse(unread_message.is_successful)
                self.assertEqual(unread_message.status_code, 400)
                self.assertEqual(unread_message.message, "Receiver is None")

    def test_unread_message_exist_yes(self):
        """
        Test does_unread_message_exist with unread message.
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiNotificationRepo', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage(
                    sender="sender",
                    receiver="testHiwiNotificationRepo",
                    message="Test message",
                    message_type=MessageType.REMINDER,
                )
                creation_result = self.notification_repository.create_notification(notification)
                self.created_notifications.append(creation_result.data.get("id"))
                unread_message = self.notification_repository.does_unread_message_exist("testHiwiNotificationRepo")
                self.assertTrue(unread_message.is_successful)
                self.assertEqual(unread_message.status_code, 200)
                self.assertEqual(unread_message.data, True)
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))

    def test_unread_message_exist_no(self):
        with self.app.app_context():
            access_token = self._authenticate('testHiwiNotificationRepo', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                unread_message = self.notification_repository.does_unread_message_exist("testHiwiNotificationRepo")
                self.assertTrue(unread_message.is_successful)
                self.assertEqual(unread_message.status_code, 200)
                self.assertEqual(unread_message.data, False)

                notification = NotificationMessage(
                    sender="testHiwi2",
                    receiver="testHiwi1",
                    message="Test message",
                    message_type=MessageType.REMINDER,
                )
                creation_result = self.notification_repository.create_notification(notification)
                unread_message = self.notification_repository.does_unread_message_exist("testHiwi1")
                self.assertTrue(unread_message.is_successful)
                self.assertEqual(unread_message.status_code, 200)
                self.assertEqual(unread_message.data, True)
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))


    def test_get_notifications_by_receiver_none(self):
        """
        Test get_notifications_by_receiver with None as input.
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiNotificationRepo', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notifications = self.notification_repository.get_notifications_by_receiver(None)
                self.assertFalse(notifications.is_successful)
                self.assertEqual(notifications.status_code, 400)
                self.assertEqual(notifications.message, "Receiver is None")

    def test_get_notifications_by_receiver_empty(self):
        """
        Test get_notifications_by_receiver with empty notifications
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiNotificationRepo', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notifications = self.notification_repository.get_notifications_by_receiver("testHiwiNotificationRepo")
                self.assertTrue(notifications.is_successful)
                self.assertEqual(notifications.status_code, 200)
                self.assertEqual(notifications.data, [])
    def test_get_notifications_by_receiver(self):
        """
        Test get_notifications_by_receiver with notifications
        """
        with self.app.app_context():
            access_token = self._authenticate('testHiwiNotificationRepo', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage(
                    sender="sender",
                    receiver="testHiwiNotificationRepo",
                    message="Test message",
                    message_type=MessageType.REMINDER,
                )
                creation_result = self.notification_repository.create_notification(notification)
                self.created_notifications.append(creation_result.data.get("id"))
                notifications = self.notification_repository.get_notifications_by_receiver("testHiwiNotificationRepo")
                self.assertTrue(notifications.is_successful)
                self.assertEqual(notifications.status_code, 200)
                self.assertEqual(len(notifications.data), 1)
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))

    def test_delete_notification_by_id_none(self):
        """
        Test delete_notification_by_id with None as input.
        """
        delete_result = self.notification_repository.delete_notification_by_id(None)
        self.assertFalse(delete_result.is_successful)
        self.assertEqual(delete_result.status_code, 400)
        self.assertEqual(delete_result.message, "Notification ID is None")
    def test_delete_notification_by_id_invalid_id(self):
        """
        Test delete_notification_by_id with invalid ID.
        """
        delete_result = self.notification_repository.delete_notification_by_id("66b93261831dca1c45d90a01")
        self.assertFalse(delete_result.is_successful)
        self.assertEqual(delete_result.status_code, 404)
        self.assertEqual(delete_result.message, "Notification not found")

    def test_delete_notification_by_id(self):
        notification = NotificationMessage(
            receiver="receiver",
            sender="sender",
            message="message",
            message_type=MessageType.TIMESHEET_STATUS_CHANGE
        )
        create_result = self.notification_repository.create_notification(notification)
        self.created_notifications.append(create_result.data.get("id"))
        notification_id = create_result.data.get("id")
        delete_result = self.notification_repository.delete_notification_by_id(notification_id)
        self.assertTrue(delete_result.is_successful)
        self.assertEqual(delete_result.status_code, 200)
        self.assertEqual(delete_result.message, "Notification deleted successfully")

