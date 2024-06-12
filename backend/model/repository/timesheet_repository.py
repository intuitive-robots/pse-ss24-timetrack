from datetime import date

from bson import ObjectId

from db import initialize_db
from model.request_result import RequestResult
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus


class TimesheetRepository:
    """
    Repository class for managing Timesheet objects in the database
    """
    _instance = None

    @staticmethod
    def get_instance():
        """
        Singleton instance of the TimesheetRepository class
        :return: TimesheetRepository instance
        """
        if TimesheetRepository._instance is None:
            TimesheetRepository._instance = TimesheetRepository()
        return TimesheetRepository._instance

    def __init__(self):
        """
        Initializes the TimesheetRepository instance
        """
        self.db = initialize_db()

    def get_timesheet_by_id(self, timesheet_id):
        """
        Retrieves a Timesheet object from the database by its ID
        :param timesheet_id: The ID of the Timesheet object
        :return: The Timesheet object if found, otherwise None
        """
        if timesheet_id is None:
            return None
        timesheet_data = self.db.timesheets.find_one({"_id": ObjectId(timesheet_id)})
        if timesheet_data:
            return timesheet_data
        return None

    def get_timesheet(self, username: str, month: int, year: int):
        """
        Retrieves a Timesheet object from the database by username, month, and year
        :param username: Username of the Hiwi
        :param month: Month of the timesheet
        :param year: Year of the timesheet
        :return: object if found, otherwise None
        """
        if username is None or month is None or year is None:
            return None
        timesheet_data = self.db.timesheets.find_one({"username": username, "month": month, "year": year})
        if timesheet_data:
            return timesheet_data
        return None

    def get_current_timesheet(self, username: str):
        """
        Retrieves the current timesheet for the given username
        :param username: Username of the Hiwi
        :return: object if found, otherwise None
        """
        if username is None:
            return None
        timesheet_data = self.db.timesheets.find_one({"username": username, "status": TimesheetStatus.NOT_SUBMITTED.value})

        if timesheet_data:
            return timesheet_data
        return None

    def get_timesheet_by_time_period(self, username:str, start_date: date, end_date: date):
        """
        Retrieves all timesheets for a given username within a specified time period
        :param username: Username of the Hiwi
        :param start_date: Start date of the time period
        :param end_date: End date of the time period
        :return: A list of timesheets for the given username within the specified time period
        """
        if username is None or start_date is None or end_date is None:
            return None
        timesheet_data = self.db.timesheets.find({"username": username, "date": {"$gte": start_date, "$lte": end_date}})
        return list(timesheet_data)

    def get_timesheets(self):
        """
        Retrieves all Timesheet objects from the database
        :return: A list of all Timesheet objects
        """
        timesheets = self.db.timesheets.find()
        return list(timesheets)

    def get_timesheet_by_status(self, status: TimesheetStatus):
        """
        Retrieves all Timesheet objects from the database with the given status
        :param status: The status of the timesheet
        :return: A list of Timesheet objects with the given status
        """
        if status is None:
            return None
        timesheets = self.db.timesheets.find({"status": str(status)})
        return list(timesheets)

    def get_timesheet_id(self, username: str, month: int, year: int):
        """
        Retrieves the timesheet ID for the given username, month, and year
        :param username: Username of the Hiwi
        :param month: Month of the timesheet
        :param year: Year of the timesheet
        :return: The timesheet ID if found, otherwise None
        """
        if username is None or month is None or year is None:
            return None
        timesheet_data = self.db.timesheets.find_one({"username": username, "month": month, "year": year})
        if timesheet_data:
            return timesheet_data['_id']
        return None

    def update_timesheet(self, timesheet):
        """
        Updates a timesheet in the database.
        :param timesheet: The timesheet object to be updated.
        :return: The ID of the updated timesheet.
        """
        if timesheet is None:
            return RequestResult(False, "Please provide a timesheet to update.", 400)
        result = self.db.timesheets.update_one({"_id": ObjectId(timesheet.timesheet_id)},
                                               {"$set": timesheet.to_dict()})
        if result.matched_count == 0:
            return RequestResult(False, "Timesheet not found", 404)
        if result.modified_count == 0:
            return RequestResult(False, "Timesheet update failed", 500)
        if result.acknowledged:
            return RequestResult(True, "Timesheet updated successfully", 200)
        return RequestResult(False, "Timesheet update failed", 500)

    def set_timesheet_status(self, timesheet_id, status):
        """
        Updates the status of a timesheet in the database.
        :param timesheet_id: The ID of the timesheet to update.
        :param status: The new status of the timesheet.
        :return: A RequestResult object indicating the success of the operation.
        """
        if timesheet_id is None or status is None:
            return RequestResult(False, "Please provide a timesheet ID and status to update the timesheet status.", 400)
        result = self.db.timesheets.update_one({"_id": ObjectId(timesheet_id)}, {"$set": {"status": str(status)}})
        if result.matched_count == 0:
            return RequestResult(False, "Timesheet not found", 404)
        if result.modified_count == 0:
            return RequestResult(False, "Timesheet status update failed", 500)
        if result.acknowledged:
            return RequestResult(True, "Timesheet status updated successfully", 200)
        return RequestResult(False, "Timesheet status update failed", 500)

    def delete_timesheet(self, timesheet_id):
        """
        Deletes a timesheet from the database.
        :param timesheet_id: The ID of the timesheet to delete.
        :return: A RequestResult object indicating the success of the operation.
        """
        if timesheet_id is None:
            return RequestResult(False, "Please provide a timesheet ID to delete the timesheet.", 400)
        result = self.db.timesheets.delete_one({"_id": ObjectId(timesheet_id)})
        if result.deleted_count == 0:
            return RequestResult(False, "Timesheet deletion failed", 500)
        if result.acknowledged:
            return RequestResult(True, "Timesheet deleted successfully", 200)
        return RequestResult(False, "Timesheet deletion failed", 500)

    def create_timesheet(self, timesheet: Timesheet):
        """
        Creates a timesheet in the database.
        :param timesheet: The timesheet object to create.
        :return: A RequestResult object indicating the success of the operation.
        """
        if timesheet is None:
            return RequestResult(False, "Please provide a timesheet to create.", 400)
        if self.get_timesheet(timesheet.username, timesheet.month, timesheet.year) is not None:
            return RequestResult(False, "Timesheet already exists", 409)
        timesheet_data = timesheet.to_dict()
        result = self.db.timesheets.insert_one(timesheet_data)
        if result.acknowledged:
            return RequestResult(True, "Timesheet created successfully", 201)
        return RequestResult(False, "Timesheet creation failed", 500)

    def get_timesheets_by_username_status(self, username: str, status: TimesheetStatus):
        """
        Retrieves all timesheets for a given username with a specified status
        :param username: Username of the Hiwi
        :param status: Status of the timesheet
        :return: A list of timesheets for the given username with the specified status
        """
        if username is None or status is None:
            return None
        timesheets = self.db.timesheets.find({"username": username, "status": status})
        return list(timesheets)

    def get_timesheets_by_username(self, username: str):
        """
        Retrieves all timesheets for a given username
        :param username: Username of the Hiwi
        :return: A list of timesheets for the given username
        """
        if username is None:
            return None
        timesheets = self.db.timesheets.find({"username": username})
        return list(timesheets)