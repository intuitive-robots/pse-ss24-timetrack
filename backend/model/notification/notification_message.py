import uuid

from model.notification.message_type import MessageType


class NotificationMessage:
    def __init__(self, receiver: str, sender: str, message: str, message_type: MessageType,
                 message_id=None):
        self.message_id = message_id
        self.receiver = receiver
        self.sender = sender
        self.message = message
        self.message_type = message_type

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
                "message_type": self.message_type.value
            }
        return {
            "_id": self.message_id,
            "receiver": self.receiver,
            "sender": self.sender,
            "message": self.message,
            "message_type": self.message_type.value
        }

    def from_dict(data: dict):
        if data is None:
            return None
        receiver = data.get("receiver")
        sender = data.get("sender")
        message = data.get("message")
        message_type = data.get("message_type")
        message_id = data.get("_id")
        return NotificationMessage(receiver, sender, message, MessageType(message_type), message_id)