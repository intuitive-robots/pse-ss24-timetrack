from db import initialize_db
from model.request_result import RequestResult
from model.time_entry import TimeEntry
from model.vacation_entry import VacationEntry
from model.work_entry import WorkEntry


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
        time_entry_data = self.db.timeEntries.find_one({"timeEntryId": time_entry_id})
        if time_entry_data:
            if time_entry_data['breakTime']:
                return WorkEntry(
                    time_entry_id=time_entry_data['timeEntryId'],
                    timesheet_id=time_entry_data['timesheetId'],
                    date=time_entry_data['date'],
                    start_time=time_entry_data['startTime'],
                    end_time=time_entry_data['endTime'],
                    break_time=time_entry_data['breakTime'],
                    activity=time_entry_data['activity'],
                    project_name=time_entry_data['projectName']
                )
            else:
                return VacationEntry(
                    time_entry_id=time_entry_data['timeEntryId'],
                    timesheet_id=time_entry_data['timesheetId'],
                    date=time_entry_data['date'],
                    start_time=time_entry_data['startTime'],
                    end_time=time_entry_data['endTime']
                )
        return None

    def get_time_entries_by_date(self, date):
        """
        Retrieves all TimeEntry objects from the database for a given date
        :param date: The date for which to retrieve TimeEntry objects
        :return: A list of TimeEntry objects for the given date
        """
        if date is None:
            return None
        time_entries = self.db.timeEntries.find({"date": date})
        return [self.get_time_entry_by_id(time_entry['timeEntryId']) for time_entry in time_entries]

    def get_time_entries(self):
        """
        Retrieves all TimeEntry objects from the database
        :return: A list of all TimeEntry objects
        """
        time_entries = self.db.timeEntries.find()
        return list(time_entries)

    def update_time_entry(self, time_entry):
        """
        Updates a TimeEntry object in the database
        :param time_entry: The TimeEntry object to update
        :return: A RequestResult object indicating the success of the operation
        """
        if time_entry is None:
            return None
        result = self.db.timeEntries.update_one({"timeEntryId": time_entry.time_entry_id},
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
            return None
        result = self.db.timeEntries.delete_one({"timeEntryId": entry_id})
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
        result = self.db.timeEntries.insert_one(time_entry.to_dict())
        if result.acknowledged:
            return RequestResult(True, f'Time entry created successfully with ID: {str(result.inserted_id)}', 201)
        return RequestResult(False, "Time entry creation failed", 500)

