from collections import defaultdict

from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry import TimeEntry
from model.time_sheet_validator.timesheet_strategy import TimesheetStrategy
from model.timesheet import Timesheet


class WeeklyHoursStrategy(TimesheetStrategy):
    """
    Validates the total weekly working hours in a Timesheet do not exceed the maximum allowed hours,
    considering all entries grouped by weeks within a single month.
    """

    MAX_WEEKLY_HOURS = 20  # TODO: Get the maximum weekly hours allowed by ContractInfo

    def validate(self, timesheet: Timesheet, time_entries: list[TimeEntry]) -> ValidationResult:
        """
        Validates that the total hours logged for each week within a month do not exceed the legal or organizational limits.

        Args:
            timesheet (Timesheet): The Timesheet object associated with the entries.
            time_entries (list[TimeEntry]): A list of all TimeEntry objects for the month.

        Returns:
            ValidationResult: The result of the validation process. Returns failure if any week's hours exceed the limit.
        """
        # Organize entries by week number
        weekly_hours = defaultdict(float)
        for entry in time_entries:
            week_number = entry.date.isocalendar()[1]
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

