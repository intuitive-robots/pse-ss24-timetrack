import unittest

from app import app
from model.notification.message_type import MessageType
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from service.notification_service import NotificationService


class TestNotificationService(unittest.TestCase):

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
    def test_send_notification(self):
        notification_data = {
            "receiver": "testHiwi1",
            "sender": "testHiwi2",
            "message": "Test message",
            "message_type": "Reminder",
            "message_data": "Test message data"
        }

        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):

                result = self.notification_service.send_notification(notification_data)
                self.assertTrue(result.is_successful)
                self.notification_repository.delete_notification_by_id(result.data.message_id)

                notification_data["message"] = None
                result = self.notification_service.send_notification(notification_data)
                self.assertTrue(result.is_successful)
                self.notification_repository.delete_notification_by_id(result.data.message_id)

                receiver = notification_data["receiver"]
                notification_data["receiver"] = None
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Receiver is not specified", result.message)
                notification_data["receiver"] = receiver

                message_type = notification_data["message_type"]
                notification_data["message_type"] = None
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Message type is not specified", result.message)
                notification_data["message_type"] = message_type

                notification_data["message_type"] = "Invalid"
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Invalid message type", result.message)
                notification_data["message_type"] = message_type


                notification_data = None
                result = self.notification_service.send_notification(notification_data)
                self.assertFalse(result.is_successful)
                self.assertEqual("Notification data is empty", result.message)



    def test_read_all_notifications(self):
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                all_notifications = self.notification_service.read_all_notifications()
                for notification in all_notifications.data:
                    self.notification_repository.delete_notification_by_id(notification.message_id)
                notification = NotificationMessage(
                    sender="testHiwi2",
                    receiver="testHiwi1",
                    message="Test message",
                    message_type=MessageType.REMINDER,
                )
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.read_all_notifications()

                self.assertEqual(response.status_code, 200)
                self.assertEqual(1, len(response.data))
                self.assertEqual(False, response.data[0].read)
                response = self.notification_service.read_all_notifications()
                self.assertEqual(True, response.data[0].read)
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))

    def test_does_unread_messages_exist(self):
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage(
                    sender="testHiwi2",
                    receiver="testHiwi1",
                    message="Test message",
                    message_type=MessageType.REMINDER,
                )
                read_result = self.notification_service.read_all_notifications()
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.does_unread_message_exist()
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(True, response.data)

                response = self.notification_service.does_unread_message_exist()
                self.assertEqual(response.status_code, 200)
                self.assertEqual(False, response.data)

    def test_delete_notification(self):
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage(
                    sender="testHiwi2",
                    receiver="testHiwi1",
                    message="Test message",
                    message_type=MessageType.REMINDER,
                )
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.delete_notification(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual("Notification deleted successfully", response.message)
                response = self.notification_service.delete_notification(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 404)
                self.assertEqual("Notification not found", response.message)

                notification.receiver = "testHiwi2"
                notification.message_id = None
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.delete_notification(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 403)
                self.assertEqual("You are not authorized to delete this notification", response.message)

                notification.message_id = None
                notification.receiver = "testHiwi1"
                response = self.notification_service.delete_notification(notification.message_id)
                self.assertEqual(response.status_code, 400)
                self.assertEqual("Notification ID is empty", response.message)

    def test_send_scheduled_reminders(self):
        with self.app.app_context():
            access_token = self.authenticate('testHiwi1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                notification = NotificationMessage(
                    sender="system",
                    receiver="testHiwi1",
                    message="Test message",
                    message_type=MessageType.REMINDER,
                )
                creation_result = self.notification_repository.create_notification(notification)
                response = self.notification_service.send_scheduled_reminders()
                self.assertEqual(response.status_code, 200)
                self.assertEqual("Reminders sent successfully", response.message)
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))



