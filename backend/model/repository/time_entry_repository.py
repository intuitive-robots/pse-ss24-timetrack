from bson import ObjectId

from db import initialize_db
from model.request_result import RequestResult
from model.time_entry import TimeEntry


class TimeEntryRepository:
    """
    Repository class for managing TimeEntry objects in the database
    """
    _instance = None

    @staticmethod
    def get_instance():
        """
        Singleton instance of the TimeEntryRepository class
        :return: TimeEntryRepository instance
        """
        if TimeEntryRepository._instance is None:
            TimeEntryRepository._instance = TimeEntryRepository()
        return TimeEntryRepository._instance

    def __init__(self):
        """
        Initializes the TimeEntryRepository instance
        """
        self.db = initialize_db()

    def get_time_entry_by_id(self, time_entry_id):
        """
        Retrieves a TimeEntry object from the database by its ID
        :param time_entry_id: The ID of the TimeEntry object
        :return: The TimeEntry object if found, otherwise None
        """
        if time_entry_id is None:
            return None
        time_entry_data = self.db.timeEntries.find_one({"_id": ObjectId(time_entry_id)})
        if not time_entry_data:
            return None
        return time_entry_data

    def get_time_entries_by_date(self, date, username):
        """
        Retrieves all TimeEntry objects from the database for a given date
        :param username: The username for which to retrieve TimeEntry objects
        :param date: The date for which to retrieve TimeEntry objects
        :return: A list of TimeEntry objects for the given date
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
        Retrieves all TimeEntry objects from the database that are associated with a specific timesheet ID.

        :param timesheet_id: The ID of the timesheet for which to retrieve TimeEntry objects.
        :return: A list of all TimeEntry documents associated with the given timesheet ID.
        """
        if not timesheet_id:
            return []
        time_entries = self.db.timeEntries.find({"timesheetId": ObjectId(timesheet_id)})
        return list(time_entries)

    def update_time_entry(self, time_entry: TimeEntry):
        """
        Updates a TimeEntry object in the database
        :param time_entry: The TimeEntry object to update
        :return: A RequestResult object indicating the success of the operation
        """
        if time_entry is None:
            return None
        result = self.db.timeEntries.update_one({"_id": ObjectId(time_entry.time_entry_id)},
                                                {"$set": time_entry.to_dict()})

        if result.matched_count == 0:
            return RequestResult(False, "Entry not found", 404)
        if result.modified_count == 0:
            return RequestResult(False, "Entry update failed", 500)
        if result.acknowledged:
            return RequestResult(True, "Entry updated successfully", 200)
        return RequestResult(False, "Entry update failed", 500)

    def delete_time_entry(self, entry_id: str):
        """
        Deletes a TimeEntry object from the database
        :param entry_id: The ID of the TimeEntry object to delete
        :return: A RequestResult object indicating the success of the operation
        """
        if entry_id is None:
            return RequestResult(False, "Entry ID is None", 400)
        result = self.db.timeEntries.delete_one({"_id": ObjectId(entry_id)})
        if result.deleted_count == 0:
            return RequestResult(False, "Entry not found", 404)
        if result.acknowledged:
            return RequestResult(True, "Entry deleted successfully", 200)
        return RequestResult(False, "Entry deletion failed", 500)

    def create_time_entry(self, time_entry: TimeEntry):
        """
        Creates a new TimeEntry object in the database
        :param time_entry: The TimeEntry object to create
        :return: A RequestResult object indicating the success of the operation
        """
        if time_entry is None:
            return RequestResult(False, "Time entry object is None", 400)

        if self.get_time_entry_by_id(time_entry.time_entry_id):
            return RequestResult(False, "Time entry already exists", 409)
        time_entry_dict = time_entry.to_dict()
        time_entry_dict.pop('timeEntryId')
        result = self.db.timeEntries.insert_one(time_entry_dict)
        if result.acknowledged:
            return RequestResult(True, f'Time entry created successfully with ID: {str(result.inserted_id)}', 201)
        return RequestResult(False, "Time entry creation failed", 500)
