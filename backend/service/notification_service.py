import copy
from datetime import datetime, timezone

import requests
from flask_jwt_extended import get_jwt_identity, jwt_required

from db import initialize_db
from model.notification.message_type import MessageType
from model.notification.notification_message import NotificationMessage
from model.repository.notification_repository import NotificationRepository
from model.repository.timesheet_repository import TimesheetRepository
from model.repository.user_repository import UserRepository
from model.request_result import RequestResult


class NotificationService:
    def __init__(self):
        db = initialize_db()
        self.SLACK_TOKEN = db.administration.find_one({}, {"_id": 0, "slackToken": 1}).get("slackToken", "")
        self.notification_repository = NotificationRepository.get_instance()
        self.user_repository = UserRepository.get_instance()
        self.timesheet_repository = TimesheetRepository.get_instance()

    @jwt_required()
    def send_notification(self, notification_data: dict):
        if notification_data is None:
            return RequestResult(False, "Notification data is empty", 400)
        if notification_data.get("sender") != "system":
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
        if str(notification.sender) != "system":
            sender_data = self.user_repository.find_by_username(notification.sender)
            sender_full_name = sender_data.get("personalInfo").get("firstName") + " " + sender_data.get("personalInfo").get(
                "lastName")
        else:
            sender_full_name = "System"
            sender_data = None
        if notification.message is None:
            notification.message = self._message_builder(MessageType(notification.message_type), sender_full_name,
                                                         notification.message_data)
        result = self.notification_repository.create_notification(notification)
        if result.is_successful:
            notification_id = result.data.get("id")
            notification.set_message_id(notification_id)
            result.data = notification
        # Define when a Slack message should be sent
        if (notification.message_type.value == MessageType.TIMESHEET_STATUS_CHANGE.value or
                notification.message_type.value == MessageType.REMINDER.value):
            slack_result = self._send_slack_message(notification, receiver_data, sender_data)
            slack_result.data = notification
            if not slack_result.is_successful: # pragma: no cover
                slack_result.message = f"{slack_result.message} - In-App Message sent successfully"
                slack_result.is_successful = True
                slack_result.status_code = 200
                return slack_result
            else:
                return slack_result
        return result

    @jwt_required()
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
                    update_result = self.notification_repository.update_notification(notification)
            read_result.data = sorted(read_result.data, key=lambda x: x.timestamp, reverse=True)
            return RequestResult(True, "Notifications retrieved successfully", 200, data=read_result.data)
        return read_result # pragma: no cover

    @jwt_required()
    def does_unread_message_exist(self):
        receiver = get_jwt_identity()
        if receiver is None:
            return RequestResult(False, "User not found", 404)
        return self.notification_repository.does_unread_message_exist(receiver)

    def _send_slack_message(self, notification: NotificationMessage, receiver_data: dict, sender_data: dict):
        if self.SLACK_TOKEN == "":
            return RequestResult(False, "Slack integration not set up", 404)
        if receiver_data.get("slackId") is None:
            return RequestResult(False, "Receiver does not have a Slack ID", 400)
        receiver_slack_id = receiver_data.get("slackId")
        if notification.sender != "system" and sender_data is None:
            return RequestResult(False, "Sender not found", 404)
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

    @jwt_required()
    def delete_notification(self, notification_id: str):
        if notification_id is None:
            return RequestResult(False, "Notification ID is empty", 400)
        notification = self.notification_repository.get_notification_by_id(notification_id).data
        if notification is None:
            return RequestResult(False, "Notification not found", 404)
        if not notification.receiver == get_jwt_identity():  # Only the receiver can delete the notification
            return RequestResult(False, "You are not authorized to delete this notification", 403)
        return self.notification_repository.delete_notification_by_id(notification_id)


    def send_scheduled_reminders(self): # pragma: no cover
        """
        Sends reminders to users who have not submitted their timesheets.
        """
        previous_month = datetime.now(timezone.utc).month - 1 if datetime.now(timezone.utc).month > 1 else 12
        previous_year = datetime.now(timezone.utc).year if previous_month != 12 else datetime.now(timezone.utc).year - 1
        day_in_month = datetime.now(timezone.utc).day
        users = self.user_repository.get_users()
        for user in users:
            if user.get('role') == "Hiwi":
                timesheet = self.timesheet_repository.get_timesheet(user.get('username'), previous_month, previous_year)
                if timesheet is not None:
                    if ((timesheet.get('status') == "Not Submitted" or timesheet.get('status') == "Revision")
                            and day_in_month > 5):  # After 5 days a reminder is sent
                        notification_data = {
                            "receiver": user.get('username'),
                            "sender": "system",
                            "message_type": "Reminder",
                            "message": f"Reminder:\nTimesheet incomplete!\n"
                                       f"Timesheet not complete for {previous_month}/{previous_year}"
                        }
                        result = self.send_notification(notification_data)

        return RequestResult(True, "Reminders sent successfully", 200)
