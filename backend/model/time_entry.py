from abc import ABC, abstractmethod
from datetime import time


class TimeEntry(ABC):
    def __init__(self, timesheet_id: str, date: str,
                 start_time: time, end_time: time):
        """
        Initializes a new TimeEntry object with the given parameters.
        :param timesheet_id: The unique identifier for the timesheet.
        :param date: The date of the time entry.
        :param start_time: The start time of the time entry.
        :param end_time: The end time of the time entry.
        """
        self.time_entry_id = None
        self.timesheet_id = timesheet_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

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
            'date': self.date,
            'startTime': str(self.start_time),
            'endTime': str(self.end_time)
        }

    @abstractmethod
    def get_duration(self):
        """
        Calculates the duration of the time entry.
        :return: The duration of the time entry.
        """
        pass