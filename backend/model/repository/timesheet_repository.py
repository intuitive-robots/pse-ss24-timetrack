from datetime import date

from bson import ObjectId

from db import initialize_db
from model.request_result import RequestResult
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus
from pymongo.errors import PyMongoError



class TimesheetRepository:
    """
    Repository class for managing Timesheet objects within a MongoDB database. Provides functions for creating,
    retrieving, updating, and deleting timesheets, as well as managing their statuses.
    """
    _instance = None

    @staticmethod
    def get_instance():
        """
        Provides a singleton instance of TimesheetRepository, ensuring it operates with a single state
        across the application.

        :return: The singleton instance of TimesheetRepository.
        """
        if TimesheetRepository._instance is None:
            TimesheetRepository._instance = TimesheetRepository()
        return TimesheetRepository._instance

    def __init__(self):
        """
        Initializes the TimesheetRepository by connecting to the MongoDB database.
        """
        self.db = initialize_db()

    def get_timesheet_by_id(self, timesheet_id):
        """
        Retrieves a Timesheet object from the MongoDB database using its ObjectId.

        :param timesheet_id: The MongoDB ObjectId of the Timesheet to retrieve.
        :return: The Timesheet object if found; otherwise, None.
        """
        if timesheet_id is None:
            return None
        try:
            timesheet_data = self.db.timesheets.find_one({"_id": ObjectId(timesheet_id)})
            if timesheet_data:
                return timesheet_data
        except PyMongoError as e:
            return None

    def get_timesheet(self, username: str, month: int, year: int):
        """
        Retrieves a Timesheet from the database based on the username, month, and year.

        :param username: The username associated with the timesheet.
        :param month: The month for which the timesheet is recorded.
        :param year: The year for which the timesheet is recorded.
        :return: The Timesheet object if found; otherwise, None.
        """
        if username is None or month is None or year is None:
            return None
        try:
            timesheet_data = self.db.timesheets.find_one({"username": username, "month": month, "year": year})
            if timesheet_data:
                return timesheet_data
        except PyMongoError as e:
            return None

    def get_current_timesheet(self, username: str):
        """
        Retrieves the most recent timesheet for a given username that has not been submitted.

        :param username: The username for whom to retrieve the current timesheet.
        :return: The current Timesheet object if found; otherwise, None.
        """
        if username is None:
            return None
        try:
            timesheet_data = self.db.timesheets.find_one({"username": username, "status": TimesheetStatus.NOT_SUBMITTED.value})
            if timesheet_data:
                return timesheet_data
        except PyMongoError as e:
            return None

    def get_timesheets_by_time_period(self, username:str, start_date: date, end_date: date):
        """
        Retrieves timesheets for a specified time period for a given username.

        :param username: The username for whom to retrieve timesheets.
        :param start_date: The start date of the time period. Includes timesheets with the month and year of the start_date.
        :param end_date: The end date of the time period. Includes timesheets with the month and year of the end_date.
        :return: A list of Timesheet objects within the specified date range.
        """
        if username is None or start_date is None or end_date is None:
            return None
        start_month = start_date.month
        start_year = start_date.year
        end_month = end_date.month
        end_year = end_date.year
        try:
            timesheet_data = self.db.timesheets.find({"username": username,
                                                      "$or": [
                                                          {"year": {"$gt": start_year, "$lt": end_year}},
                                                          {"$and": [{"year": start_year}, {"year": {"$lt": end_year}}], "month": {"$gte": start_month}},
                                                          {"$and": [{"year": end_year}, {"year": {"$gt": start_year}}], "month": {"$lte": end_month}},
                                                          {"$and": [{"year": end_year}, {"year": start_year}, {"month": {"$gte": start_month}}, {"month": {"$lte": end_month}}]}
                                                      ]})
            return list(timesheet_data)
        except PyMongoError as e:
            return None

    def get_timesheets(self):
        """
        Retrieves all Timesheet objects from the database
        
        :return: A list of all Timesheet objects
        """
        try:
            timesheets = self.db.timesheets.find()
            return list(timesheets)
        except PyMongoError as e:
            return None

    def get_timesheets_by_status(self, status: TimesheetStatus):
        """
        Retrieves all Timesheet objects from the database with the given status
        
        :param status: The status of the timesheet
        :return: A list of Timesheet objects with the given status
        """
        if status is None:
            return None
        try:
            timesheets = self.db.timesheets.find({"status": str(status)})
            return list(timesheets)
        except PyMongoError as e:
            return None

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
        try:
            timesheet_data = self.db.timesheets.find_one({"username": username, "month": month, "year": year})
            if timesheet_data:
                return timesheet_data['_id']
        except PyMongoError as e:
            return None

    def get_timesheets_by_username_status(self, username: str, status: TimesheetStatus):
        """
        Retrieves all timesheets for a given username with a specified status

        :param username: Username of the Hiwi
        :param status: Status of the timesheet
        :return: A list of timesheets for the given username with the specified status
        """
        if username is None or status is None:
            return None
        try:
            timesheets = self.db.timesheets.find({"username": username, "status": str(status)})
            return list(timesheets)
        except PyMongoError as e:
            return None

    def get_timesheets_by_username(self, username: str):
        """
        Retrieves all timesheets for a given username

        :param username: Username of the Hiwi
        :return: A list of timesheets for the given username
        """
        if username is None:
            return None
        try:
            timesheets = self.db.timesheets.find({"username": username})
            return list(timesheets)
        except PyMongoError as e:
            return None

    def update_timesheet_by_dict(self, timesheet_data: dict) -> RequestResult:
        """
        Updates a specific Timesheet in the database.

        :param timesheet_data: The dictionary of a Timesheet object to update.
        :return: A RequestResult indicating the success or failure of the update operation.
        """
        if timesheet_data is None:
            return RequestResult(False, "Please provide a timesheet to update.", 400)
        try:
            result = self.db.timesheets.update_one({"_id": ObjectId(timesheet_data['_id'])},
                                                   {"$set": timesheet_data})
            if result.matched_count == 0:
                return RequestResult(False, "Timesheet not found", 404)
            if result.acknowledged:
                return RequestResult(True, "Timesheet updated successfully", 200)
        except PyMongoError as e:
            return RequestResult(False, f"Timesheet update failed: {str(e)}", 500)
        return RequestResult(False, "Timesheet update failed", 500)

    def update_timesheet(self, timesheet) -> RequestResult:
        """
        Updates a specific Timesheet in the database.

        :param timesheet: The Timesheet object to update.
        :return: A RequestResult indicating the success or failure of the update operation.
        """
        if timesheet is None:
            return RequestResult(False, "Please provide a timesheet to update.", 400)
        try:
            result = self.db.timesheets.update_one({"_id": ObjectId(timesheet.timesheet_id)},
                                               {"$set": timesheet.to_dict()})
            if result.matched_count == 0:
                return RequestResult(False, "Timesheet not found", 404)
            if result.modified_count == 0:
                return RequestResult(False, "Timesheet update failed", 500)
            if result.acknowledged:
                return RequestResult(True, "Timesheet updated successfully", 200)
        except PyMongoError as e:
            return RequestResult(False, f"Timesheet update failed: {str(e)}", 500)
        return RequestResult(False, "Timesheet update failed", 500)

    def set_timesheet_status(self, timesheet_id: str, status) -> RequestResult:
        """
        Updates the status of a timesheet in the database.
        
        :param timesheet_id: The ID of the timesheet to update.
        :param status: The new status of the timesheet.
        :return: A RequestResult object indicating the success of the operation.
        """
        if timesheet_id is None or status is None:
            return RequestResult(False, "Please provide a timesheet ID and status to update the timesheet status.", 400)
        try:
            result = self.db.timesheets.update_one({"_id": ObjectId(timesheet_id)}, {"$set": {"status": str(status)}})
            if result.matched_count == 0:
                return RequestResult(False, "Timesheet not found", 404)
            if result.modified_count == 0:
                return RequestResult(False, "Timesheet status update failed", 500)
            if result.acknowledged:
                return RequestResult(True, "Timesheet status updated successfully", 200)
        except PyMongoError as e:
            return RequestResult(False, f"Timesheet status update failed: {str(e)}", 500)
        return RequestResult(False, "Timesheet status update failed", 500)

    def create_timesheet_by_dict(self, timesheet_data: dict):
        """
         Creates a new Timesheet in the database.

        :param timesheet: The Timesheet object to create.
        :return: A RequestResult indicating the success or failure of the creation operation.
        """
        if timesheet_data is None:
            return RequestResult(False, "Please provide a timesheet to create.", 400)
        try:
            if self.get_timesheet(timesheet_data['username'], timesheet_data['month'], timesheet_data['year']) is not None:
                return RequestResult(False, "Timesheet already exists", 409)
            if '_id' in timesheet_data:
                del timesheet_data['_id']
            result = self.db.timesheets.insert_one(timesheet_data)
            if result.acknowledged:
                return RequestResult(True, f'Timesheet created successfully with ID: {str(result.inserted_id)}', 201,
                                     data={"_id": result.inserted_id})
        except PyMongoError as e:
            return RequestResult(False, f"Timesheet creation failed: {str(e)}", 500)
        return RequestResult(False, "Timesheet creation failed", 500)

    def create_timesheet(self, timesheet: Timesheet):
        """
         Creates a new Timesheet in the database.

        :param timesheet: The Timesheet object to create.
        :return: A RequestResult indicating the success or failure of the creation operation.
        """
        if timesheet is None:
            return RequestResult(False, "Please provide a timesheet to create.", 400)
        try:
            if self.get_timesheet(timesheet.username, timesheet.month, timesheet.year) is not None:
                return RequestResult(False, "Timesheet already exists", 409)
            timesheet_data = timesheet.to_dict()
            result = self.db.timesheets.insert_one(timesheet_data)
            if result.acknowledged:
                return RequestResult(True, f'Timesheet created successfully with ID: {str(result.inserted_id)}', 201,
                                     data={"_id": result.inserted_id})
        except PyMongoError as e:
            return RequestResult(False, f"Timesheet creation failed: {str(e)}", 500)
        return RequestResult(False, "Timesheet creation failed", 500)

    def delete_timesheet(self, timesheet_id) -> RequestResult:
        """
        Deletes a Timesheet from the database based on its ObjectId.

        :param timesheet_id: The ObjectId of the Timesheet to delete.
        :return: A RequestResult indicating the success or failure of the deletion.
        """
        if timesheet_id is None:
            return RequestResult(False, "Please provide a timesheet ID to delete the timesheet.", 400)
        try:
            result = self.db.timesheets.delete_one({"_id": ObjectId(timesheet_id)})
            if result.deleted_count == 0:
                return RequestResult(False, "Timesheet deletion failed", 500)
            if result.acknowledged:
                return RequestResult(True, "Timesheet deleted successfully", 200)
        except PyMongoError as e:
            return RequestResult(False, f"Timesheet deletion failed: {str(e)}", 500)
        return RequestResult(False, "Timesheet deletion failed", 500)
