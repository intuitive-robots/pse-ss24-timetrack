import unittest

from controller.input_validator.input_validator import InputValidator
from controller.input_validator.validation_status import ValidationStatus


class TestInputValidator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_validator = InputValidator()

    def test_is_valid_data_none(self):
        """
        Test that is_valid returns a ValidationResult with SUCCESS status and message "No data provided" when data is None
        """
        validation_result = self.input_validator.is_valid(None)
        self.assertEqual(validation_result.status, ValidationStatus.SUCCESS)
        self.assertEqual(validation_result.message, "No data provided")