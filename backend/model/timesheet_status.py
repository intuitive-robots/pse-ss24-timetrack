from enum import Enum


class TimesheetStatus(Enum):
    """
    describes the status of a timesheet within the system.
    """
    NOTSUBMITTED = "Not Submitted"
    WAITINGFORAPPROVAL = "Waiting for Approval"
    REVISION = "Revision"
    COMPLETE = "Complete"

    def get_status_by_value(value):
        """
        Get the status by its value.
        :return: The status with the given value.
        """
        for status in TimesheetStatus:
            if status.value == value:
                return status
        raise ValueError("Status not found")

    def __str__(self):
        """
        Get the value of the status.
        :return: The value of the status.
        """
        return self.value
