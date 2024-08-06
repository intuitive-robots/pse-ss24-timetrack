import copy

import requests
from flask_jwt_extended import get_jwt_identity

from model.notification.message_type import MessageType
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from model.repository.user_repository import UserRepository
from model.request_result import RequestResult


class NotificationService:
    def __init__(self):
        self.SLACK_TOKEN = "xoxb-7391548519795-7490974089332-yGD8ins3aFpjSER7TD3lZdlp" # TODO: Move to environment variable
        self.notification_repository = NotificationRepository.get_instance()
        self.user_repository = UserRepository.get_instance()

    def send_notification(self, notification_data: dict):
        if notification_data is None:
            return RequestResult(False, "Notification data is empty", 400)

        #TODO: Replace this with a validation strategy

        notification_data["sender"] = get_jwt_identity()
        if notification_data.get("receiver") is None:
            return RequestResult(False, "Receiver is not specified", 400)
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
        sender_full_name = sender_data.get("personalInfo").get("firstName") + " " + sender_data.get("personalInfo").get(
            "lastName")
        if notification.message is None:
            notification.message = self._message_builder(MessageType(notification.message_type), sender_full_name,
                                                         notification.message_data)
        result = self.notification_repository.create_notification(notification)
        if result.is_successful:
            notification_id = result.data.get("id")
            notification.set_message_id(notification_id)
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

    def read_all_notifications(self):
        """
        Retrieves all notifications for the current user.
        """
        receiver = get_jwt_identity()
        if receiver is None:
            return RequestResult(False, "User not found", 404)
        read_result = self.notification_repository.get_notifications_by_receiver(receiver)
        if read_result.is_successful:
            new_notifications = copy.deepcopy(read_result.data)
            for notification in new_notifications:
                if not notification.read:
                    notification.read = True
                    self.notification_repository.update_notification(notification)
            return RequestResult(True, "Notifications retrieved successfully", 200, data=read_result.data)
        return read_result

    def does_unread_message_exist(self):
        receiver = get_jwt_identity()
        if receiver is None:
            return RequestResult(False, "User not found", 404)
        return self.notification_repository.does_unread_message_exist(receiver)

    def _send_slack_message(self, notification: NotificationMessage, receiver_data: dict, sender_data: dict):
        if receiver_data.get("slackId") is None:
            return RequestResult(False, "Receiver does not have a Slack ID", 400)
        receiver_slack_id = receiver_data.get("slackId")

        if sender_data.get("slackId") is None:
            return RequestResult(False, "Sender does not have a Slack ID", 400)

        slack_body = {
            "text": notification.message,
            "channel": receiver_slack_id
        }

        response = requests.post(
            url="https://slack.com/api/chat.postMessage",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.SLACK_TOKEN}"},
            json=slack_body
        )
        if response.status_code != 200:
            return RequestResult(False, "Failed to send message", response.status_code)
        notification.sent = True
        sent_update_result = self.notification_repository.update_notification(notification)
        if not sent_update_result.is_successful:
            return sent_update_result
        return RequestResult(True, "Message sent successfully", 200)

    def _message_builder(self, message_type: MessageType, sender: str, message_data=""):
        """
        Builds a message based on the message type.
        """
        if message_type == MessageType.TIMESHEET_STATUS_CHANGE:
            return f"Status Changed: \nTimesheet status of Timesheet {message_data} has been changed by {sender} "
        elif message_type == MessageType.REMINDER:
            return f"Reminder \n You have a pending timesheet. Please submit it as soon as possible"

    def delete_notification(self, notification_id: str):
        if notification_id is None:
            return RequestResult(False, "Notification ID is empty", 400)
        notification = self.notification_repository.get_notification_by_id(notification_id).data
        if notification is None:
            return RequestResult(False, "Notification not found", 404)
        if not notification.receiver == get_jwt_identity():  # Only the receiver can delete the notification
            return RequestResult(False, "You are not authorized to delete this notification", 403)

        return self.notification_repository.delete_notification_by_id(notification_id)
