from bson import ObjectId

from db import initialize_db
from model.request_result import RequestResult
from model.time_entry import TimeEntry


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

    def get_time_entry_by_id(self, time_entry_id):
        """
        Retrieves a TimeEntry object from the MongoDB database using its ID.

        :param time_entry_id: The MongoDB ObjectId of the TimeEntry to retrieve.

        :return: The TimeEntry object if found, otherwise None.
        """
        if time_entry_id is None:
            return None
        time_entry_data = self.db.timeEntries.find_one({"_id": ObjectId(time_entry_id)})
        if not time_entry_data:
            return None
        return time_entry_data

    def get_time_entries_by_date(self, date, username):
        """
        Retrieves all TimeEntry objects for a specific date and username.

        :param date: The date for which to retrieve TimeEntry objects.
        :param username: The username associated with the TimeEntry objects.

        :return: A list of TimeEntry objects for the specified date and username.
        """
        if date is None or username is None:
            return None
        time_entries = self.db.timeEntries.find({"date": date, "username": username})
        return list(time_entries)

    #TODO: This method is only used for testing and shouldn't be required
    def get_time_entries(self):
        """
        Retrieves all TimeEntry objects from the database

        :return: A list of all TimeEntry objects
        """
        time_entries = self.db.timeEntries.find()
        return list(time_entries)

    def get_time_entries_by_timesheet_id(self, timesheet_id: str):
        """
        Retrieves all TimeEntry objects associated with a specific timesheet ID from the MongoDB database.

        :param timesheet_id: The timesheet ID to query for TimeEntry objects.

        :return: A list of TimeEntry objects linked to the specified timesheet.
        """
        if not timesheet_id:
            return []
        cursor = self.db.timeEntries.find({"timesheetId": str(timesheet_id)})
        time_entries = [entry for entry in cursor]
        return list(time_entries)

    def update_time_entry(self, time_entry: TimeEntry) -> RequestResult:
        """
        Updates an existing TimeEntry object in the MongoDB database.

        :param time_entry: The TimeEntry object to update.

        :return: A RequestResult indicating the success or failure of the update operation.
        """
        if time_entry is None:
            return RequestResult(False, "Time entry object is None", 400)
        result = self.db.timeEntries.update_one({"_id": ObjectId(time_entry.time_entry_id)},
                                                {"$set": time_entry.to_dict()})

        if result.matched_count == 0:
            return RequestResult(False, "Entry not found", 404)
        if result.modified_count == 0:
            return RequestResult(False, "Entry update failed (Not Modified)", 500)
        if result.acknowledged:
            return RequestResult(True, "Entry updated successfully", 200)
        return RequestResult(False, "Entry update failed", 500)

    def delete_time_entry(self, entry_id: str):
        """
        Deletes a TimeEntry object from the MongoDB database using its ID.

        :param entry_id: The ID of the TimeEntry to delete.

        :return: A RequestResult indicating the success or failure of the delete operation.
        """
        if entry_id is None:
            return RequestResult(False, "Entry ID is None", 400)

        time_entry = self.get_time_entry_by_id(entry_id)
        if not time_entry:
            return RequestResult(False, "Time Entry not found", 404)

        timesheet_id = time_entry.get("timesheetId")

        result = self.db.timeEntries.delete_one({"_id": ObjectId(entry_id)})
        if result.deleted_count == 0:
            return RequestResult(False, "Entry not found", 404)
        if result.acknowledged:
            return RequestResult(True, "Entry deleted successfully", 200, data={"timesheetId": timesheet_id})
        return RequestResult(False, "Entry deletion failed", 500)

    def create_time_entry(self, time_entry: TimeEntry):
        """
        Creates a new TimeEntry object in the MongoDB database.

        :param time_entry: The TimeEntry object to create.
        :return: A RequestResult indicating the success or failure of the creation operation.
        """
        if time_entry is None:
            return RequestResult(False, "Time entry object is None", 400)

        if self.get_time_entry_by_id(time_entry.time_entry_id):
            return RequestResult(False, "Time entry already exists", 409)

        time_entry_dict = time_entry.to_dict()
        result = self.db.timeEntries.insert_one(time_entry_dict)

        if result.acknowledged:
            return RequestResult(True, f'Time entry created successfully with ID: {str(result.inserted_id)}', 201,
                                 data={"_id": ObjectId(result.inserted_id)})
        return RequestResult(False, "Time entry creation failed", 500)
