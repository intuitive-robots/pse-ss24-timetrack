from enum import Enum


class TimesheetStatus(Enum):
    """
    describes the status of a timesheet within the system.
    """
    NOT_SUBMITTED = "Not Submitted"
    WAITING_FOR_APPROVAL = "Waiting for Approval"
    REVISION = "Revision"
    COMPLETE = "Complete"

    @staticmethod
    def get_status_by_value(value: str):
        """
        Get the status by its value.
        :return: The status with the given value.
        """
        for status in TimesheetStatus:
            if status.value == value:
                return status
        return None

    def __str__(self):
        """
        Get the value of the status.
        :return: The value of the status.
        """
        return self.value
