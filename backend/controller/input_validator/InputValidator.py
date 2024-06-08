from controller.input_validator.ValidationResult import ValidationResult
from controller.input_validator.ValidationStatus import ValidationStatus


class InputValidator:
    """
    Base class for input validators.
    """

    def is_valid(self, data) -> ValidationResult:
        """
        Validate the input data. Should be overridden by subclasses.

        :param data: The data to validate
        :return: if data is valid, return True, otherwise False
        """
        if not data:
            return ValidationResult(ValidationStatus.SUCCESS, "No data provided")
