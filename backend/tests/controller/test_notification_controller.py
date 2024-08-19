import unittest

from app import app
from model.notification.message_type import MessageType
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from service.notification_service import NotificationService


class TestNotificationController(unittest.TestCase):
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
                response = self.client.get('/notification/doesUnreadMessageExist',
                                           headers={"Authorization": f"Bearer {access_token}"})
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(True, response.json)

                response = self.client.get('/notification/doesUnreadMessageExist',
                                           headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(False, response.json)

    def test_read_all_notifications(self):
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
                response = self.client.get('/notification/readAll',
                                           headers={"Authorization": f"Bearer {access_token}"})
                self.notification_repository.delete_notification_by_id(creation_result.data.get("id"))
                self.assertEqual(response.status_code, 200)
                does_unread_message_exist_response = self.client.get('/notification/doesUnreadMessageExist',
                                                                    headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(does_unread_message_exist_response.status_code, 200)
                self.assertEqual(False, does_unread_message_exist_response.json)
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
                response = self.client.delete('/notification/delete?id=' + creation_result.data.get("id"),
                                              headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual("Notification deleted successfully", response.json)
                response = self.client.delete('/notification/delete?id=' + creation_result.data.get("id"),
                                              headers={"Authorization": f"Bearer {access_token}"})
                self.assertEqual(response.status_code, 404)
                self.assertEqual("Notification not found", response.json)
