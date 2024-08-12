from datetime import datetime

from model.timesheet_status import TimesheetStatus
from bson import ObjectId


class Timesheet:
    """
    Represents a timesheet for an employee (Hiwi), encapsulating all relevant data for a specific month and year,
    including time entries, total hours, and overtime.

    Attributes:
        timesheet_id (ObjectId): Unique identifier for the timesheet, typically generated by the database.
        username (str): Username of the Hiwi associated with the timesheet.
        month (int): Month for which the timesheet is applicable.
        year (int): Year for which the timesheet is applicable.
        status (TimesheetStatus): Current status of the timesheet, e.g., submitted, not submitted, approved.
        total_time (float): Total hours recorded in the timesheet.
        overtime (float): Total overtime hours recorded in the timesheet.
        last_signature_change (datetime): Timestamp of the last signature or approval change.
        time_entry_ids (list[ObjectId]): List of ObjectIds corresponding to the time entries included in the timesheet.
    """

    def __init__(self, username: str, month: int, year: int,
                 timesheet_id=None, status=TimesheetStatus.NOT_SUBMITTED, total_time=0.0,
                 overtime=0.0, last_signature_change=datetime.utcnow()):
        """
        Initializes a new Timesheet object with the given parameters.

        :param username: The username of the employee associated with the timesheet.
        :type username: str
        :param month: The month of the timesheet.
        :type month: int
        :param year: The year of the timesheet.
        :type year: int
        :param timesheet_id: The unique identifier for the timesheet, if already assigned.
        :type timesheet_id: ObjectId, optional
        :param status: The current status of the timesheet, defaults to NOT_SUBMITTED.
        :type status: TimesheetStatus
        :param total_time: The total hours worked in this timesheet, defaults to 0.0.
        :type total_time: float
        :param overtime: The total overtime hours worked, defaults to 0.0.
        :type overtime: float
        :param last_signature_change: The datetime of the last signature update, defaults to current time.
        :type last_signature_change: datetime
        """
        self.timesheet_id = timesheet_id
        self.username = username
        self.month = month
        self.year = year
        self.status = status
        self.total_time = total_time
        self.overtime = overtime
        self.last_signature_change = last_signature_change

    @staticmethod
    def from_dict(timesheet_dict: dict):
        """
        Factory method that creates a Timesheet object from a dictionary containing its data, typically retrieved from a database.

        :param timesheet_dict: A dictionary containing all necessary data keys to instantiate a Timesheet.
        :type timesheet_dict: dict

        :return: A fully instantiated Timesheet object.
        :rtype: Timesheet
        """
        timesheet = Timesheet(
            username=timesheet_dict["username"],
            month=timesheet_dict["month"],
            year=timesheet_dict["year"],
            timesheet_id=timesheet_dict.get("_id", None),
            status=TimesheetStatus(timesheet_dict.get("status", TimesheetStatus.NOT_SUBMITTED)),
            total_time=timesheet_dict.get("totalTime", 0.0),
            overtime=timesheet_dict.get("overtime", 0.0),
            last_signature_change=timesheet_dict.get("lastSignatureChange", datetime.utcnow())
        )
        return timesheet

    def set_id(self, timesheet_id):
        """
        Sets or updates the unique identifier of the timesheet.

        :param timesheet_id: The new identifier to assign to this timesheet.
        :type timesheet_id: ObjectId
        """
        self.timesheet_id = timesheet_id

    def to_dict(self):
        """
        Converts the Timesheet object to a dictionary suitable for serialization, typically for database storage or API responses.

        :return: A dictionary representation of the Timesheet object.
        :rtype: dict
        """
        if self.timesheet_id is None:
            return {
                "username": self.username,
                "month": self.month,
                "year": self.year,
                "status": str(self.status),
                "totalTime": self.total_time,
                "overtime": self.overtime,
                "lastSignatureChange": self.last_signature_change
            }
        return {
            "_id": self.timesheet_id,
            "username": self.username,
            "month": self.month,
            "year": self.year,
            "status": str(self.status),
            "totalTime": self.total_time,
            "overtime": self.overtime,
            "lastSignatureChange": self.last_signature_change
        }

    def to_str_dict(self):
        """
        Converts the Timesheet object to a dictionary suitable for serialization, typically for database storage or API responses.

        :return: A dictionary representation of the Timesheet object.
        :rtype: dict
        """
        return {
            "_id": str(self.timesheet_id),
            "username": self.username,
            "month": self.month,
            "year": self.year,
            "status": str(self.status),
            "totalTime": self.total_time,
            "overtime": self.overtime,
            "lastSignatureChange": self.last_signature_change
        }
