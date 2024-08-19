from controller.input_validator.validation_status import ValidationStatus


class ValidationResult:
    """
    Represents the result of a validation operation, including the status and a message.

    :param status: The status of the validation, indicating success or failure.
    :param message: A message providing additional information about the validation result.

    :ivar status: Stores the status of the validation after the object is initialized.
    :ivar message: Stores the message providing details about the validation result.
    """

    def __init__(self, status: ValidationStatus, message: str):
        """
        Initializes a new instance of the ValidationResult class.

        :param status: The status of the validation.
        :param message: A message providing additional information about the validation result.
        """
        self.status = status
        self.message = message

    def __str__(self):
        """
        Returns a string representation of the ValidationResult.

        :return: A string describing the validation status and the message.
        """
        return f"ValidationResult(status={self.status.name}, message='{self.message}')"