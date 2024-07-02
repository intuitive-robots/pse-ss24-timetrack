from abc import ABC, abstractmethod

from controller.input_validator.validation_result import ValidationResult
from model.time_entry import TimeEntry
from model.timesheet import Timesheet


class TimesheetStrategy(ABC):
    """
    Abstract base class for defining validation strategies for Timesheet objects. This class serves
    as a foundation for implementing various validation strategies as part of a strategy pattern,
    enabling dynamic validation logic tailored to specific requirements of Timesheet objects.

    Each subclass of TimesheetStrategy is expected to implement the `validate` method, which encapsulates
    the validation logic specific to the aspect of the timesheet that needs to be validated, such as
    adherence to working hours limits, validation of project-specific time allocations, or compliance
    with labor regulations.
    """

    def __init__(self):
        """
        Initializes a new instance of a TimesheetStrategy. This constructor can be overridden by
        subclasses to set up necessary configurations or initial state specific to the validation
        requirements.
        """
        pass

    @abstractmethod
    def validate(self, timesheet: Timesheet, time_entries: list[TimeEntry]) -> ValidationResult:
        """
        Abstract method that must be implemented by all subclasses to perform specific validation
        on a Timesheet object, taking into consideration all related TimeEntry records.

        This method evaluates the Timesheet and its associated TimeEntries against predefined
        validation criteria, which may vary depending on the specific implementation. For example,
        one strategy might check that the total hours recorded do not exceed legal work limits,
        while another could verify that time entries fall within approved project scopes.

        :param timesheet: The Timesheet object that is subject to validation. It represents a
                          collection of work records for a specific period.
        :type timesheet: Timesheet

        :param time_entries: A list of TimeEntry objects that belong to the timesheet. These are
                             the individual records of work that cumulatively make up the timesheet.
        :type time_entries: list[TimeEntry]

        :return: A ValidationResult object that indicates the outcome of the validation process.
                 This result includes a status (e.g., success, failure, or warning) and a message
                 detailing the reasons for the validation outcome.
        :rtype: ValidationResult

        Examples:
            - If timesheet hours exceed a regulatory or contractual limit, the validate method
              might return a ValidationResult with a FAILURE status and an appropriate message.
            - If all checks pass, the method would return a ValidationResult with a SUCCESS status.

        Note:
            This method is abstract and should be overridden in each subclass with specific logic
            appropriate to the particular validation being implemented.
        """
        pass
