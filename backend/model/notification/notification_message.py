import datetime
import uuid

from model.notification.message_type import MessageType


class NotificationMessage:
    def __init__(self, receiver: str, sender: str, message: str, message_type: MessageType,
                 timestamp=datetime.datetime.now(),
                 read=False,
                 sent=False,
                 message_id=None,
                 message_data=""):
        self.message_id = message_id
        self.receiver = receiver
        self.sender = sender
        self.message = message
        self.message_type = message_type
        self.timestamp = timestamp
        self.read = read
        self.sent = sent
        self.message_data = message_data

    def set_message_id(self, message_id):
        self.message_id = message_id

    def send_message(self):
        pass

    def to_dict(self):
        if self.message_id is None:
            return {
                "receiver": self.receiver,
                "sender": self.sender,
                "message": self.message,
                "message_type": self.message_type.value,
                "timestamp": self.timestamp,
                "read": self.read,
                "sent": self.sent,
                "message_data": self.message_data
            }
        return {
            "_id": str(self.message_id),
            "receiver": self.receiver,
            "sender": self.sender,
            "message": self.message,
            "message_type": self.message_type.value,
            "timestamp": self.timestamp,
            "read": self.read,
            "sent": self.sent,
            "message_data": self.message_data
        }

    def from_dict(data: dict):
        if data is None:
            return None
        receiver = data.get("receiver")
        sender = data.get("sender")
        message = data.get("message")
        message_type = data.get("message_type")
        message_id = data.get("_id")
        timestamp = data.get("timestamp", datetime.datetime.now())
        read = data.get("read", False)
        sent = data.get("sent", False)
        message_data = data.get("message_data")
        return NotificationMessage(receiver, sender, message, MessageType(message_type), timestamp, read, sent,
                                   message_id, message_data)