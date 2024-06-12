import re
from datetime import datetime

from controller.input_validator.input_validator import InputValidator
from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry_type import TimeEntryType
from model.time_entry import TimeEntry


class TimeEntryDataValidator(InputValidator):
    def __init__(self):
        """
        Initializes the TimeEntryDataValidator with predefined regex patterns for validating time entry fields.
        """
        self.field_patterns = {
            'timesheetId': r'^[a-zA-Z0-9]{10}$',  # Alphanumeric exactly 10 characters long
            'activity': r'^[\w\s\-,.:;!?\']+$',  # Alphanumeric, whitespace, and selected punctuation
            'projectName': r'^[\w\s\-]+$',  # Alphanumeric, whitespace, hyphens, and underscores
            'breakTime': r'^\d+$'  # Non-negative integers (zero or more)
        }

    def is_valid(self, time_entry_data):
        """
        Validates the completeness and correctness of time entry data using keys from TimeEntry.dict_keys method.

        :param time_entry_data: A dictionary containing time entry details to validate.
        :return: ValidationResult indicating if the time entry data is valid.
        """
        required_keys = TimeEntry.dict_keys()
        missing_keys = [key for key in required_keys if key not in time_entry_data]
        if missing_keys:
            return ValidationResult(ValidationStatus.FAILURE, f"Missing required fields: {', '.join(missing_keys)}")

        # Check each field with a regex pattern if specified
        for field, pattern in self.field_patterns.items():
            if field in time_entry_data:
                if pattern and not re.match(pattern, time_entry_data[field]):
                    return ValidationResult(ValidationStatus.FAILURE, f"Invalid {field}.")

        # Validate dateTime fields if they are correctly typed and logically correct
        if 'startTime' in time_entry_data and 'endTime' in time_entry_data:
            if not (isinstance(time_entry_data['startTime'], datetime)
                    and isinstance(time_entry_data['endTime'], datetime)):
                return ValidationResult(ValidationStatus.FAILURE, "Start and end times must be datetime objects.")
            if time_entry_data['startTime'] >= time_entry_data['endTime']:
                return ValidationResult(ValidationStatus.FAILURE, "Start time must be earlier than end time.")

        # Validate entryType
        if 'entryType' in time_entry_data:
            if not TimeEntryType.get_type_by_value(time_entry_data['entryType']):
                return ValidationResult(ValidationStatus.FAILURE, "Invalid or unspecified entry type.")

        return ValidationResult(ValidationStatus.SUCCESS, "Time entry data is valid.")

    def _validate_entry_type(self, entry_type_value):
        """
        Validates that the provided entry type value represents a valid TimeEntryType.

        :param entry_type_value: The entry type value to validate.
        :return: Boolean indicating whether the entry type value is valid.
        """
        entry_type = TimeEntryType.get_type_by_value(entry_type_value)
        return entry_type is not None
