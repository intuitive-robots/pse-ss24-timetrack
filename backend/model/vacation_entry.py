from datetime import datetime, timedelta

from model.time_entry import TimeEntry
from model.time_entry_type import TimeEntryType
from model.time_entry_validator.holiday_strategy import HolidayStrategy
from model.time_entry_validator.time_entry_validator import TimeEntryValidator
from model.time_entry_validator.working_time_strategy import WorkingTimeStrategy


class VacationEntry(TimeEntry):
    """
    Represents a vacation or leave entry in a timesheet, inheriting from TimeEntry. This class specifically handles
    entries that are marked as vacation, applying appropriate validation rules that may differ from those for other
    types of time entries.

    The class also integrates validation strategies specific to vacation entries, such as checks against working during
    holidays or exceeding allowable vacation time.
    """

    def __init__(self, timesheet_id: str,
                 start_time: datetime, end_time: datetime):
        """
        Initializes a new VacationEntry object with specified timesheet ID, start time, and end time,
        automatically setting the entry type to VACATION_ENTRY.

        :param timesheet_id: The unique identifier for the timesheet to which this vacation entry belongs.
        :type timesheet_id: str
        :param start_time: The start time of the vacation period.
        :type start_time: datetime
        :param end_time: The end time of the vacation period, which should be after the start time.
        :type end_time: datetime
        """

        super().__init__(timesheet_id, start_time, end_time, TimeEntryType.VACATION_ENTRY)
        self.time_entry_validator = TimeEntryValidator()
        self.time_entry_validator.add_validation_rule(WorkingTimeStrategy())
        self.time_entry_validator.add_validation_rule(HolidayStrategy())

    def to_dict(self):
        """
        Converts the VacationEntry object to a dictionary format, including all base class attributes
        and any that are specific to the VacationEntry class.

        :return: A dictionary representation of the VacationEntry, suitable for serialization.
        :rtype: dict
        """
        return super().to_dict()

    @classmethod
    def dict_keys(cls):
        """
        Provides a list of keys that are used in the dictionary representation of a VacationEntry object.
        This method can be used to understand what information is serialized for storage or transmission.

        :return: A list of string keys that represent the attributes of a VacationEntry object.
        :rtype: list[str]
        """
        dummy_start_time = datetime.now()
        dummy_end_time = dummy_start_time + timedelta(hours=1)
        dummy_entry = cls("dummy_timesheet_id", dummy_start_time, dummy_end_time)
        return list(dummy_entry.to_dict().keys())

    def get_duration(self):
        """
         Calculates and returns the total duration of the vacation entry, expressed in hours.

        :return: The total number of hours between the start and end times of the vacation entry.
        :rtype: float

        Example:
            - If the start_time is at 10 AM and the end_time is at 2 PM on the same day,
              the duration would be 4.0 hours.
        """
        # Calculate the duration
        duration = self.end_time - self.start_time
        # Return the duration in hours
        return duration.total_seconds() / 3600
