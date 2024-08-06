import math

from bson import ObjectId

from model.repository.time_entry_repository import TimeEntryRepository
from model.repository.timesheet_repository import TimesheetRepository
from model.request_result import RequestResult
from model.time_entry import TimeEntry
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus
from service.notification_service import NotificationService
from service.user_service import UserService


#TODO: Calculate proper overtime - take a look at the documentData class
class TimesheetService:
    """
    Provides service-layer functionality to handle timesheet-related operations, such as creating,
    updating, retrieving, and managing timesheets and their statuses. This service works with the
    TimesheetRepository to interact with the model-data layer.
    """

    def __init__(self):
        self.timesheet_repository = TimesheetRepository.get_instance()
        self.time_entry_repository = TimeEntryRepository.get_instance()
        self.user_service = UserService()
        self.time_entry_repository = TimeEntryRepository.get_instance()
        self.notification_service = NotificationService()

    def ensure_timesheet_exists(self, username: str, month: int, year: int):
        """
        Ensures that a timesheet exists for the given username, month, and year.
        If the timesheet does not exist, it will be created.

        :param username: The username of the Hiwi.
        :type username: str
        :param month: The month of the timesheet.
        :type month: int
        :param year: The year of the timesheet.
        :type year: int
        :return: A RequestResult object containing the result of the ensure operation.
        :rtype: RequestResult
        """
        timesheet = self.timesheet_repository.get_timesheet(username, month, year)
        if timesheet is not None:
            return RequestResult(True, "Timesheet already exists", 200)
        creation_result = self._create_timesheet(username, month, year)
        if creation_result.status_code == 201:
            return RequestResult(True, "Timesheet created", 201)
        return RequestResult(False, "Failed to create timesheet", 500)

    def set_total_time(self, timesheet_id: str):
        """
        Updates the total hours of a timesheet based on the sum of all its time entries.

        :param timesheet_id: The ID of the timesheet to update.
        :type timesheet_id: str
        """
        time_entries_data = self.time_entry_repository.get_time_entries_by_timesheet_id(timesheet_id)
        time_entries = [TimeEntry.from_dict(entry_data) for entry_data in time_entries_data]
        total_time = sum([entry.get_duration() for entry in time_entries])
        timesheet = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if not timesheet:
            return RequestResult(False, "Timesheet not found", 404)
        timesheet['totalTime'] = total_time
        result = self.timesheet_repository.update_timesheet_by_dict(timesheet)
        if result.is_successful:
            return RequestResult(True, "Total time updated", 200)
        return RequestResult(False, "Failed to update total time", 500)

    def sign_timesheet(self, timesheet_id: str):
        """
        Method used by the Hiwi to sign his timesheet.

        :param timesheet_id: The ID of the timesheet to sign.
        :type timesheet_id: str
        :return: The result of the sign operation.
        :rtype: RequestResult
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)

        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        if timesheet_data['status'] in (TimesheetStatus.WAITING_FOR_APPROVAL.value, TimesheetStatus.COMPLETE.value):
            return RequestResult(False, "Timesheet already signed", 409)
        hiwi_data = self.user_service.get_profile(timesheet_data["username"])
        if hiwi_data is None:
            return RequestResult(False, "HiWi not found", 404)
        supervisor_username = hiwi_data.supervisor
        if supervisor_username is None:
            return RequestResult(False, "Supervisor not found", 404)
        hiwi_full_name = hiwi_data.personal_info.first_name + " " + hiwi_data.personal_info.last_name
        notification_result = self.notification_service.send_notification({"receiver": supervisor_username,
                                                                           "message_type": "Timesheet Status Change",
                                                                           "message":
                                                                               f"Signed Timesheet: \n"
                                                                               f"{hiwi_full_name} signed timesheet \n"
                                                                               f"{timesheet_data['month']}/"
                                                                               f"{timesheet_data['year']}"})

        return self._set_timesheet_status(timesheet_id, TimesheetStatus.WAITING_FOR_APPROVAL)

    def approve_timesheet(self, timesheet_id: str):
        """
        Method used by the supervisor to sign a timesheet_data.
        This sets the status to approved.

        :param timesheet_id: The ID of the timesheet_data to approve.
        :type timesheet_id: str
        :return: The result of the approval operation.
        :rtype: RequestResult
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        if timesheet_data['status'] == 'Complete':
            return RequestResult(False, "Timesheet already approved", 409)
        if timesheet_data['status'] != 'Waiting for Approval':
            return RequestResult(False, "Timesheet cannot be approved", 400)
        notification_result = self.notification_service.send_notification({"receiver": timesheet_data["username"],
                                                                           "message_type": "Timesheet Status Change",
                                                                           "message": f"Timesheet approved and "
                                                                                      f"marked as completed: \n"
                                                                                      f"{timesheet_data['month']}/"
                                                                                      f"{timesheet_data['year']}"})
        return self._set_timesheet_status(timesheet_id, TimesheetStatus.COMPLETE)

    def request_change(self, timesheet_id: str):
        """
        Method used by the supervisor to request changes to a timesheet_data.
        This sets the status to change requested.

        :param timesheet_id: The ID of the timesheet_data to request changes for.
        :type timesheet_id: str
        :return: The result of the request change operation.
        :rtype: RequestResult
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        if timesheet_data['status'] == 'Complete':
            return RequestResult(False, "Timesheet already approved", 409)
        if timesheet_data['status'] != 'Waiting for Approval':
            return RequestResult(False, "HiWi didn't submitted the timesheet_data", 400)
        hiwi_data = self.user_service.get_profile(timesheet_data["username"])
        if hiwi_data is None:
            return RequestResult(False, "HiWi not found", 404)
        supervisor = self.user_service.get_profile(hiwi_data.supervisor)
        if supervisor is None:
            return RequestResult(False, "Supervisor not found", 404)
        supervisor_full_name = supervisor.personal_info.first_name + " " + supervisor.personal_info.last_name

        notification_result = self.notification_service.send_notification({"receiver": timesheet_data["username"],
                                                                           "message_type": "Timesheet Status Change",
                                                                           "message": f"Change Requested: \n"
                                                                                      f"{supervisor_full_name} requested changes to your timesheet \n:"
                                                                                      f"{timesheet_data['month']}/"
                                                                                      f"{timesheet_data['year']}"})
        return self._set_timesheet_status(timesheet_id, TimesheetStatus.REVISION)

    def _set_timesheet_status(self, timesheet_id: str, status: TimesheetStatus):
        """
        Sets the status of a timesheet.
        
        :param timesheet_id: The ID of the timesheet to update
        :param status: The new status of the timesheet
        :return: The result of the status update operation
        """
        return self.timesheet_repository.set_timesheet_status(timesheet_id, status)

    def _create_timesheet(self, username: str, month: int, year: int):
        """
        Creates a new timesheet.
        
        :param username: The username of the Hiwi
        :param month: The month of the timesheet
        :param year: The year of the timesheet
        :return: The result of the create operation
        """
        self.user_service.add_vacation_minutes(username)

        result = self.timesheet_repository.create_timesheet(Timesheet(username, month, year))
        if result.is_successful:
            hiwi = self.user_service.get_profile(username)
            hiwi.add_timesheet(result.data["_id"])
            update_result = self.user_service.update_user(hiwi.to_dict())
            monthly_working_hours = hiwi.contract_info.working_hours
            self.user_service.remove_overtime_minutes(username, monthly_working_hours * 60)
            if not update_result.is_successful:
                self.timesheet_repository.delete_timesheet(result.data["_id"])
                return update_result
            return RequestResult(True, "Timesheet created", 201, {"_id": result.data["_id"]})
        return RequestResult(False, "Failed to create timesheet", 500)
    def calculate_overtime(self, timesheet_id):
        """
        Calculates the overtime for a timesheet.

        :param timesheet_id: The ID of the timesheet
        :return: The result of the overtime calculation
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        timee_entries_data = self.time_entry_repository.get_time_entries_by_timesheet_id(timesheet_id)
        if timee_entries_data is None:
            return RequestResult(False, "No time entries found", 404)
        total_minutes = 0
        for entry in timee_entries_data:
            time_entry = TimeEntry.from_dict(entry)
            total_minutes += time_entry.get_duration()
        hiwi = self.user_service.get_profile(timesheet_data["username"])
        monthly_working_hours = hiwi.contract_info.working_hours
        previous_overtime = self.get_previous_overtime(timesheet_data["username"], timesheet_data["month"],
                                                       timesheet_data["year"])
        overtime_minutes = total_minutes - (monthly_working_hours * 60) + previous_overtime
        timesheet_data["overtime"] = overtime_minutes
        if timesheet_data["status"] != TimesheetStatus.COMPLETE.value:
            self.timesheet_repository.update_timesheet_by_dict(timesheet_data)
            return RequestResult(True, "", 200, overtime_minutes)
        return RequestResult(False, "Overtime can't be edited when Timesheet is complete", 409)

    def get_previous_overtime(self, username: str, current_month: int, current_year: int):
        """
        Retrieves the overtime from the previous month for a Hiwi.

        :param username: The username of the Hiwi
        :param current_month: The current month
        :param current_year: The current year
        :return: The overtime from the previous month
        """
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1
        timesheet_data = self.timesheet_repository.get_timesheet(username, previous_month, previous_year)
        if timesheet_data is None:
            return 0
        return timesheet_data.get("overtime", 0)

    def delete_timesheet_by_id(self, timesheet_id: str):
        """
        Deletes a timesheet by its ID.

        :param timesheet_id: The ID of the timesheet
        :return: The result of the delete operation
        """

        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        self.user_service.remove_vacation_minutes(timesheet_data["username"])
        result = self.timesheet_repository.delete_timesheet(timesheet_id)
        if result.is_successful:
            hiwi = self.user_service.get_profile(timesheet_data["username"])
            hiwi.remove_timesheet(ObjectId(timesheet_id))
            monthly_working_hours = hiwi.contract_info.working_hours
            self.user_service.add_overtime_minutes(timesheet_data["username"], monthly_working_hours * 60)
            update_result = self.user_service.update_user(hiwi.to_dict())
            if not update_result.is_successful:
                return update_result
        return result

    def delete_timesheets_by_username(self, username: str):
        """
        Deletes all timesheets for a given username.

        :param username: The username of the Hiwi
        :return: The result of the delete operation
        """
        timesheets_data = self.timesheet_repository.get_timesheets_by_username(username)
        if timesheets_data is None or len(timesheets_data) == 0:
            return RequestResult(True, "No timesheets to delete", 200)
        for timesheet_data in timesheets_data:
            result = self.delete_timesheet_by_id(timesheet_data["_id"])
            if not result.is_successful:
                return result
        return RequestResult(True, "Timesheets deleted", 200)

    def get_timesheet_by_id(self, timesheet_id: str):
        """
        Retrieves a timesheet by its ID.
        
        :param timesheet_id: The ID of the timesheet
        :return: A RequestResult object with the timesheet object in the data field if it was found.
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
        timesheets = list(map(Timesheet.from_dict, timesheets_data))
        sorted_timesheets = sorted(timesheets, key=lambda x: (x.year, x.month), reverse=True)
        return RequestResult(True, "", 200, sorted_timesheets)

    def get_timesheets_by_username_status(self, username: str, status: TimesheetStatus):
        """
        Retrieves all timesheets for a given username and status.
        
        :param username: The username of the Hiwi
        :param status: The status of the timesheets
        :return: A list of timesheet objects
        """
        timesheets_data = self.timesheet_repository.get_timesheets_by_username_status(username, status)
        if timesheets_data is None or len(timesheets_data) == 0:
            return RequestResult(False, "No timesheets found", 404)
        return RequestResult(True, "", 200, list(map(Timesheet.from_dict, timesheets_data)))

    def get_timesheet_id(self, username: str, month: int, year: int):
        """
        Retrieves the ID of a timesheet.
        
        :param username: The username of the Hiwi
        :param month: The month of the timesheet
        :param year: The year of the timesheet
        :return: The ID of the timesheet
        """
        timesheet_id = self.timesheet_repository.get_timesheet_id(username, month, year)
        if timesheet_id is None:
            return RequestResult(False, "Timesheet not found", 404)
        return RequestResult(True, "", 200, timesheet_id)

    def get_timesheet_status(self, timesheet_id: str):
        """
        Retrieves the status of a timesheet.

        :param timesheet_id: The ID of the timesheet
        :return: The status of the timesheet
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        return RequestResult(True, "", 200, TimesheetStatus(timesheet_data["status"]))

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

    def get_highest_priority_timesheet(self, username: str):
        """
        Retrieves the highest priority timesheet for a given username.

        :param username: The username of the Hiwi
        :return: The timesheet object
        """
        if username is None:
            return RequestResult(False, "Please provide a username to retrieve the timesheet", 400)
        timesheet_data = self.timesheet_repository.get_timesheets_by_username(username)
        timesheets = [Timesheet.from_dict(timesheet_data) for timesheet_data in timesheet_data]
        sorted_timesheets = sorted(timesheets, key=lambda timesheet: (
            self._get_status_priority(timesheet.status), timesheet.year, timesheet.month))
        if sorted_timesheets is None or len(sorted_timesheets) == 0:
            return RequestResult(False, "No timesheets found", 404)
        if sorted_timesheets[0].status == TimesheetStatus.COMPLETE:
            return RequestResult(True, "", 200, sorted_timesheets[-1])
        return RequestResult(True, "", 200, sorted_timesheets[0])

    def _get_status_priority(self, status: TimesheetStatus): #pragma: no cover
        if status == TimesheetStatus.REVISION:
            return 1
        elif status == TimesheetStatus.NOT_SUBMITTED:
            return 2
        elif status == TimesheetStatus.WAITING_FOR_APPROVAL:
            return 3
        elif status == TimesheetStatus.COMPLETE:
            return 4

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
