from abc import ABC, abstractmethod
from datetime import datetime
from model.time_entry_type import TimeEntryType


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
            'timesheetId': str(self.timesheet_id),
            'startTime': self.start_time,
            'endTime': self.end_time,
            'entryType': self.entry_type.value
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a WorkEntry instance from a dictionary containing MongoDB data,
        utilizing the superclass method to handle common fields.
        """
        entry_type = TimeEntryType.get_type_by_value(data['entryType'])

        from model.work_entry import WorkEntry
        from model.vacation_entry import VacationEntry
        type_class_map = {
            TimeEntryType.WORK_ENTRY: WorkEntry,
            TimeEntryType.VACATION_ENTRY: VacationEntry,
        }

        if entry_type in type_class_map:
            return type_class_map[entry_type].from_dict(data)
        else:
            raise ValueError(f"Unsupported entry type: {data['entryType']}")

    @abstractmethod
    def get_duration(self):
        """
        Calculates the duration of the time entry.
        :return: The duration of the time entry.
        """
        pass
