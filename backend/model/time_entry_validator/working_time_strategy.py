from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry import TimeEntry
from model.time_entry_validator.time_entry_strategy import TimeEntryStrategy
import datetime


class WorkingTimeStrategy(TimeEntryStrategy):
    """
    Strategy for validating TimeEntry objects to ensure they comply with standard business hours
    (8 AM to 6 PM) and do not exceed the maximum permitted working hours within a day.

    This strategy is particularly useful for organizations that adhere to strict working
    time regulations and wish to enforce compliance through time entry validations.
    """

    BUSINESS_START = datetime.time(6, 0)  # 8:00 AM (6:00 AM UTC)
    BUSINESS_END = datetime.time(16, 0)  # 6:00 PM (4:00 PM UTC)

    MAX_WORKING_HOURS = 8
    FAILURE_WORKING_HOURS = 10

    OUT_OF_BUSINESS_HOURS_THRESHOLD = 120

    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Validates a single TimeEntry against defined business hours and maximum working hours constraints.

        :param entry: The TimeEntry object to validate. It should have attributes for start and end times.
        :type entry: TimeEntry

        :return: A ValidationResult indicating whether the time entry meets the established business rules.
                 This includes validation against the start and end times for being within business hours,
                 and checking the total working hours against maximum thresholds.
        :rtype: ValidationResult

        Examples:
            - If a time entry starts at 7:55 AM (which is before 8 AM), this method will return a
              ValidationResult with a WARNING status indicating the time is outside standard business hours.
            - If a time entry represents 9 hours of work, this method will return a
              ValidationResult with a WARNING status due to exceeding the maximum allowable working hours.
            - If a time entry represents 11 hours of work, this method will return a
              ValidationResult with a FAILURE status due to exceeding the maximum allowable working hours.

        Notes:
            - Time entries within business hours but exceeding 8 hours will trigger a WARNING about long working hours.
            - Time entries that exceed 10 hours of work will receive a FAILURE status, as this is beyond
              the acceptable working time limit.
        """

        # Check if the entry is outside business hours
        total_outside_business_hours = 0

        # Convert business hours to datetime for comparison with entry times
        business_start_datetime = datetime.datetime.combine(entry.start_time.date(), self.BUSINESS_START)
        business_end_datetime = datetime.datetime.combine(entry.end_time.date(), self.BUSINESS_END)

        if entry.start_time < business_start_datetime:
            total_outside_business_hours += (business_start_datetime - entry.start_time).seconds // 60
        elif entry.start_time >= business_end_datetime:
            total_outside_business_hours += (entry.start_time - business_end_datetime).seconds // 60

        if entry.end_time > business_end_datetime:
            total_outside_business_hours += (entry.end_time - business_end_datetime).seconds // 60
        elif entry.end_time <= business_start_datetime:
            total_outside_business_hours += (business_start_datetime - entry.end_time).seconds // 60

        # Validate based on the total time outside business hours
        if total_outside_business_hours > self.OUT_OF_BUSINESS_HOURS_THRESHOLD:
            return ValidationResult(ValidationStatus.FAILURE,
                                    "Entry exceeds the allowed threshold for working outside business hours.")

        if total_outside_business_hours > 0:
            return ValidationResult(ValidationStatus.WARNING,
                                    "Entry is outside of standard business hours (8 AM to 6 PM).")

        # Validate maximum working hours
        work_duration = entry.get_duration()
        if work_duration > (self.MAX_WORKING_HOURS * 60):
            return ValidationResult(ValidationStatus.WARNING, "Working time exceeds the maximum allowed 8 hours.")

        if work_duration > (self.FAILURE_WORKING_HOURS * 60):
            return ValidationResult(ValidationStatus.FAILURE, "Working time exceeds the permitted 10 hours.")

        return ValidationResult(ValidationStatus.SUCCESS, "Time entry is valid.")
