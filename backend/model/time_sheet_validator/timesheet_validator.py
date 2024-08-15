from model.repository.time_entry_repository import TimeEntryRepository
from model.time_entry import TimeEntry
from model.time_sheet_validator.timesheet_strategy import TimesheetStrategy
from model.timesheet import Timesheet


class TimesheetValidator:
    """
    Manages the validation of `Timesheet` objects against a set of defined validation rules.
    This validator uses a strategy pattern to allow for dynamic addition and removal of validation rules.

    Attributes:
        validationRules (list): A list of validation rules that `Timesheet` objects will be checked against.
    """

    def __init__(self):
        """
        Initializes the TimesheetValidator with an empty list of validation rules, ready to be populated with
        specific validation strategies.
        """
        self.validationRules = []
        self.time_entry_repository = TimeEntryRepository()
        self.contract_info = None  # TODO: Add a ContractInfo object for working hours validation

    def add_validation_rule(self, rule: TimesheetStrategy):
        """
        Adds a new validation rule to the validator.

        This method allows for adding custom rules that implement specific validation
        logic defined in separate classes. Each rule must have a `validate` method that
        accepts a `Timesheet` object as its parameter.

        :param rule: The validation strategy to be added, which must implement the TimesheetStrategy interface.
        :type rule: :class:`~model.timesheet_strategy.TimesheetStrategy`
        """
        self.validationRules.append(rule)

    def remove_validation_rule(self, rule: TimesheetStrategy):
        """
        Removes a validation rule from the validator.

        This method allows for the dynamic removal of validation rules from the validator,
        useful for adapting the validation process to different contexts or requirements.

        :param rule: The validation strategy to be removed, which should currently be part of the validation rules.
        :type rule: TimesheetStrategy
        """
        self.validationRules.remove(rule)

    def validate_timesheet(self, timesheet: Timesheet):
        """
        Validates a given `Timesheet` object against all registered validation strategies to assess its compliance
        with each of the configured rules.

        :param timesheet: The `Timesheet` object to validate.
        :type timesheet: Timesheet

        :return: A list of `ValidationResult` instances, each representing the outcome from one of the validation
                 strategies applied to the `Timesheet`.
        :rtype: list[ValidationResult]

        Note:
            This method assumes that an external service (`time_entry_service`) is available to fetch time entries
            related to the timesheet, which are necessary for certain validations. The availability of this service
            and its proper function must be ensured before validation.
        """
        time_entries = self.time_entry_repository.get_time_entries_by_timesheet_id(timesheet.timesheet_id)
        time_entries = [TimeEntry.from_dict(time_entry) for time_entry in time_entries]

        results = []
        for rule in self.validationRules:
            result = rule.validate(timesheet, time_entries)
            results.append(result)
        return results
