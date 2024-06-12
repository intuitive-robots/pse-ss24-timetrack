from datetime import datetime

from model.time_sheet_validator.timesheet_validator import TimesheetValidator
from model.timesheet_status import TimesheetStatus


class Timesheet:
    def __init__(self, username: str, month: int, year: int):
        """
        Initializes a new Timesheet object with the given parameters.

        :param username: The username of the Hiwi associated with the timesheet.
        :param month: The month of the timesheet.
        :param year: The year of the timesheet.
        """
        self.timesheet_id = None
        self.username = username
        self.month = month
        self.year = year
        self.status = TimesheetStatus.NOT_SUBMITTED
        self.total_time = 0.0
        self.overtime = 0.0
        self.last_signature_change = datetime.now()
        self.time_entry_ids = []


    @staticmethod
    def from_dict(timesheet_dict: dict):
        """
        Creates a Timesheet object from a dictionary.

        :param timesheet_dict: The dictionary representing the timesheet.
        :return: A Timesheet object.
        """
        timesheet = Timesheet(timesheet_dict["username"], timesheet_dict["month"], timesheet_dict["year"])
        timesheet.set_id(timesheet_dict["_id"])
        timesheet.status = TimesheetStatus(timesheet_dict["status"])
        timesheet.total_time = timesheet_dict["totalTime"]
        timesheet.overtime = timesheet_dict["overtime"]
        timesheet.last_signature_change = timesheet_dict["lastSignatureChange"]
        return timesheet

    def set_id(self, timesheet_id):
        """
        Sets the ID of the timesheet.

        :param timesheet_id: The ID of the timesheet.
        """
        self.timesheet_id = timesheet_id

    def add_time_entry(self, time_entry_id):
        """
        Adds a time entry to the timesheet.

        :param time_entry_id: The ID of the time entry to add.
        """
        self.time_entry_ids.append(time_entry_id)

    def remove_time_entry(self, time_entry_id):
        """
        Removes a time entry from the timesheet.

        :param time_entry_id: The ID of the time entry to remove.
        """
        self.time_entry_ids.remove(time_entry_id)
        self.timesheet_validator = TimesheetValidator()

    def to_dict(self):
        """
        Converts the Timesheet object to a dictionary format.

        :return: A dictionary representing the timesheet.
        """
        return {
            "username": self.username,
            "month": self.month,
            "year": self.year,
            "status": str(self.status),
            "totalTime": self.total_time,
            "overtime": self.overtime,
            "lastSignatureChange": self.last_signature_change,
            "timeEntryIds": self.time_entry_ids
        }