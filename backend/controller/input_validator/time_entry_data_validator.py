import re
from datetime import datetime

from controller.input_validator.input_validator import InputValidator
from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry_type import TimeEntryType
from model.vacation_entry import VacationEntry
from model.work_entry import WorkEntry
from utils.object_utils import ObjectUtils


class TimeEntryDataValidator(InputValidator):
    """
    A validator class for time entry data in a project management system. This class
    checks the validity of different fields specific to time entries.
    """

    def __init__(self):
        """
        Initializes the TimeEntryDataValidator with predefined regex patterns for validating time entry fields.
        These patterns ensure that the input for various fields like timesheet ID and project name conforms
        to expected formats.
        """
        self.field_patterns = {
            'timesheetId': r'^[0-9a-fA-F]{24}$',  # Alphanumeric exactly 10 characters long
            'activity': r'^[\w\s\-,.:;!?\']+$',  # Alphanumeric, whitespace, and selected punctuation
            'projectName': r'^[\w\s\-]+$',  # Alphanumeric, whitespace, hyphens, and underscores
            # 'breakTime': r'^\d+$'  # Non-negative integers (zero or more)
            # 'startTime': r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$',
            # 'endTime': r'^^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$'
        }

    def is_valid(self, time_entry_data):
        """
        Validates the completeness and correctness of time entry data based on the entry type.

        :param time_entry_data: A dictionary containing time entry details to validate.
        :return: ValidationResult: An object indicating whether the time entry data is valid, including
                              a message and status code.
        """

        if 'entryType' not in time_entry_data or not TimeEntryType.get_type_by_value(time_entry_data['entryType']):
            return ValidationResult(ValidationStatus.FAILURE, "Invalid or unspecified entry type.")
        entry_class = self._get_entry_class(time_entry_data['entryType'])
        if not entry_class:
            return ValidationResult(ValidationStatus.FAILURE, "Invalid entry type specified.")
        required_keys = entry_class.dict_keys()
        required_keys.remove('_id')

        missing_keys = [key for key in required_keys if key not in time_entry_data]
        if missing_keys:
            return ValidationResult(ValidationStatus.FAILURE, f"Missing required fields: {', '.join(missing_keys)}")
        # Check each field with a regex pattern if specified
        for field, pattern in self.field_patterns.items():
            if not isinstance(pattern, str):
                continue
            if field in time_entry_data and not re.match(pattern, str(time_entry_data[field])):
                return ValidationResult(ValidationStatus.FAILURE, f"Invalid {field}.")
        date_fields = ['startTime', 'endTime']
        for field in date_fields:
            try:
                if isinstance(time_entry_data.get(field), str):
                    time_entry_data[field] = datetime.fromisoformat(time_entry_data[field].rstrip('Z'))
            except ValueError:
                return ValidationResult(ValidationStatus.FAILURE, f"Invalid datetime format in {field}.")
        if 'startTime' in time_entry_data and 'endTime' in time_entry_data:
            if not (isinstance(time_entry_data['startTime'], datetime) and isinstance(time_entry_data['endTime'],
                                                                                      datetime)):
                return ValidationResult(ValidationStatus.FAILURE,
                                        "DateTime objects required for startTime and endTime.")
            if time_entry_data['startTime'] >= time_entry_data['endTime']:
                return ValidationResult(ValidationStatus.FAILURE, "Start time must be earlier than end time.")
        not_required_fields = [field for field in time_entry_data if field not in required_keys and field != '_id']
        if not_required_fields:
            return ValidationResult(ValidationStatus.WARNING, f"Skipped fields: {', '.join(not_required_fields)}")
        return ValidationResult(ValidationStatus.SUCCESS, "Time entry data is valid.")

    def _get_entry_class(self, entry_type_value):
        """
        Maps entry type values to specific TimeEntry subclass.

        :param entry_type_value: The entry type value to use.
        :return: Corresponding TimeEntry subclass or None if invalid.
        """
        if entry_type_value == TimeEntryType.WORK_ENTRY.value:
            return WorkEntry
        elif entry_type_value == TimeEntryType.VACATION_ENTRY.value:
            return VacationEntry
        return None
    def _validate_entry_type(self, entry_type_value):
        """
        Validates that the provided entry type value represents a valid TimeEntryType.

        :param entry_type_value: The entry type value to validate.
        :return: Boolean indicating whether the entry type value is valid.
        """
        entry_type = TimeEntryType.get_type_by_value(entry_type_value)
        return entry_type is not None