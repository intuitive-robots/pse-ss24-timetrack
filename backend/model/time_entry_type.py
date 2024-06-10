from enum import Enum


class TimeEntryType(Enum):
    """
    Describes the type of time entry within the system.
    """
    WORK_ENTRY = "Work Entry"
    VACATION_ENTRY = "Vacation Entry"

    @staticmethod
    def get_type_by_value(value):
        """
        Get the type by its value.

        :param value: The value to look up.
        :return: The type with the given value.
        """
        for entry_type in TimeEntryType:
            if entry_type.value == value:
                return entry_type
        return None

    def __str__(self):
        """
        Get the value of the type.

        :return: The value of the type.
        """
        return self.value
