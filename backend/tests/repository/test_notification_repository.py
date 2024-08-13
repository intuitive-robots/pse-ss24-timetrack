import unittest

from app import app
from model.notification.message_type import MessageType
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from service.notification_service import NotificationService


class TestNotificationRepository(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.notification_repository = NotificationRepository.get_instance()
        self.notification_service = NotificationService()

    def authenticate(self, username, password):
        """
        Authenticate the user.
        """
        user = {
            "username": username,
            "password": password
        }
        response = self.client.post('/user/login', json=user)
        return response.json['accessToken']
    def test_create_notification(self):
        create_result = self.notification_repository.create_notification(None)
        self.assertFalse(create_result.is_successful)
        self.assertEqual(create_result.status_code, 400)
        self.assertEqual(create_result.message, "Notification is None")

        notification = NotificationMessage(
            receiver="receiver",
            sender="sender",
            message="message",
            message_type=MessageType.TIMESHEET_STATUS_CHANGE
        )
        create_result = self.notification_repository.create_notification(notification)
        self.assertTrue(create_result.is_successful)
        self.assertEqual(create_result.status_code, 201)
        self.assertIsNotNone(create_result.data.get("id"))
        self.notification_repository.delete_notification_by_id(create_result.data.get("id"))

    def test_get_notification_by_id(self):
        get_result = self.notification_repository.get_notification_by_id(None)
        self.assertFalse(get_result.is_successful)
        self.assertEqual(get_result.status_code, 400)
        self.assertEqual(get_result.message, "Given notification ID is None")

        notification = NotificationMessage(
            receiver="receiver",
            sender="sender",
            message="message",
            message_type=MessageType.TIMESHEET_STATUS_CHANGE
        )
        create_result = self.notification_repository.create_notification(notification)
        notification_id = create_result.data.get("id")
        get_result = self.notification_repository.get_notification_by_id(notification_id)
        self.assertTrue(get_result.is_successful)
        self.assertEqual(get_result.status_code, 200)
        self.assertEqual(get_result.data.receiver, "receiver")
        self.assertEqual(get_result.data.sender, "sender")
        self.assertEqual(get_result.data.message, "message")
        self.assertEqual(get_result.data.message_type, MessageType.TIMESHEET_STATUS_CHANGE)
        self.notification_repository.delete_notification_by_id(notification_id)

    def test_update_notification(self):
        notification = NotificationMessage(
            receiver="receiver",
            sender="sender",
            message="message",
            message_type=MessageType.TIMESHEET_STATUS_CHANGE
        )
        create_result = self.notification_repository.create_notification(notification)
        notification_id = create_result.data.get("id")
        notification.message = "new message"
        update_result = self.notification_repository.update_notification(notification)
        self.assertTrue(update_result.is_successful)
        self.assertEqual(update_result.status_code, 200)
        self.assertEqual(update_result.message, "Notification updated successfully")

        update_result = self.notification_repository.update_notification(notification)
        self.assertFalse(update_result.is_successful)
        self.assertEqual(update_result.status_code, 500)
        self.assertEqual(update_result.message, "Notification update failed")

        notification.message_id = "66b93261831dca1c45d90a01"
        notification.message = "new message2"
        update_result = self.notification_repository.update_notification(notification)
        self.assertFalse(update_result.is_successful)
        self.assertEqual(update_result.status_code, 404)
        self.notification_repository.delete_notification_by_id(notification_id)

        notification = None
        update_result = self.notification_repository.update_notification(notification)
        self.assertFalse(update_result.is_successful)
        self.assertEqual(update_result.status_code, 400)

    def test_unread_message_exist(self):
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.notification_service.read_all_notifications()
                unread_message = self.notification_repository.does_unread_message_exist(None)
                self.assertFalse(unread_message.is_successful)
                self.assertEqual(unread_message.status_code, 400)
                self.assertEqual(unread_message.message, "Receiver is None")

                unread_message = self.notification_repository.does_unread_message_exist("testHiwi1")
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

    def test_get_notifications_by_receiver(self):
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.notification_service.read_all_notifications()
                notifications = self.notification_repository.get_notifications_by_receiver(None)
                self.assertFalse(notifications.is_successful)
                self.assertEqual(notifications.status_code, 400)
                self.assertEqual(notifications.message, "Receiver is None")

                notifications = self.notification_service.read_all_notifications()
                for notification in notifications.data:
                    self.notification_repository.delete_notification_by_id(notification.message_id)

                notifications = self.notification_repository.get_notifications_by_receiver("testHiwi1")
                self.assertTrue(notifications.is_successful)
                self.assertEqual(notifications.status_code, 200)
                self.assertEqual(notifications.data, [])

                notification = NotificationMessage(
                    sender="testHiwi2",
                    receiver="testHiwi1",
                    message="Test message",
                    message_type=MessageType.REMINDER,
                )
                creation_result = self.notification_repository.create_notification(notification)
                notifications = self.notification_repository.get_notifications_by_receiver("testHiwi1")
                self.assertTrue(notifications.is_successful)
                self.assertEqual(notifications.status_code, 200)
                self.assertEqual(len(notifications.data), 1)
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))

    def test_delete_notification_by_id(self):
        delete_result = self.notification_repository.delete_notification_by_id(None)
        self.assertFalse(delete_result.is_successful)
        self.assertEqual(delete_result.status_code, 400)
        self.assertEqual(delete_result.message, "Notification ID is None")

        notification = NotificationMessage(
            receiver="receiver",
            sender="sender",
            message="message",
            message_type=MessageType.TIMESHEET_STATUS_CHANGE
        )
        create_result = self.notification_repository.create_notification(notification)
        notification_id = create_result.data.get("id")
        delete_result = self.notification_repository.delete_notification_by_id(notification_id)
        self.assertTrue(delete_result.is_successful)
        self.assertEqual(delete_result.status_code, 200)
        self.assertEqual(delete_result.message, "Notification deleted successfully")

        delete_result = self.notification_repository.delete_notification_by_id(notification_id)
        self.assertFalse(delete_result.is_successful)
        self.assertEqual(delete_result.status_code, 404)
