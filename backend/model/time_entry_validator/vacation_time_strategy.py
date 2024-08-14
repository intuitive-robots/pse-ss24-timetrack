from flask_jwt_extended import get_jwt_identity, jwt_required

from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus
from model.time_entry import TimeEntry
from model.time_entry_validator.time_entry_strategy import TimeEntryStrategy
import service.user_service


class VacationTimeStrategy(TimeEntryStrategy):
    """
    Strategy for validating TimeEntry objects to ensure the Hiwi does not take more vacation time than they are entitled
    to according to their contract.
    """

    @jwt_required()
    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Validates a single TimeEntry against allowed vacation time.

        :param entry: The TimeEntry object to validate.
        :type entry: TimeEntry

        :return: A ValidationResult indicating whether the vacation entry does not exceed the allowed vacation time.
        :rtype: ValidationResult
        """

        user = get_jwt_identity()
        user_service = service.user_service.UserService()
        contract_info = user_service.get_contract_info(user).data
        if contract_info.vacation_minutes - entry.get_duration() < 0:
            return ValidationResult(ValidationStatus.FAILURE, "Vacation time exceeds the remaining vacation time.")
        return ValidationResult(ValidationStatus.SUCCESS, "Vacation time is valid.")


