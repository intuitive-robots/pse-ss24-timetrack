from flask_jwt_extended import get_jwt_identity

from controller.input_validator.time_entry_data_validator import TimeEntryDataValidator
from controller.input_validator.validation_status import ValidationStatus
from model.repository.time_entry_repository import TimeEntryRepository
from model.time_entry import TimeEntry
from model.request_result import RequestResult
from model.time_entry_type import TimeEntryType
from model.vacation_entry import VacationEntry
from model.work_entry import WorkEntry
from service.timesheet_service import TimesheetService


class TimeEntryService:
    """
    Manages time entry operations, interfacing with the TimeEntryRepository for data storage and retrieval,
    the TimesheetService for handling related timesheet operations, and a validator for time entry data validation.
    """

    def __init__(self):
        """
        Initializes a new instance of the TimeEntryService class.

        This service is responsible for managing time entry operations, interfacing
        with both the TimeEntryRepository for data storage and retrieval, and
        a TimesheetService for handling related timesheet operations, as well as a
        validator for time entry data validation.
        """
        self.time_entry_repository = TimeEntryRepository.get_instance()
        self.timesheet_service = TimesheetService()
        self.entry_validator = TimeEntryDataValidator()

        self.entry_type_mapping = {
            TimeEntryType.WORK_ENTRY: WorkEntry,
            TimeEntryType.VACATION_ENTRY: VacationEntry
        }

    def _add_time_entry(self, entry_data: dict, entry_type: TimeEntryType):
        """
        General method to handle addition of work or vacation time entries.

        :param entry_data: Time entry data.
        :type entry_data: dict
        :param entry_type: The type of the entry (e.g., WorkEntry or VacationEntry).
        :type entry_type: TimeEntryType
        :return: A RequestResult object containing the outcome.
        :rtype: RequestResult
        """
        username = get_jwt_identity()
        entry_data['entryType'] = entry_type.value
        validation_result = self.entry_validator.is_valid(entry_data)
        if validation_result.status == ValidationStatus.FAILURE:
            return RequestResult(False, validation_result.message, status_code=400)

        # Select the appropriate class based on entry_type and create a time entry instance
        entry_class = self.entry_type_mapping.get(entry_type)
        if not entry_class:
            return RequestResult(False, "Invalid entry type specified", status_code=400)

        time_entry = entry_class.from_dict(entry_data)

        entry_creation_result = self.time_entry_repository.create_time_entry(time_entry)
        if not entry_creation_result.is_successful:
            return entry_creation_result

        # Ensure the timesheet exists before adding a new entry
        timesheet_exists_result = self.timesheet_service.ensure_timesheet_exists(
            username, time_entry.start_time.month, time_entry.start_time.year)
        if not timesheet_exists_result.is_successful:
            return timesheet_exists_result

        add_entry_result = self.timesheet_service.add_time_entry_to_timesheet(
            time_entry.timesheet_id, entry_creation_result.data["_id"])
        if not add_entry_result.is_successful:
            return add_entry_result

        if validation_result.status == ValidationStatus.WARNING:
            return RequestResult(True, f"{entry_type.name} entry added with warnings ´{validation_result.message}´",
                                 status_code=200)

        return RequestResult(True, f"{entry_type.name} entry added successfully", status_code=200)

    def create_work_entry(self, entry_data: dict) -> RequestResult:
        """
        Creates a new work time entry in the system based on the provided entry data.

        :param entry_data: A dictionary containing time entry attributes necessary for creating a new time entry.
        :type entry_data: dict
        :return: A RequestResult object containing the result of the create operation.
        :rtype: RequestResult
        """
        return self._add_time_entry(entry_data, TimeEntryType.WORK_ENTRY)

    def add_vacation_entry(self, entry_data: dict) -> RequestResult:
        """
        Adds a new vacation time entry based on the provided entry data.

        :param entry_data: A dictionary containing vacation time entry attributes.
        :type entry_data: dict
        :return: A RequestResult object containing the result of the add operation.
        :rtype: RequestResult
        """
        # TODO Implement vacation logic
        return self._add_time_entry(entry_data, TimeEntryType.VACATION_ENTRY)

    def update_time_entry(self, entry_id: str, update_data: dict) -> RequestResult:
        """
        Updates an existing time entry in the system with the provided update data after validating the data.

        :param entry_id: The ID of the time entry to update.
        :type entry_id: str
        :param update_data: A dictionary with time entry attributes that should be updated.
        :type update_data: dict
        :return: RequestResult object containing the result of the update operation.
        :rtype: RequestResult
        """
        existing_entry_data = self.time_entry_repository.get_time_entry_by_id(entry_id)
        if not existing_entry_data:
            return RequestResult(False, "Time entry not found", status_code=404)

        updated_entry_data = existing_entry_data.copy()
        updated_entry_data.update(update_data)

        validation_result = self.entry_validator.is_valid(updated_entry_data)
        if validation_result.status == ValidationStatus.FAILURE:
            return RequestResult(False, validation_result.message, status_code=400)

        updated_time_entry = TimeEntry.from_dict(updated_entry_data)
        updated_time_entry.set_id(entry_id)
        if not updated_time_entry:
            return RequestResult(False, "Failed to construct updated time entry", status_code=500)

        repo_result = self.time_entry_repository.update_time_entry(updated_time_entry)
        if not repo_result.is_successful:
            return repo_result

        if validation_result.status == ValidationStatus.WARNING:
            return RequestResult(True, f"entry updated with warnings ´{validation_result.message}´",
                                 status_code=200)
        return repo_result

    def delete_time_entry(self, entry_id: str) -> RequestResult:
        """
        Deletes a time entry from the system identified by its ID.

        :param entry_id: The ID of the time entry to be deleted.
        :type entry_id: str
        :return: A RequestResult object containing the result of the delete operation.
        :rtype: RequestResult
        """
        if not entry_id:
            return RequestResult(False, "Entry ID is None", status_code=400)

        delete_result = self.time_entry_repository.delete_time_entry(entry_id)

        if not delete_result.is_successful:
            return delete_result

        return self.timesheet_service.delete_time_entry_from_timesheet(delete_result.data["timesheetId"], entry_id)

    def get_entries_of_timesheet(self, timesheet_id: str) -> list[TimeEntry]:
        """
        Retrieves a list of time entries associated with a specific timesheet ID and converts them into
        TimeEntry objects, considering the specific type of each entry.

        :param timesheet_id: The ID of the timesheet for which to retrieve entries.
        :type timesheet_id: str
        :return: A list of TimeEntry model instances representing all time entries for the specified timesheet.
        :rtype: list[TimeEntry]
        """
        # TODO: Use TimeEntryValidator to check if timesheet_id is valid object id

        entries_data = self.time_entry_repository.get_time_entries_by_timesheet_id(timesheet_id)

        if not entries_data:
            return []
        time_entries = []
        for entry_data in entries_data:
            entry_type = TimeEntryType.get_type_by_value(entry_data['entryType'])
            if entry_type == TimeEntryType.WORK_ENTRY:
                time_entries.append(WorkEntry.from_dict(entry_data))
            elif entry_type == TimeEntryType.VACATION_ENTRY:
                time_entries.append(VacationEntry.from_dict(entry_data))

        return time_entries
