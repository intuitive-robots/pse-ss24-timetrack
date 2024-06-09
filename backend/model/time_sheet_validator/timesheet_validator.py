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
        Initializes the TimesheetValidator with an empty list of validation rules.
        """
        self.validationRules = []

    def addValidationRule(self, rule: TimesheetStrategy):
        """
        Adds a new validation rule to the validator.

        This method allows for adding custom rules that implement specific validation
        logic defined in separate classes. Each rule must have a `validate` method that
        accepts a `Timesheet` object as its parameter.

        Args:
            rule (TimesheetStrategy): A validation strategy instance that contains
            specific validation logic to apply to Timesheet objects.
        """
        self.validationRules.append(rule)

    def removeValidationRule(self, rule: TimesheetStrategy):
        """
        Removes a validation rule from the validator.

        This method allows for the dynamic removal of validation rules from the validator,
        useful for adapting the validation process to different contexts or requirements.

        Args:
            rule (TimesheetStrategy): The validation strategy instance to remove from the
            current set of validation rules.
        """
        self.validationRules.remove(rule)

    def validateTimesheet(self, timesheet: Timesheet):
        """
        Validates a `Timesheet` object using all the accumulated validation rules.

        This method iterates through each validation rule and applies its `validate` method
        to the provided `Timesheet` object. This is a way to enforce all validation rules
        that have been added to the validator.

        Args:
            timesheet (Timesheet): The `Timesheet` object to validate.

        Returns:
            list: A list of `ValidationResult` objects from each validation rule applied,
            indicating the success or failure of each validation.
        """
        results = []
        for rule in self.validationRules:
            result = rule.validate(timesheet)
            results.append(result)
        return results
