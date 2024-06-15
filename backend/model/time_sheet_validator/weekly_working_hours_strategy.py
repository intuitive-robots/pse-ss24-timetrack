from collections import defaultdict

from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry import TimeEntry
from model.time_sheet_validator.timesheet_strategy import TimesheetStrategy
from model.timesheet import Timesheet


class WeeklyHoursStrategy(TimesheetStrategy):
    """
    A strategy for validating that the total weekly working hours recorded in a Timesheet do not exceed
    the maximum allowed hours. This is particularly important for compliance with labor regulations
    or contractual agreements that limit the amount of work hours per week.

    Attributes:
        MAX_WEEKLY_HOURS (int): The maximum number of hours an employee is allowed to work in a week.
                                This is set to 20 hours by default but should be configurable based
                                on organizational policies or labor law requirements.
    """

    MAX_WEEKLY_HOURS = 20  # TODO: Get the maximum weekly hours allowed by ContractInfo

    def validate(self, timesheet: Timesheet, time_entries: list[TimeEntry]) -> ValidationResult:
        """
        Validates the weekly working hours for each week within a Timesheet to ensure that no week's
        working hours exceed the set maximum. It organizes time entries by week and calculates the
        total hours worked per week.

        :param timesheet: The Timesheet object associated with the time entries being validated.
        :type timesheet: :class:`model.timesheet.Timesheet`

        :param time_entries: A list of TimeEntry objects that belong to the timesheet, to be aggregated into weekly totals.
        :type time_entries: list[:class:`model.time_entry.TimeEntry`]

        :return: A ValidationResult object that includes a status indicating whether the weekly hours are within
                 the acceptable range, and a message detailing the validation result.
        :rtype: :class:`controller.input_validator.validation_result.ValidationResult`

        Example:
            - If a week's total hours are 25, which exceeds the maximum of 20 hours, the validation will
              return a ValidationResult with a WARNING status and a message detailing the overage.
            - If all weeks are within the limit, it returns a ValidationResult with a SUCCESS status.
        """
        # Organize entries by week number
        weekly_hours = defaultdict(float)
        for entry in time_entries:
            week_number = entry.start_time.date().isocalendar()[1]
            weekly_hours[week_number] += entry.get_duration()

        # Validate weekly working hours for each week
        for week, hours in weekly_hours.items():
            if hours > self.MAX_WEEKLY_HOURS:
                return ValidationResult(
                    ValidationStatus.WARNING,
                    f"Week {week} working hours exceed the limit: {hours} hours recorded,"
                    f"but the limit is {self.MAX_WEEKLY_HOURS} hours."
                )

        return ValidationResult(ValidationStatus.SUCCESS, "All weekly working hours are within the acceptable limits.")

