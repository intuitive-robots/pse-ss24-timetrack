from abc import ABC, abstractmethod

from controller.input_validator.validation_result import ValidationResult
from model.time_entry import TimeEntry


class TimeEntryStrategy(ABC):
    """
    Abstract base class for defining validation strategies for TimeEntry objects.

    This class provides a framework for implementing various validation strategies
    as part of a strategy pattern in validating TimeEntry objects. Each subclass
    should provide a concrete implementation of the validate method that encapsulates
    the specific validation logic applicable to the TimeEntry being validated.
    """

    def __init__(self):
        """
        Initializes a new instance of a TimeEntryStrategy.

        """
        pass

    @abstractmethod
    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Abstract method to validate a TimeEntry object.

        Subclasses must implement this method to provide specific validation behavior.
        This method should examine the provided TimeEntry object and determine
        whether it complies with a particular rule or set of rules.

        :param entry (TimeEntry): The TimeEntry object to validate.

        Returns:
            ValidationResult: The result of the validation process, typically indicating
            whether the TimeEntry passed the specific validation and, if applicable,
            providing messages or codes that explain why the validation passed or failed.
        """
        pass
