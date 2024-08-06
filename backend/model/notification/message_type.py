from enum import Enum


class MessageType(Enum):
    TIMESHEET_STATUS_CHANGE = "Timesheet Status Change"
    REMINDER = "Reminder"

    @staticmethod
    def get_type_by_value(value):
        for message_type in MessageType:
            if message_type.value == value:
                return message_type
        return None

    def __str__(self):
        return self.value
