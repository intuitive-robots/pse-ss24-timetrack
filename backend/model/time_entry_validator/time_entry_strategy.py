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
        Abstract method to validate a TimeEntry object. Subclasses must implement this method
        to provide specific validation behavior based on different rules or conditions.

        Each validation strategy derived from this class will implement this method to assess
        a TimeEntry object against specific criteria, determining if the entry meets the required
        validation standards.

        :param entry: The TimeEntry object to validate, which contains data such as start and end times,
                      break durations, and potentially other metadata pertinent to the validation logic.
        :type entry: TimeEntry

        :return: A ValidationResult object encapsulating the outcome of the validation process.
                 The result includes a status indicating success or failure and, optionally, a message
                 providing details about the validation outcome.
        :rtype: ValidationResult

        Example:
            - A `BreakLengthStrategy` might return a failure if the breaks are too short for the
              recorded working hours.
            - A `HolidayStrategy` might fail the validation if the work is recorded on a public holiday.

        Note:
            This method is abstract and must be overridden by subclasses; it should not be called directly.
        """
        pass
