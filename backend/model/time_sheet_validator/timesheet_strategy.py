from abc import ABC, abstractmethod

from controller.input_validator.validation_result import ValidationResult
from model.timesheet import Timesheet


class TimesheetStrategy(ABC):
    """
    Abstract base class for defining validation strategies for Timesheet objects.

    This class provides a framework for implementing various validation strategies
    as part of a strategy pattern in validating Timesheet objects. Each subclass
    should provide a concrete implementation of the validate method that encapsulates
    the specific validation logic applicable to the Timesheet being validated.
    """

    def __init__(self):
        """
        Initializes a new instance of a TimesheetStrategy.

        This setup prepares the strategy for validation, ensuring that all necessary
        components or properties are initialized.
        """
        pass

    @abstractmethod
    def validate(self, timesheet: Timesheet) -> ValidationResult:
        """
        Abstract method to validate a Timesheet object.

        Subclasses must implement this method to provide specific validation behavior.
        This method should examine the provided Timesheet object and determine
        whether it complies with a particular rule or set of rules. The validation
        might consider factors such as total hours worked, compliance with labor laws,
        and adherence to project-specific time allocations.

        Args:
            timesheet (Timesheet): The Timesheet object to validate.

        Returns:
            ValidationResult: The result of the validation process, typically indicating
            whether the Timesheet passed the specific validation and, if applicable,
            providing messages or codes that explain why the validation passed or failed.
        """
        pass
