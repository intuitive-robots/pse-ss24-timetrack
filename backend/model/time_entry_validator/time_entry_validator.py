from model.time_entry import TimeEntry


class TimeEntryValidator:
    """
    Manages the validation of `TimeEntry` objects against a set of defined validation rules.
    This validator uses a strategy pattern to allow for dynamic addition and removal of validation rules.

    Attributes:
        validationRules (list): A list of validation rules that `TimeEntry` objects will be checked against.
    """

    def __init__(self):
        """
        Initializes the TimeEntryValidator with an empty list of validation rules.
        """
        self.validationRules = []

    def add_validation_rule(self, rule):
        """
        Adds a new validation rule to the validator.

        This method allows for adding custom rules that implement specific validation
        logic defined in separate classes. Each rule must have a `validate` method that
        accepts a `TimeEntry` object as its parameter.

        Args:
            rule (TimeEntryStrategy): A validation strategy instance that contains specific validation logic to apply to TimeEntry objects.
        """
        self.validationRules.append(rule)

    def remove_validation_rule(self, rule):
        """
        Removes a validation rule from the validator.

        This method allows for the dynamic removal of validation rules from the validator,
        useful for adapting the validation process to different contexts or requirements.

        Args:
            rule (TimeEntryStrategy): The validation strategy instance to remove from the
            current set of validation rules.
        """
        self.validationRules.remove(rule)

    def validate_entry(self, timeEntry: TimeEntry):
        """
        Validates a `TimeEntry` object using all the accumulated validation rules.

        This method iterates through each validation rule and applies its `validate` method
        to the provided `TimeEntry` object. This is a way to enforce all validation rules
        that have been added to the validator.

        Args:
            timeEntry (TimeEntry): The `TimeEntry` object to validate.

        Returns:
            list: A list of `ValidationResult` objects from each validation rule applied,
            indicating the success or failure of each validation.
        """
        results = []
        for rule in self.validationRules:
            result = rule.validate(timeEntry)
            results.append(result)
        return results
