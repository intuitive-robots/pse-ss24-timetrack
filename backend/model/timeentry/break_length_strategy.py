from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry import TimeEntry
from model.timeentry.time_entry_strategy import TimeEntryStrategy


class BreakLengthStrategy(TimeEntryStrategy):
    """
    Validates the break times of a TimeEntry according to work law regulations.
    The law requires different break lengths based on the total duration of work,
    efficiently determined by iterating through a sorted list of thresholds.
    """

    DEFAULT_MINIMUM_BREAK_LENGTH = 0
    MIN_PER_HOUR = 60

    WORK_DURATION_THRESHOLDS = [
        (6, 15),  # Up to 6 hours, 15 minutes break (default minimum)
        (9, 30),  # More than 6 hours up to 9 hours, 30 minutes break
        (float('inf'), 45)  # More than 9 hours, 45 minutes break
    ]

    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Validates the break time in the TimeEntry based on the total work duration.

        Args:
            entry (TimeEntry): The entry to validate.

        Returns:
            ValidationResult: The result of the validation, indicating whether the
            break length meets the legal requirements.
        """
        if not hasattr(entry, 'break_time') or entry.break_time is None:
            return ValidationResult(ValidationStatus.FAILURE, "Break time information is missing or invalid.")

        work_duration_hours = entry.get_duration() / self.MIN_PER_HOUR

        required_break_length = self.DEFAULT_MINIMUM_BREAK_LENGTH
        for hours_threshold, break_length in self.WORK_DURATION_THRESHOLDS:
            if work_duration_hours <= hours_threshold:
                required_break_length = break_length
                break

        if entry.break_time < required_break_length:
            return ValidationResult(
                ValidationStatus.FAILURE,
                f"Break length of {entry.break_time} minutes is less than the required {required_break_length} "
                f"minutes for {work_duration_hours:.2f} hours of work."
            )

        return ValidationResult(ValidationStatus.SUCCESS, "Break length is valid according to work law regulations.")
