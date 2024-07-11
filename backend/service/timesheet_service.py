from bson import ObjectId

from model.repository.timesheet_repository import TimesheetRepository
from model.request_result import RequestResult
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus
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
        self.user_service = UserService()

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

    def sign_timesheet(self, timesheet_id: str):
        #TODO: first check if Hiwi has already uploaded signature
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
        return self._set_timesheet_status(timesheet_id, TimesheetStatus.WAITING_FOR_APPROVAL)

    def approve_timesheet(self, timesheet_id: str):
        """
        Method used by the supervisor to sign a timesheet.
        This sets the status to approved.

        :param timesheet_id: The ID of the timesheet to approve.
        :type timesheet_id: str
        :return: The result of the approval operation.
        :rtype: RequestResult
        """
        timesheet = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet is None:
            return RequestResult(False, "Timesheet not found", 404)
        if timesheet['status'] == 'Complete':
            return RequestResult(False, "Timesheet already approved", 409)
        if timesheet['status'] != 'Waiting for Approval':
            return RequestResult(False, "Timesheet cannot be approved", 400)
        return self._set_timesheet_status(timesheet_id, TimesheetStatus.COMPLETE)

    def request_change(self, timesheet_id: str):
        """
        Method used by the supervisor to request changes to a timesheet.
        This sets the status to change requested.

        :param timesheet_id: The ID of the timesheet to request changes for.
        :type timesheet_id: str
        :return: The result of the request change operation.
        :rtype: RequestResult
        """
        timesheet = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet is None:
            return RequestResult(False, "Timesheet not found", 404)
        if timesheet['status'] == 'Complete':
            return RequestResult(False, "Timesheet already approved", 409)
        if timesheet['status'] != 'Waiting for Approval':
            return RequestResult(False, "HiWi didn't submitted the timesheet", 400)
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
        result = self.timesheet_repository.create_timesheet(Timesheet(username, month, year))
        if result.is_successful:
            hiwi = self.user_service.get_profile(username)
            hiwi.add_timesheet(result.data["_id"])
            update_result = self.user_service.update_user(hiwi.to_dict())
            if not update_result.is_successful:
                self.timesheet_repository.delete_timesheet(result.data["_id"])
                return update_result

            return RequestResult(True, "Timesheet created", 201, {"_id": result.data["_id"]})

        return RequestResult(False, "Failed to create timesheet", 500)

    def delete_timesheet_by_id(self, timesheet_id: str):
        """
        Deletes a timesheet by its ID.

        :param timesheet_id: The ID of the timesheet
        :return: The result of the delete operation
        """
        timesheet_data = self.timesheet_repository.get_timesheet_by_id(timesheet_id)
        if timesheet_data is None:
            return RequestResult(False, "Timesheet not found", 404)
        result = self.timesheet_repository.delete_timesheet(timesheet_id)
        if result.is_successful:
            hiwi = self.user_service.get_profile(timesheet_data["username"])
            hiwi.remove_timesheet(ObjectId(timesheet_id))
            update_result = self.user_service.update_user(hiwi.to_dict())
            if not update_result.is_successful:
                return update_result
        return result

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
        return RequestResult(True, "", 200, sorted_timesheets )

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
        not_complete_timesheet_data = self.timesheet_repository.get_timesheets_by_username_status(username, TimesheetStatus.REVISION)
        not_complete_timesheet_data += self.timesheet_repository.get_timesheets_by_username_status(username, TimesheetStatus.WAITING_FOR_APPROVAL)
        not_complete_timesheet_data += self.timesheet_repository.get_timesheets_by_username_status(username, TimesheetStatus.NOT_SUBMITTED)
        timesheets = (Timesheet.from_dict(timesheet_data) for timesheet_data in not_complete_timesheet_data)
        sorted_timesheets = sorted(timesheets, key=lambda timesheet: (timesheet.year, timesheet.month))
        if sorted_timesheets is None or len(sorted_timesheets) == 0:
            return RequestResult(False, "No timesheets found", 404)
        return RequestResult(True, "", 200, sorted_timesheets[0])

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
