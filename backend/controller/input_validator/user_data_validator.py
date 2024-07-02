import re

from controller.input_validator.input_validator import InputValidator
from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole


class UserDataValidator(InputValidator):
    """
    A class that validates user data against predefined regular expression patterns
    to ensure data conforms to the expected formats.
    """

    def __init__(self):
        """
        Initializes the UserDataValidator with predefined regex patterns for validating user data fields.
        """
        self.field_patterns = {
            'username': r'^[a-zA-Z0-9]+$',  # Only letters
            'password': r'.{8,}',  # At least 8 characters
            'firstName': r'^[a-zA-Z]{2,15}$',  # Only letters, 2-15 characters long
            'lastName': r'^[a-zA-Z]{2,20}$',  # Only letters, 2-20 characters long
            'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
            'personalNumber': r'^\d{4,10}$',  # 4 to 10 digits
            'instituteName': r'^[a-zA-Z\s]{2,30}$'  # Only letters and spaces, 2-20 characters long
        }

    def is_valid(self, user_data):
        """
        Validates the completeness and correctness of user data using regex.

        :param user_data: A dictionary containing user details to validate.
        :return: ValidationResult indicating if the user data is valid.
        """
        # Check role
        if 'role' in user_data and not self.validate_role(user_data['role']):
            return ValidationResult(ValidationStatus.FAILURE, "Invalid or unspecified user role.")

        # Validate fields with regex patterns
        for field, pattern in self.field_patterns.items():
            if field in user_data and not re.match(pattern, user_data[field]):
                return ValidationResult(ValidationStatus.FAILURE, f"Invalid or missing {field}.")

        # Validate personal information
        if 'personalInfo' in user_data:
            for field_key in PersonalInfo.dict_keys():
                pattern = self.field_patterns[field_key]
                if field_key in user_data['personalInfo'] and not re.match(pattern,
                                                                           user_data['personalInfo'][field_key]):
                    return ValidationResult(ValidationStatus.FAILURE,
                                            f"Invalid or missing personal info field: {field_key}.")

        return ValidationResult(ValidationStatus.SUCCESS, "User data is valid.")

    def validate_role(self, role: str):
        """
        Validates that the provided role value represents a valid UserRole.

        :param role: The role value to validate.
        :return: Boolean, True if the role value is valid, otherwise False.
        """
        role = UserRole.get_role_by_value(role)
        if role is None:
            return False
        return True
