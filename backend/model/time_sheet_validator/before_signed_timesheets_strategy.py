from collections import defaultdict

from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry import TimeEntry
from model.time_sheet_validator.timesheet_strategy import TimesheetStrategy
from model.timesheet import Timesheet
import service.timesheet_service


class BeforeSignedTimesheetsStrategy(TimesheetStrategy):
    """
    A strategy for validating that all Timesheets before the current one have been completed.
    """

    def validate(self, timesheet: Timesheet, time_entries: list[TimeEntry]) -> ValidationResult:
        """
        Validates that all Timesheets before the current one have been completed.

        :param timesheet: The Timesheet object associated with the time entries being validated.
        :type timesheet: :class:`model.timesheet.Timesheet`

        :param time_entries: A list of TimeEntry objects that belong to the timesheet.
        :type time_entries: list[:class:`model.time_entry.TimeEntry`]

        :return: A ValidationResult object that includes a status indicating whether all previous Timesheets are completed,
                 and a message detailing the validation result.
        :rtype: :class:`controller.input_validator.validation_result.ValidationResult`
        """

        timesheet_service = service.timesheet_service.TimesheetService()
        timesheets = timesheet_service.get_timesheets_by_username(timesheet.username).data
        previous_timesheet = None
        for i, ts in enumerate(timesheets):
            if ts.timesheet_id == timesheet.timesheet_id:
                if i + 1 < len(timesheets):
                    previous_timesheet = timesheets[i + 1]
                break

        if previous_timesheet is None:
            return ValidationResult(ValidationStatus.SUCCESS, "No previous Timesheets found.")
        if previous_timesheet.status.value == "Complete":
            return ValidationResult(ValidationStatus.SUCCESS, "All previous Timesheets are completed.")
        else:
            return ValidationResult(ValidationStatus.FAILURE, "A previous Timesheet is not completed.")

