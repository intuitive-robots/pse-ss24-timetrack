from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry import TimeEntry
from model.time_entry_validator.time_entry_strategy import TimeEntryStrategy
import datetime


class WorkingTimeStrategy(TimeEntryStrategy):
    """
    Validates that the time entry falls within the standard business hours (8 AM to 6 PM)
    and that the total working hours do not exceed 8 hours.
    """

    BUSINESS_START = datetime.time(8, 0)  # 8:00 AM
    BUSINESS_END = datetime.time(18, 0)  # 6:00 PM

    MAX_WORKING_HOURS = 8
    FAILURE_WORKING_HOURS = 10

    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Validates the time entry against business hours and maximum working hours constraints.

        Args:
            entry (TimeEntry): The time entry to validate.

        Returns:
            ValidationResult: The result of the validation.
        """
        # Validate business hours
        if not (self.BUSINESS_START <= entry.start_time < self.BUSINESS_END):
            return ValidationResult(ValidationStatus.WARNING,
                                    "Entry is outside of standard business hours (8 AM to 6 PM).")

        # Validate maximum working hours
        work_duration = entry.get_duration()
        if work_duration > self.MAX_WORKING_HOURS:
            return ValidationResult(ValidationStatus.WARNING, "Working time exceeds the maximum allowed 8 hours.")

        if work_duration > self.FAILURE_WORKING_HOURS:
            return ValidationResult(ValidationStatus.FAILURE, "Working time exceeds the permitted 10 hours.")

        return ValidationResult(ValidationStatus.SUCCESS, "Time entry is valid.")
