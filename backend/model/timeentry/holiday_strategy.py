import holidays
from model.time_entry import TimeEntry
from model.timeentry.time_entry_strategy import TimeEntryStrategy
from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus


class HolidayStrategy(TimeEntryStrategy):
    """
    Validates that the TimeEntry is not made on a public holiday in Baden-Württemberg, Germany.
    """

    def __init__(self):
        """
        Initializes the HolidayStrategy with a holiday calendar specific to Baden-Württemberg.
        """
        self.holiday_calendar = holidays.DE(prov='BW')  # BW stands for Baden-Württemberg

    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Checks if the date of the entry falls on a public holiday.

        Args:
            entry (TimeEntry): The time entry to validate.

        Returns:
            ValidationResult: Indicates whether the entry date is a public holiday.
        """
        if entry.date in self.holiday_calendar:
            holiday_name = self.holiday_calendar.get(entry.date)
            return ValidationResult(ValidationStatus.FAILURE, f"Entry date is a public holiday: {holiday_name}.")

        return ValidationResult(ValidationStatus.SUCCESS, "Entry date is not a public holiday.")
