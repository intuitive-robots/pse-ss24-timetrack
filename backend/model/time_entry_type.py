from enum import Enum


class TimeEntryType(Enum):
    """
    Enum representing different types of time entries within a timesheet system. This enum facilitates
    distinguishing between different categories of time entries, such as work-related entries and vacation
    or leave entries.

    Attributes:
        WORK_ENTRY (str): Represents a time entry for regular work.
        VACATION_ENTRY (str): Represents a time entry for vacation or leave.
    """
    WORK_ENTRY = "Work Entry"
    VACATION_ENTRY = "Vacation Entry"

    @staticmethod
    def get_type_by_value(value):
        """
        Retrieves a `TimeEntryType` enum member based on its string value. This method is useful
        for converting string data (e.g., from a database or user input) into the corresponding enum member.

        :param value: The string representation of the time entry type to look up.
        :type value: str

        :return: The corresponding `TimeEntryType` enum member if found, or `None` if no match is found.
        :rtype: Optional[TimeEntryType]

        Examples:
            - `TimeEntryType.get_type_by_value("Work Entry")` will return `TimeEntryType.WORK_ENTRY`.
            - `TimeEntryType.get_type_by_value("Nonexistent Type")` will return `None`.
        """
        for entry_type in TimeEntryType:
            if entry_type.value == value:
                return entry_type
        return None

    def __str__(self):
        """
        Returns the string representation of the enum member, which is useful for displaying the type
        in a user-friendly format.

        :return: The string value associated with the enum member.
        :rtype: str
        """
        return self.value
