import re
from datetime import datetime

from controller.input_validator.input_validator import InputValidator
from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry_type import TimeEntryType


class TimeEntryDataValidator(InputValidator):
    def __init__(self):
        """
        Initializes the TimeEntryDataValidator with predefined regex patterns for validating time entry fields.
        """
        self.field_patterns = {
            'timesheetId': r'^[a-zA-Z0-9]{10}$',  # Assume timesheet IDs are alphanumeric with exactly 10 characters
            'startTime': None,  # Start time and end time are validated as datetime objects, not with regex
            'endTime': None,
            'entryType': None  # Entry type validated against the TimeEntryType enum
        }

    def is_valid(self, time_entry_data):
        """
        Validates the completeness and correctness of time entry data.

        :param time_entry_data: A dictionary containing time entry details to validate.
        :return: ValidationResult indicating if the time entry data is valid.
        """
        # Validate timesheetId with regex pattern
        if 'timesheetId' in time_entry_data:
            if not re.match(self.field_patterns['timesheetId'], time_entry_data['timesheetId']):
                return ValidationResult(ValidationStatus.FAILURE, "Invalid or missing timesheetId.")

        # Validate startTime and endTime as datetime objects
        if 'startTime' in time_entry_data and 'endTime' in time_entry_data:
            if not (isinstance(time_entry_data['startTime'], datetime) and isinstance(time_entry_data['endTime'],
                                                                                      datetime)):
                return ValidationResult(ValidationStatus.FAILURE, "Invalid start or end time.")
            if time_entry_data['startTime'] >= time_entry_data['endTime']:
                return ValidationResult(ValidationStatus.FAILURE, "Start time must be earlier than end time.")

        # Validate entryType against the TimeEntryType enum
        if 'entryType' in time_entry_data:
            if not TimeEntryType.get_type_by_value(time_entry_data['entryType']):
                return ValidationResult(ValidationStatus.FAILURE, "Invalid or unspecified entry type.")

        return ValidationResult(ValidationStatus.SUCCESS, "Time entry data is valid.")

    def validate_entry_type(self, entry_type_value):
        """
        Validates that the provided entry type value represents a valid TimeEntryType.

        :param entry_type_value: The entry type value to validate.
        :return: Boolean indicating whether the entry type value is valid.
        """
        entry_type = TimeEntryType.get_type_by_value(entry_type_value)
        return entry_type is not None
