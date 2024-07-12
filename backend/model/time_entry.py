from abc import ABC, abstractmethod
from datetime import datetime

from bson import ObjectId

from model.time_entry_type import TimeEntryType


class TimeEntry(ABC):
    """
    An abstract base class for time entries that defines common attributes and requires implementation
    of specific methods that depend on the type of time entry.

    This class serves as a template for defining different types of time entries, such as work entries or vacation entries,
    providing common implementation details and requiring subclasses to implement specific behaviors.

    Attributes:
        time_entry_id (str): The unique identifier for the time entry, which may be None if not set.
        timesheet_id (str): The unique identifier of the timesheet this entry belongs to.
        start_time (datetime): The start time of the time entry.
        end_time (datetime): The end time of the time entry.
        entry_type (TimeEntryType): The type of time entry, which dictates additional behaviors.
    """

    def __init__(self, timesheet_id: str, start_time: datetime, end_time: datetime, entry_type: TimeEntryType,
                 time_entry_id=None):
        """
        Initializes a new instance of the TimeEntry class with specified values.

        :param timesheet_id: The unique identifier for the timesheet to which this time entry belongs.
        :type timesheet_id: str
        :param start_time: The starting datetime of the time entry.
        :type start_time: datetime
        :param end_time: The ending datetime of the time entry.
        :type end_time: datetime
        :param entry_type: The specific type of the time entry, influencing validation and processing.
        :type entry_type: TimeEntryType
        :param time_entry_id: Optional unique identifier for the time entry itself.
        :type time_entry_id: str, optional
        """
        self.time_entry_id = time_entry_id
        self.timesheet_id = timesheet_id
        self.start_time = start_time
        self.end_time = end_time
        self.entry_type = entry_type

    def set_id(self, time_entry_id: ObjectId):
        """
        Sets or updates the identifier for this time entry.

        :param time_entry_id: A new identifier to assign to this time entry.
        :type time_entry_id: str
        """
        self.time_entry_id = time_entry_id

    @abstractmethod
    def to_dict(self):
        """
        Abstract method that must be overridden in subclasses to convert the specific TimeEntry object
        to a dictionary format, suitable for serialization or storage.

        :return: A dictionary representation of the time entry including keys for timesheet ID, start and end times, and entry type.
        :rtype: dict
        """
        return {
            '_id': self.time_entry_id,
            'timesheetId': str(self.timesheet_id),
            'startTime': self.start_time,
            'endTime': self.end_time,
            'entryType': self.entry_type.value
        }

    @abstractmethod
    def to_str_dict(self):
        """
        Abstract method that must be overridden in subclasses to convert the specific TimeEntry object
        to a dictionary format with string values, suitable for serialization or storage.
        """
        return {
            '_id': str(self.time_entry_id),
            'timesheetId': str(self.timesheet_id),
            'startTime': self.start_time,
            'endTime': self.end_time,
            'entryType': self.entry_type.value
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Factory method that creates an instance of a TimeEntry subclass from a dictionary.

        This method dynamically determines the subclass of TimeEntry to instantiate based on the `entryType` key
        in the input dictionary.

        :param data: A dictionary containing all necessary data to instantiate a specific TimeEntry.
        :type data: dict

        :return: An instance of a subclass of TimeEntry based on the type provided.
        :rtype: TimeEntry

        :raises ValueError: If the entry type is unsupported or missing.
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
        Abstract method that calculates the duration of the time entry, which must be implemented by subclasses.

        :return: The duration of the time entry, typically in hours or minutes.
        :rtype: int
        """
        pass
