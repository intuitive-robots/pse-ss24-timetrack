from enum import Enum


class ActivityType(Enum):
    """
    Enum representing different types of activities within a project management system. This enum facilitates
    distinguishing between different categories of activities, such as project meetings and project work.

    Attributes:
        PROJECT_MEETING (str): Represents a project meeting activity.
        PROJECT_WORK (str): Represents a project work activity
    """
    PROJECT_MEETING = "Projektbesprechung"
    PROJECT_WORK = "Projektarbeit"

    @staticmethod
    def get_type_by_value(value):
        """
        Retrieves an `ActivityType` enum member based on its string value. This method is useful
        for converting string data (e.g., from a database or user input) into the corresponding enum member.

        :param value: The string representation of the activity type to look up.
        :type value: str
        """
        for entry_type in ActivityType:
            if entry_type.value == value:
                return entry_type
        return None
