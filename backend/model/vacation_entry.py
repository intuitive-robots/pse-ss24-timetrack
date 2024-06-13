from datetime import datetime, timedelta

from model.time_entry import TimeEntry
from model.time_entry_type import TimeEntryType
from model.time_entry_validator.holiday_strategy import HolidayStrategy
from model.time_entry_validator.time_entry_validator import TimeEntryValidator
from model.time_entry_validator.working_time_strategy import WorkingTimeStrategy


class VacationEntry(TimeEntry):
    """
    Represents a vacation entry in the timesheet.
    """

    def __init__(self, timesheet_id: str,
                 start_time: datetime, end_time: datetime):
        """
        Initializes a new VacationEntry object with the given parameters.
        :param timesheet_id: Id of the timesheet.
        :param start_time: Start time of the vacation entry.
        :param end_time: End time of the vacation entry.
        """

        super().__init__(timesheet_id, start_time, end_time, TimeEntryType.VACATION_ENTRY)
        self.time_entry_validator = TimeEntryValidator()
        self.time_entry_validator.add_validation_rule(WorkingTimeStrategy())
        self.time_entry_validator.add_validation_rule(HolidayStrategy())

    def to_dict(self):
        return super().to_dict()

    @classmethod
    def dict_keys(cls):
        """
        Returns a list of keys used for the dictionary representation of a VacationEntry object by creating a dummy instance.

        :return: A list of keys representing the vacation time entry data fields.
        """
        dummy_start_time = datetime.now()
        dummy_end_time = dummy_start_time + timedelta(hours=1)
        dummy_entry = cls("dummy_timesheet_id", dummy_start_time, dummy_end_time)
        return list(dummy_entry.to_dict().keys())

    def get_duration(self):
        """
        Calculates the duration of the vacation entry.
        :return: The duration of the vacation entry.
        """
        # Calculate the duration
        duration = self.end_time - self.start_time
        # Return the duration in hours
        return duration.total_seconds() / 3600
