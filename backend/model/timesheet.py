from datetime import datetime

from model.timesheet_status import TimesheetStatus


class Timesheet:
    def __init__(self, username: str, month: int, year: int, status: TimesheetStatus,
                 total_time: float, overtime: float, last_signature_change: datetime):
        """
        Initializes a new Timesheet object with the given parameters.

        :param username: The username of the Hiwi associated with the timesheet.
        :param month: The month of the timesheet.
        :param year: The year of the timesheet.
        :param status: The status of the timesheet.
        :param total_time: The total time worked by the Hiwi in the timesheet.
        :param overtime: The overtime worked by the Hiwi in the timesheet.
        :param last_signature_change: The date and time of the last signature change.
        """
        self.timesheet_id = None
        self.username = username
        self.month = month
        self.year = year
        self.status = status
        self.total_time = total_time
        self.overtime = overtime
        self.last_signature_change = last_signature_change

    def set_id(self, timesheet_id):
        """
        Sets the ID of the timesheet.

        :param timesheet_id: The ID of the timesheet.
        """
        self.timesheet_id = timesheet_id

    def to_dict(self):
        """
        Converts the Timesheet object to a dictionary format.

        :return: A dictionary representing the timesheet.
        """
        return {
            "timesheetId": self.timesheet_id,
            "username": self.username,
            "month": self.month,
            "year": self.year,
            "status": str(self.status),
            "totalTime": self.total_time,
            "overtime": self.overtime,
            "lastSignatureChange": self.last_signature_change
        }