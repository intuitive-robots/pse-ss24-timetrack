from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry import TimeEntry
from model.time_entry_type import TimeEntryType
from model.time_entry_validator.time_entry_strategy import TimeEntryStrategy


class BreakLengthStrategy(TimeEntryStrategy):
    """
    Strategy class for validating the break times of a TimeEntry according to work law regulations.
    Break lengths are determined based on the total duration of work, with thresholds that dictate
    the minimum required break length for different work durations.
    """

    DEFAULT_MINIMUM_BREAK_LENGTH = 0
    MIN_PER_HOUR = 60

    WORK_DURATION_THRESHOLDS = [
        (2, 0),  # Up to 2 hours, no break required
        (6, 15),  # Up to 6 hours, 15 minutes break (default minimum)
        (9, 30),  # More than 6 hours up to 9 hours, 30 minutes break
        (float('inf'), 45)  # More than 9 hours, 45 minutes break
    ]

    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Validates the break time specified in a TimeEntry object against legal requirements,
        based on the total duration of work performed. The method checks if the break time
        meets or exceeds the required duration specified by work duration thresholds.

        :param entry: The TimeEntry object containing details of the work duration and break time.
        :type entry: TimeEntry

        :return: ValidationResult indicating whether the break time is sufficient as per legal standards.
        :rtype: ValidationResult

        Usage:
            If the work duration is 6 hours and above, a break of 30 minutes or more is required,
            the validation will pass if the break time is equal to or more than the required break time,
            otherwise it will fail, providing a detailed message.
        """
        if entry.entry_type != TimeEntryType.WORK_ENTRY:
            return ValidationResult(ValidationStatus.SUCCESS, "Break length is not applicable for non-work entries.")

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
