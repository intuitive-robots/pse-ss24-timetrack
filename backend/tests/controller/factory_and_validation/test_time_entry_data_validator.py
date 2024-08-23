import unittest
from datetime import datetime

from controller.input_validator.time_entry_data_validator import TimeEntryDataValidator
from controller.input_validator.validation_status import ValidationStatus


class TestTimeEntryDataValidator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.time_entry_data_validator = TimeEntryDataValidator()

    def setUp(self):
        self.time_entry_data = {'timesheetId': '60b1f7b3b6f1f3b3b3b3b3b3',
                                'startTime': datetime(2024, 6, 1, 8, 0, 0, 0),
                                'endTime': datetime(2024, 6, 1, 18, 0),
                                'entryType': 'Work Entry',
                                'breakTime': 60,
                                'activity': 'timeEntryServiceActivitiy',
                                'activityType': 'Projektbesprechung',
                                'projectName': 'timeEntryServiceTest'}

    def test_is_valid_work_entry(self):
        """
        Test that is_valid returns a ValidationResult with SUCCESS status when work entry data is valid
        """
        validation_result = self.time_entry_data_validator.is_valid(self.time_entry_data)
        self.assertEqual(validation_result.status, ValidationStatus.SUCCESS)
        self.assertEqual(validation_result.message, "Time entry data is valid.")

    def test_is_valid_invalid_type(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status and message "Invalid or unspecified entry type." when entryType is missing
        """
        del self.time_entry_data['entryType']
        validation_result = self.time_entry_data_validator.is_valid(self.time_entry_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message, "Invalid or unspecified entry type.")

    def test_is_valid_missing_field(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status and message "Missing required fields: endTime" when endTime is missing
        """
        del self.time_entry_data['endTime']
        validation_result = self.time_entry_data_validator.is_valid(self.time_entry_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message, "Missing required fields: endTime")

    def test_is_valid_invalid_field_data(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status and message "Invalid timesheetId." when timesheetId is invalid
        """
        self.time_entry_data['timesheetId'] = 'invalid'
        validation_result = self.time_entry_data_validator.is_valid(self.time_entry_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message, "Invalid timesheetId.")

    def test_is_valid_invalid_date_format(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status and message "Invalid startTime." when startTime is invalid
        """
        self.time_entry_data['startTime'] = 'invalid'
        validation_result = self.time_entry_data_validator.is_valid(self.time_entry_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message, "Invalid datetime format in startTime.")

    def test_is_valid_start_time_after_end_time(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status and message "Start time must be earlier than end time." when startTime is after endTime
        """
        self.time_entry_data['startTime'] = datetime(2024, 6, 1, 18, 0, 0, 0)
        validation_result = self.time_entry_data_validator.is_valid(self.time_entry_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message, "Start time must be earlier than end time.")
