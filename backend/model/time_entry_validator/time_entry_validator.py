from model.time_entry import TimeEntry


class TimeEntryValidator:
    """
    Handles the validation of `TimeEntry` objects against a set of dynamically manageable validation rules.
    This class utilizes a strategy pattern to facilitate the flexible addition and removal of validation strategies,
    enabling custom validation scenarios for different types of time entries.

    Attributes:
        validationRules (list): A list of validation rules that `TimeEntry` objects will be checked against.
    """

    def __init__(self):
        """
        Constructs a TimeEntryValidator with an empty list, ready to accept validation strategies.
        """
        self.validationRules = []
        # working_time_strategy = WorkingTimeStrategy()
        # holiday_strategy = HolidayStrategy()
        # break_length_strategy = BreakLengthStrategy()
        # self.add_validation_rule(working_time_strategy)
        # self.add_validation_rule(holiday_strategy)
        # self.add_validation_rule(break_length_strategy)

    def add_validation_rule(self, rule):
        """
        Adds a new validation strategy to the list of rules. Each strategy must be an object that
        implements a `validate` method capable of processing a `TimeEntry` object.

        :param rule: A validation strategy instance, typically derived from the TimeEntryStrategy class,
                     which includes specific validation logic for TimeEntry objects.
        :type rule: TimeEntryStrategy
        """
        self.validationRules.append(rule)

    def remove_validation_rule(self, rule):
        """
        Removes a specified validation strategy from the list of rules. This method allows for dynamic
        adjustments to the validation process, accommodating changes in validation requirements or contexts.

        :param rule: The validation strategy instance to remove.
        :type rule: TimeEntryStrategy
        """
        self.validationRules.remove(rule)

    def validate_entry(self, timeEntry: TimeEntry):
        """
        Validates a `TimeEntry` object against all active validation strategies. This method applies
        each rule to the `TimeEntry` object and collects the results.

        :param timeEntry: The `TimeEntry` object to validate, containing all necessary data for the validations.
        :type timeEntry: TimeEntry

        :return: A list of `ValidationResult` objects, each representing the outcome of a single validation strategy
        applied to the `TimeEntry` object. Each result includes information about whether the validation was
        successful, along with any relevant messages. :rtype: list[ValidationResult]
        """
        results = []
        for rule in self.validationRules:
            result = rule.validate(timeEntry)
            results.append(result)
        return results
