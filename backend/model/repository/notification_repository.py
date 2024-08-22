from bson import ObjectId
from pymongo.errors import PyMongoError

from db import initialize_db
from model.notification.notification_message import NotificationMessage
from model.request_result import RequestResult


class NotificationRepository:
    __instance = None

    def __init__(self):
        self.db = initialize_db()

    @staticmethod
    def get_instance():
        if NotificationRepository.__instance is None:
            NotificationRepository.__instance = NotificationRepository()
        return NotificationRepository.__instance

    def create_notification(self, notification: NotificationMessage):
        """
        Creates a new notification in the MongoDB database.

        :param notification: The notification to create.

        :return: The ID of the newly created notification.
        """
        try:
            if notification is None:
                return RequestResult(False, "Notification is None", 400)
            notification_data = notification.to_dict()
            result = self.db.notifications.insert_one(notification_data)
            if result.acknowledged:
                notification.set_message_id(str(result.inserted_id))
                return RequestResult(True, "Notification created successfully", 201,
                                     data={"id": str(result.inserted_id)})
            else:
                return RequestResult(False, "Notification creation failed", 500)
        except PyMongoError as e: # pragma: no cover
            return RequestResult(False, str(e), 500)

    def get_notification_by_id(self, notification_id: str):
        """
        Retrieves a notification from the MongoDB database using its ID.

        :param notification_id: The ID of the notification to retrieve.

        :return: The notification object if found, None otherwise.
        """
        if notification_id is None:
            return RequestResult(False, "Given notification ID is None", 400)
        try:
            notification_data = self.db.notifications.find_one({"_id": ObjectId(notification_id)})
            if notification_data:
                return RequestResult(True, "Notification found", 200,
                                     data=NotificationMessage.from_dict(notification_data))
            else:
                return RequestResult(False, "Notification not found", 404)
        except PyMongoError as e: # pragma: no cover
            return RequestResult(False, str(e), 500)

    def update_notification(self, notification: NotificationMessage):
        """
        Updates an existing notification in the MongoDB database.

        :param notification: The updated notification object.

        :return: A RequestResult indicating the success or failure of the update operation.
        """
        if notification is None:
            return RequestResult(False, "Notification is None", 400)
        try:
            notification_data = notification.to_dict()
            notification_data.pop("_id", None)
            result = self.db.notifications.update_one({"_id": ObjectId(notification.message_id)},
                                                      {"$set": notification_data})
            if result.matched_count == 0:
                return RequestResult(False, "Notification not found", 404)
            if result.modified_count == 0:
                return RequestResult(False, "Notification update failed", 500)
            if result.acknowledged:
                return RequestResult(True, "Notification updated successfully", 200)
        except PyMongoError as e: # pragma: no cover
            return RequestResult(False, str(e), 500)

    def does_unread_message_exist(self, receiver: str):
        """
        Checks if there are any unread messages for the given receiver in the MongoDB database.

        :param receiver: The username of the receiver.

        :return: True if unread messages exist, False otherwise.
        """
        if receiver is None:
            return RequestResult(False, "Receiver is None", 400)
        try:
            unread_message = self.db.notifications.find_one({"receiver": receiver, "read": False})
            if unread_message is not None:
                return RequestResult(True, "Unread message found", 200, data=True)
            else:
                return RequestResult(True, "No unread message found", 200, data=False)
        except PyMongoError as e: # pragma: no cover
            return RequestResult(False, str(e), 500)

    def get_notifications_by_receiver(self, receiver: str):
        """
        Retrieves all notifications for a given receiver from the MongoDB database.

        :param receiver: The username of the receiver.

        :return: A list of notifications for the receiver.
        """
        if receiver is None:
            return RequestResult(False, "Receiver is None", 400)
        try:
            notifications = list(self.db.notifications.find({"receiver": receiver}))
            return RequestResult(True, "Notifications retrieved successfully", 200,
                                 data=[NotificationMessage.from_dict(notification) for notification in notifications])
        except PyMongoError as e: # pragma: no cover
            return RequestResult(False, str(e), 500)

    def delete_notification_by_id(self, notification_id: str):
        """
        Deletes a notification from the MongoDB database using its ID.

        :param notification_id: The ID of the notification to delete.

        :return: A RequestResult indicating the success or failure of the delete operation.
        """
        if notification_id is None:
            return RequestResult(False, "Notification ID is None", 400)
        try:
            result = self.db.notifications.delete_one({"_id": ObjectId(notification_id)})
            if result.deleted_count == 1:
                return RequestResult(True, "Notification deleted successfully", 200)
            else:
                return RequestResult(False, "Notification not found", 404)
        except PyMongoError as e: # pragma: no cover
            return RequestResult(False, str(e), 500)
