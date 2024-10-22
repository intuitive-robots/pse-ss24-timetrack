import datetime

from bson import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required

from controller.input_validator.time_entry_data_validator import TimeEntryDataValidator
from controller.input_validator.validation_status import ValidationStatus
from model.repository.time_entry_repository import TimeEntryRepository
from model.time_entry import TimeEntry
from model.request_result import RequestResult
from model.time_entry_type import TimeEntryType
from model.time_entry_validator.break_length_strategy import BreakLengthStrategy
from model.time_entry_validator.holiday_strategy import HolidayStrategy
from model.time_entry_validator.time_entry_validator import TimeEntryValidator
from model.time_entry_validator.vacation_time_strategy import VacationTimeStrategy
from model.time_entry_validator.weekend_strategy import WeekendStrategy
from model.time_entry_validator.working_time_strategy import WorkingTimeStrategy
from model.timesheet_status import TimesheetStatus
from model.vacation_entry import VacationEntry
from model.work_entry import WorkEntry
from service.timesheet_service import TimesheetService
from service.user_service import UserService


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
        self.entry_input_validator = TimeEntryDataValidator()

        self.work_entry_validator = TimeEntryValidator()
        self.vacation_entry_validator = TimeEntryValidator()

        self.work_entry_validator.add_validation_rule(WorkingTimeStrategy())
        self.work_entry_validator.add_validation_rule(BreakLengthStrategy())
        self.work_entry_validator.add_validation_rule(HolidayStrategy())
        self.work_entry_validator.add_validation_rule(WeekendStrategy())

        self.vacation_entry_validator.add_validation_rule(HolidayStrategy())
        self.vacation_entry_validator.add_validation_rule(VacationTimeStrategy())
        self.vacation_entry_validator.add_validation_rule(WeekendStrategy())

        self.user_service = UserService()
        self.entry_type_mapping = {
            TimeEntryType.WORK_ENTRY: WorkEntry,
            TimeEntryType.VACATION_ENTRY: VacationEntry
        }

    def _add_time_entry(self, entry_data: dict, entry_type: TimeEntryType, username: str):  #pragma: no cover
        """
        General method to handle addition of work or vacation time entries.

        :param entry_data: Time entry data.
        :type entry_data: dict
        :param entry_type: The type of the entry (e.g., WorkEntry or VacationEntry).
        :type entry_type: TimeEntryType
        :return: A RequestResult object containing the outcome.
        :rtype: RequestResult
        """
        entry_data['entryType'] = entry_type.value

        # if start time is string
        if isinstance(entry_data['startTime'], str):
            start_date = datetime.datetime.fromisoformat(entry_data['startTime'].replace('Z', ""))
        else:
            start_date = entry_data['startTime']

        # Check if a time entry already exists for the user on this date
        existing_entries = self.time_entry_repository.get_time_entries_by_date(start_date, username)
        if existing_entries:
            return RequestResult(False, "A time entry already exists for this day", status_code=409)

        if entry_data.get('timesheetId') is None:
            result = self.timesheet_service.ensure_timesheet_exists(username, start_date.month, start_date.year)
            if not result.is_successful:
                return RequestResult(False, result.message, result.status_code)

            timesheet_id = self.timesheet_service.get_timesheet(username, start_date.month,
                                                                start_date.year).data.timesheet_id
            entry_data['timesheetId'] = str(timesheet_id)

        timesheet_status = self.timesheet_service.get_timesheet_status(entry_data['timesheetId']).data
        if timesheet_status == TimesheetStatus.COMPLETE or timesheet_status == TimesheetStatus.WAITING_FOR_APPROVAL:
            return RequestResult(False, "Cannot add time entry to a submitted timesheet", status_code=409)

        # Validate input data
        data_validation_result = self.entry_input_validator.is_valid(entry_data)
        if data_validation_result.status == ValidationStatus.FAILURE:
            return RequestResult(False, data_validation_result.message, status_code=400)

        # Select the appropriate class based on entry_type and create a time entry instance
        entry_class = self.entry_type_mapping.get(entry_type)
        if not entry_class:
            return RequestResult(False, "Invalid entry type specified", status_code=422)

        time_entry = entry_class.from_dict(entry_data)

        # Validate the entry through strategy pattern
        strategy_validation_results = self._strategy_validate(time_entry)
        for result in strategy_validation_results:
            if result.status == ValidationStatus.FAILURE:
                return RequestResult(False, result.message, status_code=400)

        entry_creation_result = self.time_entry_repository.create_time_entry(time_entry)
        if not entry_creation_result.is_successful:
            return entry_creation_result

        timesheet_exists_result = self.timesheet_service.ensure_timesheet_exists(
            username, time_entry.start_time.month, time_entry.start_time.year)
        if not timesheet_exists_result.is_successful:
            return timesheet_exists_result
        if entry_type == TimeEntryType.VACATION_ENTRY:
            self.user_service.remove_vacation_minutes(username, time_entry.get_duration())
        self.user_service.add_overtime_minutes(username, time_entry.get_duration())

        result = self.timesheet_service.set_total_and_vacation_time(time_entry.timesheet_id)
        if not result.is_successful:
            return result

        self.timesheet_service.calculate_overtime(entry_data['timesheetId'])
        if data_validation_result.status == ValidationStatus.WARNING:
            return RequestResult(True,
                                 f"{entry_type.name} entry added with warnings ´{data_validation_result.message}´",
                                 status_code=200, data={"_id": entry_creation_result.data["_id"]})
        for result in strategy_validation_results:
            if result.status == ValidationStatus.WARNING:
                return RequestResult(True, f"{entry_type.name} entry added with warnings ´{result.message}´",
                                     status_code=200, data={"_id": entry_creation_result.data["_id"]})
        return RequestResult(True, f"{entry_type.name} entry added successfully", status_code=200,
                             data={"_id": entry_creation_result.data["_id"]})

    def _strategy_validate(self, entry: TimeEntry):
        """
        Validates a time entry using the strategy pattern.

        :param entry: The time entry to validate.
        :type entry: TimeEntry
        :return: A list of ValidationResult objects containing the results of the validation.
        :rtype: list[ValidationResult]
        """
        entry_validator = None
        if entry.entry_type == TimeEntryType.WORK_ENTRY:
            entry_validator = self.work_entry_validator
        elif entry.entry_type == TimeEntryType.VACATION_ENTRY:
            entry_validator = self.vacation_entry_validator

        if entry_validator is not None:
            strategy_validation_results = entry_validator.validate_entry(entry)
            return strategy_validation_results
        return []

    def create_work_entry(self, entry_data: dict, username: str) -> RequestResult:
        """
        Creates a new work time entry in the system based on the provided entry data.

        :param entry_data: A dictionary containing time entry attributes necessary for creating a new time entry.
        :type entry_data: dict
        :param username: The username of the user creating the time entry.
        :type username: str
        :return: A RequestResult object containing the result of the create operation.
        :rtype: RequestResult
        """
        return self._add_time_entry(entry_data, TimeEntryType.WORK_ENTRY, username)

    def create_vacation_entry(self, entry_data: dict, username: str) -> RequestResult:
        """
        Adds a new vacation time entry based on the provided entry data.

        :param entry_data: A dictionary containing vacation time entry attributes.
        :type entry_data: dict
        :param username: The username of the user creating the time entry.
        :type username: str
        :return: A RequestResult object containing the result of the add operation.
        :rtype: RequestResult
        """
        return self._add_time_entry(entry_data, TimeEntryType.VACATION_ENTRY, username)

    @jwt_required()
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

        timesheet_status = self.timesheet_service.get_timesheet_status(existing_entry_data['timesheetId']).data
        if timesheet_status == TimesheetStatus.COMPLETE or timesheet_status == TimesheetStatus.WAITING_FOR_APPROVAL:
            return RequestResult(False, "Cannot update time entry of a submitted timesheet", status_code=400)

        updated_entry_data = existing_entry_data.copy()
        updated_entry_data.update(update_data)

        # Validate input update data
        validation_result = self.entry_input_validator.is_valid(updated_entry_data)
        if validation_result.status == ValidationStatus.FAILURE:
            return RequestResult(False, validation_result.message, status_code=400)

        updated_time_entry = TimeEntry.from_dict(updated_entry_data)
        updated_time_entry.set_id(ObjectId(entry_id))
        if not updated_time_entry:
            return RequestResult(False, "Failed to construct updated time entry", status_code=500)
        existing_start_date = datetime.datetime.fromisoformat(str(existing_entry_data['startTime']))
        updated_start_date = updated_time_entry.start_time
        if existing_start_date.month != updated_start_date.month or existing_start_date.year != updated_start_date.year:
            return RequestResult(False, "Cannot update time entry to a different month or year", status_code=400)

        # Check if the update causes a duplicate entry on the same date
        existing_entries = self.time_entry_repository.get_time_entries_by_date(updated_start_date,
                                                                               get_jwt_identity())
        if existing_entries:
            # Filter out the current entry itself
            duplicate_entries = [entry for entry in existing_entries if str(entry["_id"]) != entry_id]
            if duplicate_entries:
                return RequestResult(False, "A time entry already exists for this date", status_code=409)

        # Validate the updated entry through strategy pattern
        strategy_validation_results = self._strategy_validate(updated_time_entry)
        for result in strategy_validation_results:
            if result.status == ValidationStatus.FAILURE:
                return RequestResult(False, result.message, status_code=400)

        repo_result = self.time_entry_repository.update_time_entry(updated_time_entry)

        if not repo_result.is_successful:  #pragma: no cover
            return repo_result

        self.timesheet_service.calculate_overtime(existing_entry_data['timesheetId'])

        if existing_entry_data['entryType'] == TimeEntryType.VACATION_ENTRY.value:
            existing_entry = VacationEntry.from_dict(existing_entry_data)
            update_entry = VacationEntry.from_dict(update_data)
            if update_entry.get_duration() < existing_entry.get_duration():
                self.user_service.add_vacation_minutes(get_jwt_identity(),
                                                        abs(existing_entry.get_duration() - update_entry.get_duration()))
            elif update_entry.get_duration() > existing_entry.get_duration():
                self.user_service.remove_vacation_minutes(get_jwt_identity(),
                                                          abs(update_entry.get_duration() - existing_entry.get_duration()))
        existing_entry = TimeEntry.from_dict(existing_entry_data)
        update_entry = TimeEntry.from_dict(update_data)
        if update_entry.get_duration() > existing_entry.get_duration():
            self.user_service.add_overtime_minutes(get_jwt_identity(),
                                                   abs(existing_entry.get_duration() - update_entry.get_duration()))
        elif update_entry.get_duration() < existing_entry.get_duration():
            self.user_service.remove_overtime_minutes(get_jwt_identity(),
                                                      abs(update_entry.get_duration() - existing_entry.get_duration()))
        result = self.timesheet_service.set_total_and_vacation_time(updated_time_entry.timesheet_id)
        if not result.is_successful:
            return result
        if validation_result.status == ValidationStatus.WARNING:
            return RequestResult(True, f"entry updated with warnings ´{validation_result.message}´",
                                 status_code=200)
        return repo_result

    @jwt_required()
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

        time_entry_data = self.time_entry_repository.get_time_entry_by_id(entry_id)
        if not time_entry_data:
            return RequestResult(False, "Time entry not found", status_code=404)
        timesheet_status = self.timesheet_service.get_timesheet_status(time_entry_data['timesheetId']).data
        if timesheet_status == TimesheetStatus.COMPLETE or timesheet_status == TimesheetStatus.WAITING_FOR_APPROVAL:
            return RequestResult(False, "Cannot delete time entry of a submitted timesheet", status_code=400)

        delete_result = self.time_entry_repository.delete_time_entry(entry_id)
        time_entry = TimeEntry.from_dict(time_entry_data)
        if time_entry_data['entryType'] == TimeEntryType.VACATION_ENTRY.value:
            self.user_service.add_vacation_minutes(get_jwt_identity(), time_entry.get_duration())

        self.user_service.remove_overtime_minutes(get_jwt_identity(), time_entry.get_duration())
        self.timesheet_service.calculate_overtime(time_entry_data['timesheetId'])

        result = self.timesheet_service.set_total_and_vacation_time(time_entry.timesheet_id)
        if not result.is_successful and delete_result.is_successful:
            result.message = "Time entry deleted, but total hours could not be updated."
            return result
        return delete_result

    def delete_time_entries_by_timesheet_id(self, timesheet_id: str) -> RequestResult:
        """
        Deletes all time entries of a user that is being deleted.

        :param timesheet_id: The id of the timesheet for which to delete all time entries.
        :type timesheet_id: str
        :return: A RequestResult object containing the result of the delete operation.
        :rtype: RequestResult
        """
        time_entries = self.time_entry_repository.get_time_entries_by_timesheet_id(timesheet_id)
        for entry in time_entries:
            entry_id = str(entry['_id'])
            delete_result = self.time_entry_repository.delete_time_entry(entry_id)
            if not delete_result.is_successful:
                return delete_result

        return RequestResult(True, "All time entries deleted successfully", status_code=200)

    def get_entries_of_timesheet(self, timesheet_id: str):
        """
        Retrieves a list of time entries associated with a specific timesheet ID and converts them into
        TimeEntry objects, considering the specific type of each entry.

        :param timesheet_id: The ID of the timesheet for which to retrieve entries.
        :type timesheet_id: str
        :return: A list of TimeEntry model instances representing all time entries for the specified timesheet.
        :rtype: RequestResult
        """

        entries_data = self.time_entry_repository.get_time_entries_by_timesheet_id(timesheet_id)

        if not entries_data:
            return RequestResult(is_successful=False, message="No entries found", status_code=404)
        time_entries = []
        for entry_data in entries_data:
            entry_type = TimeEntryType.get_type_by_value(entry_data['entryType'])
            if entry_type == TimeEntryType.WORK_ENTRY:
                time_entries.append(WorkEntry.from_dict(entry_data))
            elif entry_type == TimeEntryType.VACATION_ENTRY:
                time_entries.append(VacationEntry.from_dict(entry_data))

        sorted_time_entries = sorted(time_entries, key=lambda entry: entry.start_time, reverse=True)
        return RequestResult(is_successful=True, message="", status_code=200, data=sorted_time_entries)
