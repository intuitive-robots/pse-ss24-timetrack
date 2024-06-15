from enum import Enum


class TimesheetStatus(Enum):
    """
    Enum representing the various statuses a timesheet can have within a system, defining the progress
    and state of a timesheet from creation to completion.

    This enum facilitates state management of timesheets, allowing systems to track and control the workflow
    of timesheet processing, approval, and archival.

    Attributes:
        NOT_SUBMITTED (str): Status indicating the timesheet has not yet been submitted for approval.
        WAITING_FOR_APPROVAL (str): Status indicating the timesheet has been submitted and is awaiting approval.
        REVISION (str): Status indicating the timesheet requires revisions before it can be approved.
        COMPLETE (str): Status indicating the timesheet has been approved and is now considered complete.
    """
    NOT_SUBMITTED = "Not Submitted"
    WAITING_FOR_APPROVAL = "Waiting for Approval"
    REVISION = "Revision"
    COMPLETE = "Complete"

    @staticmethod
    def get_status_by_value(value: str):
        """
        Retrieves a `TimesheetStatus` enum member based on its string value. This method is useful
        for converting string data (e.g., from user input or database values) into the corresponding
        enum member.

        :param value: The string representation of the timesheet status to look up.
        :type value: str

        :return: The corresponding `TimesheetStatus` enum member if found, or `None` if no match is found.
        :rtype: Optional[TimesheetStatus]

        Example:
            - `TimesheetStatus.get_status_by_value("Not Submitted")` will return `TimesheetStatus.NOT_SUBMITTED`.
            - `TimesheetStatus.get_status_by_value("Nonexistent Status")` will return `None`.
        """
        for status in TimesheetStatus:
            if status.value == value:
                return status
        return None

    def __str__(self):
        """
        Returns the string representation of the enum member, which is useful for displaying the status
        in a user-friendly format or for serializing it to string-based formats like JSON.

        :return: The string value associated with the enum member.
        :rtype: str
        """
        return self.value
