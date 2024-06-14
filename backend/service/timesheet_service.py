from model.repository.timesheet_repository import TimesheetRepository
from model.request_result import RequestResult
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus

#TODO: Calculate proper overtime - take a look at the documentData class
class TimesheetService:
    def __init__(self):
        self.timesheet_repository = TimesheetRepository.get_instance()

    def ensure_timesheet_exists(self, username: str, month: int, year: int):
        """
        Ensures that a timesheet exists for the given username, month, and year.
        If the timesheet does not exist, it will be created.
        :param username: Username of the Hiwi
        :param month: Month of the timesheet
        :param year: Year of the timesheet
        :return: The timesheet object
        """
        timesheet = self.timesheet_repository.get_timesheet(username, month, year)
        if timesheet is not None:
            return RequestResult(True, "Timesheet already exists", 200)
        creation_result = self.timesheet_repository.create_timesheet(Timesheet(username, month, year))
        if creation_result.status_code == 201:
            return RequestResult(True, "Timesheet created", 201)
        return RequestResult(False, "Failed to create timesheet", 500)

    def sign_timesheet(self, timesheet_id: str):
        """
        Method used by the Hiwi to sign his timesheet
        :param timesheet_id: The ID of the timesheet to sign
        :return: The result of the sign operation
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)

        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        if timesheet_data['status'] in (TimesheetStatus.WAITING_FOR_APPROVAL.value, TimesheetStatus.COMPLETE.value):
            return RequestResult(False, "Timesheet already signed", 409)
        return self.set_timesheet_status(timesheet_id, TimesheetStatus.WAITING_FOR_APPROVAL)

    def approve_timesheet(self, timesheet_id: str):
        """
        Method used by the supervisor to sign a timesheet.
        This sets the status to approved.
        :param timesheet_id: The ID of the timesheet to approve
        :return: The result of the approval operation
        """
        timesheet = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet is None:
            return RequestResult(False, "Timesheet not found", 404)
        if timesheet['status'] == 'Complete':
            return RequestResult(False, "Timesheet already approved", 409)
        if timesheet['status'] != 'Waiting for Approval':
            return RequestResult(False, "Timesheet cannot be approved", 400)
        return self.set_timesheet_status(timesheet_id, TimesheetStatus.COMPLETE)

    def request_change(self, timesheet_id: str):
        """
        Method used by the supervisor to request changes to a timesheet.
        This sets the status to change requested.
        :param timesheet_id: The ID of the timesheet to request changes for
        :return: The result of the request change operation
        """
        timesheet = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet is None:
            return RequestResult(False, "Timesheet not found", 404)
        if timesheet['status'] == 'Complete':
            return RequestResult(False, "Timesheet already approved", 409)
        if timesheet['status'] != 'Waiting for Approval':
            return RequestResult(False, "HiWi didn't submitted the timesheet", 400)
        return self.set_timesheet_status(timesheet_id, TimesheetStatus.REVISION)

    def set_timesheet_status(self, timesheet_id: str, status: TimesheetStatus):
        """
        Sets the status of a timesheet.
        :param timesheet_id: The ID of the timesheet to update
        :param status: The new status of the timesheet
        :return: The result of the status update operation
        """
        return self.timesheet_repository.set_timesheet_status(timesheet_id, status)

    def create_timesheet(self, username: str, month: int, year: int):
        """
        Creates a new timesheet.
        :param username: The username of the Hiwi
        :param month: The month of the timesheet
        :param year: The year of the timesheet
        :return: The result of the create operation
        """
        return self.timesheet_repository.create_timesheet(Timesheet(username, month, year))

    def get_timesheet_by_id(self, timesheet_id: str):
        """
        Retrieves a timesheet by its ID.
        :param timesheet_id: The ID of the timesheet
        :return: The timesheet object
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        return RequestResult(True, "", 200, Timesheet.from_dict(timesheet_data))

    def get_timesheets_by_username(self, username: str):
        """
        Retrieves all timesheets for a given username.
        :param username: The username of the Hiwi
        :return: A list of timesheet objects
        """
        timesheets_data = self.timesheet_repository.get_timesheets_by_username(username)
        if timesheets_data is None or len(timesheets_data) == 0:
            return RequestResult(False, "No timesheets found", 404)
        return RequestResult(True, "", 200, list(map(Timesheet.from_dict, timesheets_data)))

    def get_timesheets_by_username_status(self, username: str, status: TimesheetStatus):
        """
        Retrieves all timesheets for a given username and status.
        :param username: The username of the Hiwi
        :param status: The status of the timesheets
        :return: A list of timesheet objects
        """
        timesheets_data = self.timesheet_repository.get_timesheets_by_username_status(username, status)
        return list(map(Timesheet.from_dict, timesheets_data))

    def get_timesheet_id(self, username: str, month: int, year: int):
        """
        Retrieves the ID of a timesheet.
        :param username: The username of the Hiwi
        :param month: The month of the timesheet
        :param year: The year of the timesheet
        :return: The ID of the timesheet
        """
        return self.timesheet_repository.get_timesheet_id(username, month, year)

    def add_time_entry_to_timesheet(self, timesheet_id: str, time_entry_id: str):
        """
        Adds a time entry to a timesheet_data.
        :param timesheet_id: The ID of the timesheet_data
        :param time_entry_id: The ID of the time entry
        :return: The result of the add operation
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)

        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        timesheet = Timesheet.from_dict(timesheet_data)
        timesheet.add_time_entry(time_entry_id)
        return self.timesheet_repository.update_timesheet(timesheet)

    def delete_time_entry_from_timesheet(self, timesheet_id: str, time_entry_id: str):
        """
        Removes a time entry from a timesheet.
        :param timesheet_id: The ID of the timesheet
        :param time_entry_id: The ID of the time entry
        :return: The result of the remove operation
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        timesheet = Timesheet.from_dict(timesheet_data)
        timesheet.remove_time_entry(time_entry_id)
        return self.timesheet_repository.update_timesheet(timesheet)

    def get_current_timesheet(self, username: str):
        """
        Retrieves the current timesheet for a given username.
        :param username: The username of the Hiwi
        :return: The timesheet object
        """
        if username is None:
            return RequestResult(False, "Please provide a username to retrieve the timesheet", 400)
        current_timesheet_data = self.timesheet_repository.get_current_timesheet(username)
        if current_timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        return RequestResult(True, "", 200, Timesheet.from_dict(current_timesheet_data))

    def get_timesheet(self, username: str, month: int, year: int):
        """
        Retrieves a timesheet by username, month, and year.
        :param username: The username of the Hiwi
        :param month: The month of the timesheet
        :param year: The year of the timesheet
        :return: The timesheet object
        """
        if username is None or month is None or year is None:
            return RequestResult(False, "Please provide a username, month, and year to retrieve the timesheet", 400)
        timesheet_data = self.timesheet_repository.get_timesheet(username,
                                                                 month, year)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        return RequestResult(True, "", 200,
                             Timesheet.from_dict(timesheet_data))
