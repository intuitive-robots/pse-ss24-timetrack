from datetime import datetime

from model.timesheet_status import TimesheetStatus
from bson import ObjectId


class Timesheet:
    def __init__(self, username: str, month: int, year: int,
                 timesheet_id=None, status=TimesheetStatus.NOT_SUBMITTED, total_time=0.0,
                 overtime=0.0, last_signature_change=datetime.now(), time_entry_ids=[]):
        """
        Initializes a new Timesheet object with the given parameters.

        :param username: The username of the Hiwi associated with the timesheet.
        :param month: The month of the timesheet.
        :param year: The year of the timesheet.
        TODO Add more parameter DOC
        """
        self.timesheet_id = timesheet_id
        self.username = username
        self.month = month
        self.year = year
        self.status = status
        self.total_time = total_time
        self.overtime = overtime
        self.last_signature_change = last_signature_change
        self.time_entry_ids = time_entry_ids

    @staticmethod
    def from_dict(timesheet_dict: dict):
        """
        Creates a Timesheet object from a dictionary.

        :param timesheet_dict: The dictionary representing the timesheet.
        :return: A Timesheet object.
        """
        timesheet = Timesheet(
            username=timesheet_dict["username"],
            month=timesheet_dict["month"],
            year=timesheet_dict["year"],
            timesheet_id=timesheet_dict.get("_id", None),
            status=TimesheetStatus(timesheet_dict.get("status", TimesheetStatus.NOT_SUBMITTED)),
            total_time=timesheet_dict.get("totalTime", 0.0),
            overtime=timesheet_dict.get("overtime", 0.0),
            last_signature_change=timesheet_dict.get("lastSignatureChange", datetime.now()),
            time_entry_ids=[ObjectId(id) for id in timesheet_dict.get("timeEntryIds", [])]
        )
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
        self.time_entry_ids.append(ObjectId(time_entry_id))

    def remove_time_entry(self, time_entry_id):
        """
        Removes a time entry from the timesheet.

        :param time_entry_id: The ID of the time entry to remove.
        """
        self.time_entry_ids.remove(ObjectId(time_entry_id))

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
