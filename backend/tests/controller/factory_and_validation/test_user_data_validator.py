import unittest

from controller.input_validator.user_data_validator import UserDataValidator
from controller.input_validator.validation_status import ValidationStatus
from utils.security_utils import SecurityUtils


class TestUserDataValidator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user_data_validator = UserDataValidator()

    def setUp(self):
        self.hiwi_user_data = {
            "username": "testHiwiUserDataValidator",
            "password": "test_password",
            "role": "Hiwi",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "LastName",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "contractInfo": {
                "hourlyWage": 12.40,
                "workingHours": 80
            },
            "supervisor": "testSupervisorUserService",
            "slackId": None,
            "accountCreation": None,
            "lastLogin": None
        }

    def test_is_valid_hiwi(self):
        """
        Test that is_valid returns a ValidationResult with SUCCESS status when user data is valid
        """
        validation_result = self.user_data_validator.is_valid(self.hiwi_user_data)
        self.assertEqual(validation_result.status, ValidationStatus.SUCCESS)
        self.assertEqual(validation_result.message, "User data is valid.")

    def test_is_valid_hiwi_missing_hourly_wage(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status and message "Missing or null hourlyWage in contractInfo." when hourlyWage is missing
        """
        self.hiwi_user_data["contractInfo"]["hourlyWage"] = None
        validation_result = self.user_data_validator.is_valid(self.hiwi_user_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message, "Missing or null hourlyWage in contractInfo.")

    def test_is_valid_hiwi_missing_working_hours(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status
         and message "Missing workingHours in contractInfo." when workingHours is missing
        """
        self.hiwi_user_data["contractInfo"]["workingHours"] = None
        validation_result = self.user_data_validator.is_valid(self.hiwi_user_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message,
                         "Invalid workingHours in contractInfo. Must be a positive number.")


    def test_is_valid_hiwi_missing_fields(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status and message "Missing <field> cannot be empty." when a field is missing
        """
        self.hiwi_user_data["username"] = ""
        validation_result = self.user_data_validator.is_valid(self.hiwi_user_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message, "username cannot be empty.")

    def test_is_valid_hiwi_first_name_missing(self):
        """
        Test that is_valid returns a ValidationResult with FAILURE status and message "Invalid or missing firstName." when firstName is missing
        """
        self.hiwi_user_data["personalInfo"]["firstName"] = ""
        validation_result = self.user_data_validator.is_valid(self.hiwi_user_data)
        self.assertEqual(validation_result.status, ValidationStatus.FAILURE)
        self.assertEqual(validation_result.message, "Invalid or missing personal info field: firstName.")
