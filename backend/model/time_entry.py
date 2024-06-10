from abc import ABC, abstractmethod
from datetime import time, datetime
from model.time_entry_type import TimeEntryType
from model.time_entry_validator.time_entry_validator import TimeEntryValidator


class TimeEntry(ABC):
    def __init__(self, timesheet_id: str, start_time: datetime, end_time: datetime, entry_type: TimeEntryType):
        """
        Initializes a new TimeEntry object with the given parameters.
        :param timesheet_id: The unique identifier for the timesheet.
        :param start_time: The start time of the time entry.
        :param end_time: The end time of the time entry.
        :param entry_type: The type of the time entry (WorkEntry or VacationEntry).
        """
        self.time_entry_id = None
        self.timesheet_id = timesheet_id
        self.start_time = start_time
        self.end_time = end_time
        self.entry_type = entry_type

    def set_id(self, time_entry_id):
        """
        Sets the ID of the time entry.
        :param time_entry_id: The ID of the time entry.
        """
        self.time_entry_id = time_entry_id

    @abstractmethod
    def to_dict(self):
        """
        Converts the TimeEntry object to a dictionary format.
        :return: A dictionary representing the time entry.
        """
        return {
            'timeEntryId': self.time_entry_id,
            'timesheetId': self.timesheet_id,
            'startTime': self.start_time,
            'endTime': self.end_time,
            'entryType': self.entry_type.value
        }

    @abstractmethod
    def get_duration(self):
        """
        Calculates the duration of the time entry.
        :return: The duration of the time entry.
        """
        pass
