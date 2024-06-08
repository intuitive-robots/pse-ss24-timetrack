from controller.input_validator.validation_status import ValidationStatus


class ValidationResult:
    """
    Represents the result of a validation operation, including the status and a message.

    Attributes:
        status: The status of the validation, indicating success or failure.
        message: A message providing additional information about the validation result.
    """

    def __init__(self, status: ValidationStatus, message: str):
        """
        Initializes a new instance of the ValidationResult class.

        :param status: The status of the validation.
        :param message: A message providing additional information about the validation result.
        """
        self.status = status
        self.message = message
