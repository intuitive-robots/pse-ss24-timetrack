from datetime import datetime
from model.time_entry import TimeEntry
from model.time_entry_validator.time_entry_strategy import TimeEntryStrategy
from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus


class WeekendStrategy(TimeEntryStrategy):
    """
    Strategy for validating TimeEntry objects to ensure they do not fall on weekends.
    This strategy checks if the entry's date is a Saturday or Sunday and blocks it
    if it does.
    """

    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Validates a given TimeEntry to check if it occurs on a weekend (Saturday or Sunday).
        If the date of the time entry is a weekend, the validation will fail.

        :param entry: The TimeEntry object whose date needs to be validated against weekend days.
        :type entry: TimeEntry

        :return: A ValidationResult object that indicates whether the entry date is on a weekend.
                 It returns failure if the date is on a Saturday or Sunday.
        :rtype: ValidationResult
        """
        day_of_week = entry.start_time.weekday()  # 5 = Saturday, 6 = Sunday
        if day_of_week == 5:  # Saturday
            return ValidationResult(ValidationStatus.FAILURE,
                                    "Working on weekends is not allowed by institute policy: Saturday.")
        elif day_of_week == 6:  # Sunday
            return ValidationResult(ValidationStatus.FAILURE,
                                    "Working on weekends is not allowed by institute policy: Sunday.")

        return ValidationResult(ValidationStatus.SUCCESS, "Entry date is a weekday.")
