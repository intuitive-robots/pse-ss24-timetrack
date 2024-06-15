import holidays
from model.time_entry import TimeEntry
from model.time_entry_validator.time_entry_strategy import TimeEntryStrategy
from controller.input_validator.validation_result import ValidationResult
from controller.input_validator.validation_status import ValidationStatus


class HolidayStrategy(TimeEntryStrategy):
    """
    Strategy for validating TimeEntry objects to ensure they do not coincide with public holidays
    in Baden-Württemberg, Germany. This strategy utilizes the `holidays` package to check for
    state-specific public holidays and assesses whether time entries fall on these dates.
    """

    def __init__(self):
        """
        Initializes the HolidayStrategy with a holiday calendar specific to Baden-Württemberg,
        Germany, enabling it to check for public holidays in this region.
        """
        self.holiday_calendar = holidays.DE(prov='BW')  # BW stands for Baden-Württemberg

    def validate(self, entry: TimeEntry) -> ValidationResult:
        """
        Validates a given TimeEntry against public holidays in Baden-Württemberg. If the date
        of the time entry is a public holiday, the validation will fail.

        :param entry: The TimeEntry object whose date needs to be validated against the public
                      holiday calendar.
        :type entry: TimeEntry

        :return: A ValidationResult object that indicates whether the entry date is a public
                 holiday. It returns failure if the date is a public holiday, along with a message
                 stating the name of the holiday. Otherwise, it returns success, indicating that
                 the date is not a public holiday.
        :rtype: ValidationResult

        Example:
            - If a time entry is made on 01.01.2022 and it's New Year's Day (a public holiday),
              the validation will return:
              ValidationResult(ValidationStatus.FAILURE, "Entry date is a public holiday: New Year's Day.")
            - If a time entry is made on 01.02.2022, which is not a public holiday,
              the validation will return:
              ValidationResult(ValidationStatus.SUCCESS, "Entry date is not a public holiday.")
        """
        if entry.date in self.holiday_calendar:
            holiday_name = self.holiday_calendar.get(entry.date)
            return ValidationResult(ValidationStatus.FAILURE, f"Entry date is a public holiday: {holiday_name}.")

        return ValidationResult(ValidationStatus.SUCCESS, "Entry date is not a public holiday.")
