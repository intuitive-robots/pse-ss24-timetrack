
import datetime

from bson import ObjectId

from db import initialize_db
from model.repository.timesheet_repository import TimesheetRepository
from model.request_result import RequestResult
from model.time_entry import TimeEntry
from pymongo.errors import PyMongoError


class TimeEntryRepository:
    """
    Repository class for managing TimeEntry objects in a MongoDB database via GridFS. Handles the operations for
    uploading, updating, retrieving, and deleting time entries along with their associated metadata.
    """
    _instance = None

    @staticmethod
    def get_instance():
        """
        Provides a singleton instance of TimeEntryRepository to ensure only one instance
        is used throughout the application.
        
        :return: The singleton instance of TimeEntryRepository.
        """
        if TimeEntryRepository._instance is None:
            TimeEntryRepository._instance = TimeEntryRepository()
        return TimeEntryRepository._instance

    def __init__(self):
        """
        Initializes the TimeEntryRepository by setting up a connection to the MongoDB database.
        """
        self.db = initialize_db()
        self.timesheet_repository = TimesheetRepository.get_instance()

    def get_time_entry_by_id(self, time_entry_id):
        """
        Retrieves a TimeEntry object from the MongoDB database using its ID.

        :param time_entry_id: The MongoDB ObjectId of the TimeEntry to retrieve.

        :return: The TimeEntry object if found, otherwise None.
        """
        if time_entry_id is None:
            return None
        try:
            time_entry_data = self.db.timeEntries.find_one({"_id": ObjectId(time_entry_id)})
            if not time_entry_data:
                return None
            return time_entry_data
        except PyMongoError as e:  # pragma: no cover
            return None

    def get_time_entries_by_date(self, date, username):
        """
        Retrieves all TimeEntry objects for a specific date and username.

        :param date: The date for which to retrieve TimeEntry objects.
        :param username: The username associated with the TimeEntry objects.

        :return: A list of TimeEntry objects for the specified date and username.
        """
        if date is None or username is None:
            return None
        start_date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        end_date = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)
        try:
            timesheet_id = self.timesheet_repository.get_timesheet_id(username, date.month, date.year)
            time_entries = self.db.timeEntries.find({"startTime": {"$gte": start_date, "$lt": end_date},
                                                     "timesheetId": str(timesheet_id)})
            return list(time_entries)
        except PyMongoError as e:  # pragma: no cover
            return None

    def get_time_entries_by_timesheet_id(self, timesheet_id: str):
        """
        Retrieves all TimeEntry objects associated with a specific timesheet ID from the MongoDB database.

        :param timesheet_id: The timesheet ID to query for TimeEntry objects.

        :return: A list of TimeEntry objects linked to the specified timesheet.
        """
        if not timesheet_id:
            return []
        try:
            cursor = self.db.timeEntries.find({"timesheetId": str(timesheet_id)})
            time_entries = [entry for entry in cursor]
            return list(time_entries)
        except PyMongoError as e:  # pragma: no cover
            return []

    def update_time_entry(self, time_entry: TimeEntry) -> RequestResult:
        """
        Updates an existing TimeEntry object in the MongoDB database.

        :param time_entry: The TimeEntry object to update.

        :return: A RequestResult indicating the success or failure of the update operation.
        """
        if time_entry is None:
            return RequestResult(False, "Time entry object is None", 400)
        try:
            result = self.db.timeEntries.update_one({"_id": time_entry.time_entry_id},
                                                    {"$set": time_entry.to_dict()})
            if result.matched_count == 0:
                return RequestResult(False, "Entry not found", 404)
            if result.modified_count == 0:
                return RequestResult(False, "Entry update failed (Not Modified)", 500)
            if result.acknowledged:
                return RequestResult(True, "Entry updated successfully", 200)
        except PyMongoError as e:  # pragma: no cover
            return RequestResult(False, f"Entry update failed: {str(e)}", 500)
        return RequestResult(False, "Entry update failed", 500)

    def create_time_entry(self, time_entry: TimeEntry):
        """
        Creates a new TimeEntry object in the MongoDB database.

        :param time_entry: The TimeEntry object to create.
        :return: A RequestResult indicating the success or failure of the creation operation.
        """
        if time_entry is None:
            return RequestResult(False, "Time entry object is None", 400)
        try:
            if self.get_time_entry_by_id(time_entry.time_entry_id):
                return RequestResult(False, "Time entry already exists", 409)
            if not self.timesheet_repository.get_timesheet_by_id(time_entry.timesheet_id):
                return RequestResult(False, "Timesheet not found", 404)

            time_entry_dict = time_entry.to_dict()
            if '_id' in time_entry_dict:
                del time_entry_dict['_id']

            result = self.db.timeEntries.insert_one(time_entry_dict)

            if result.acknowledged:
                return RequestResult(True, f'Time entry created successfully with ID: {str(result.inserted_id)}', 201,
                                     data={"_id": ObjectId(result.inserted_id)})
        except PyMongoError as e:  # pragma: no cover
            return RequestResult(False, f"Time entry creation failed: {str(e)}", 500)
        return RequestResult(False, "Time entry creation failed", 500)

    def delete_time_entry(self, entry_id: str):
        """
        Deletes a TimeEntry object from the MongoDB database using its ID.

        :param entry_id: The ID of the TimeEntry to delete.

        :return: A RequestResult indicating the success or failure of the delete operation.
        """
        if entry_id is None:
            return RequestResult(False, "Entry ID is None", 400)
        try:
            time_entry_data = self.get_time_entry_by_id(entry_id)
            if not time_entry_data:
                return RequestResult(False, "Time Entry not found", 404)

            timesheet_id = time_entry_data.get("timesheetId")

            result = self.db.timeEntries.delete_one({"_id": ObjectId(entry_id)})
            if result.deleted_count == 0:
                return RequestResult(False, "Entry not found", 404)
            if result.acknowledged:
                return RequestResult(True, "Entry deleted successfully", 200, data={"timesheetId": timesheet_id})
        except PyMongoError as e:  # pragma: no cover
            return RequestResult(False, f"Entry deletion failed: {str(e)}", 500)
        return RequestResult(False, "Entry deletion failed", 500)
