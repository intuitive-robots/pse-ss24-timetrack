import requests
from flask_jwt_extended import get_jwt_identity

from model.notification.message_type import MessageType
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from model.repository.user_repository import UserRepository
from model.request_result import RequestResult


class NotificationService:
    def __init__(self):
        self.SLACK_TOKEN = "xoxb-7391548519795-7490974089332-yGD8ins3aFpjSER7TD3lZdlp"
        self.notification_repository = NotificationRepository.get_instance()
        self.user_repository = UserRepository.get_instance()

    def send_notification(self, notification_data: dict):
        if notification_data is None:
            return RequestResult(False, "Notification data is empty", 400)

        #TODO: Replace this with a validation strategy

        notification_data["sender"] = get_jwt_identity()
        if notification_data.get("receiver") is None:
            return RequestResult(False, "Receiver is not specified", 400)
        if notification_data.get("message") is None:
            return RequestResult(False, "Message is not specified", 400)
        if notification_data.get("message_type") is None:
            return RequestResult(False, "Message type is not specified", 400)
        message_type = notification_data.get("message_type")
        if not message_type == MessageType.TIMESHEET_STATUS_CHANGE.value and not message_type == MessageType.REMINDER.value:
            return RequestResult(False, "Invalid message type", 400)
        notification = NotificationMessage.from_dict(notification_data)
        if notification is None:
            return RequestResult(False, "Notification data is invalid", 400)
        receiver_data = self.user_repository.find_by_username(notification.receiver)
        if receiver_data is None:
            return RequestResult(False, "Receiver not found", 404)
        sender_data = self.user_repository.find_by_username(notification.sender)
        if sender_data is None:
            return RequestResult(False, "Sender not found", 404)

        result = self.notification_repository.create_notification(notification)
        # Define when a Slack message should be sent
        if (notification.message_type.value == MessageType.TIMESHEET_STATUS_CHANGE.value or
                notification.message_type.value == MessageType.REMINDER.value):
            slack_result = self._send_slack_message(notification, receiver_data, sender_data)
            if not slack_result.is_successful:
                slack_result.message = f"{slack_result.message} - In-App Message sent successfully"
                return slack_result
            else:
                return slack_result
        return result

    def _send_slack_message(self, notification: NotificationMessage, receiver_data: dict, sender_data: dict):
        if receiver_data.get("slackId") is None:
            return RequestResult(False, "Receiver does not have a Slack ID", 400)
        receiver_slack_id = receiver_data.get("slackId")
        receiver_full_name = receiver_data.get("personalInfo").get("firstName") + " " + receiver_data.get(
            "personalInfo").get("lastName")

        if sender_data.get("slackId") is None:
            return RequestResult(False, "Sender does not have a Slack ID", 400)
        sender_full_name = sender_data.get("personalInfo").get("firstName") + " " + sender_data.get("personalInfo").get(
            "lastName")

        slack_body = {
            "text": f"From: {sender_full_name}\nTo: {receiver_full_name}\nMessage: {notification.message}",
            "channel": receiver_slack_id
        }

        response = requests.post(
            url="https://slack.com/api/chat.postMessage",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.SLACK_TOKEN}"},
            json=slack_body
        )
        if response.status_code != 200:
            return RequestResult(False, "Failed to send message", response.status_code)
        return RequestResult(True, "Message sent successfully", 200)

    def delete_notification(self, notification_id: str):
        if notification_id is None:
            return RequestResult(False, "Notification ID is empty", 400)
        notification = self.notification_repository.get_notification_by_id(notification_id).data
        if notification is None:
            return RequestResult(False, "Notification not found", 404)
        if not notification.receiver == get_jwt_identity():  # Only the receiver can delete the notification
            return RequestResult(False, "You are not authorized to delete this notification", 403)

        return self.notification_repository.delete_notification_by_id(notification_id)
