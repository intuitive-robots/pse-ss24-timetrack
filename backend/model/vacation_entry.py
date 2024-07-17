import math
from datetime import datetime, timedelta

import math
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
                 start_time: datetime, end_time: datetime, time_entry_id=None):
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

        super().__init__(timesheet_id, start_time, end_time, TimeEntryType.VACATION_ENTRY, time_entry_id)
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

    def to_str_dict(self):
        """
        Converts the VacationEntry object to a dictionary format, including all base class attributes
        and any that are specific to the VacationEntry class.

        :return: A dictionary representation of the VacationEntry, suitable for serialization.
        :rtype: dict
        """
        return super().to_str_dict()
    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a VacationEntry object from a dictionary.
        """
        start_datetime = data['startTime']
        end_datetime = data['endTime']

        if isinstance(start_datetime, str):
            start_datetime = datetime.fromisoformat(data['startTime'])

        if isinstance(end_datetime, str):
            end_datetime = datetime.fromisoformat(data['endTime'])
        time_entry_id = data.get('_id', None)
        timesheet_id = data['timesheetId']

        return cls(
            time_entry_id=time_entry_id,
            timesheet_id=timesheet_id,
            start_time=start_datetime,
            end_time=end_datetime
        )


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
        :rtype: int

        Example:
            - If the start_time is at 10 AM and the end_time is at 2 PM on the same day,
              the duration would be 4.0 hours.
        """
        # Calculate the duration
        duration = self.end_time - self.start_time
        # Return the duration in minutes
        return math.ceil(duration.total_seconds() / 60)
