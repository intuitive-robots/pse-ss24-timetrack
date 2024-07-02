import math
from datetime import datetime, timedelta

from model.time_entry import TimeEntry
from model.time_entry_type import TimeEntryType
from model.time_entry_validator.break_length_strategy import BreakLengthStrategy
from model.time_entry_validator.holiday_strategy import HolidayStrategy
from model.time_entry_validator.time_entry_validator import TimeEntryValidator
from model.time_entry_validator.working_time_strategy import WorkingTimeStrategy


class WorkEntry(TimeEntry):
    """
    Represents a work entry in the timesheet, capturing detailed information about work periods,
    activities performed, and breaks taken during the work period.

    Attributes:
        break_time (float): The duration of the break time in minutes.
        activity (str): A description of the activity performed during the work entry.
        project_name (str): The name of the project associated with the work entry.
    """

    def __init__(self, timesheet_id: str,
                 start_time: datetime, end_time: datetime, break_time: float,
                 activity: str, project_name: str, time_entry_id=None):
        """
        Initializes a new WorkEntry object with specified timesheet ID, start and end times, break time, activity, and project name.

        :param timesheet_id: The unique identifier for the timesheet to which this work entry belongs.
        :type timesheet_id: str
        :param start_time: The start time of the work period.
        :type start_time: datetime
        :param end_time: The end time of the work period.
        :type end_time: datetime
        :param break_time: The duration of break time taken during the work period, in minutes.
        :type break_time: float
        :param activity: A description of the activity performed during the work entry.
        :type activity: str
        :param project_name: The name of the project associated with the work entry.
        :type project_name: str
        :param time_entry_id: Optional unique identifier for the time entry itself.
        :type time_entry_id: str, optional
        """
        super().__init__(timesheet_id, start_time, end_time, TimeEntryType.WORK_ENTRY, time_entry_id=time_entry_id)

        self.break_time = break_time
        self.activity = activity
        self.project_name = project_name
        time_entry_validator = TimeEntryValidator()
        time_entry_validator.add_validation_rule(WorkingTimeStrategy())
        time_entry_validator.add_validation_rule(HolidayStrategy())
        time_entry_validator.add_validation_rule(BreakLengthStrategy())

    def to_dict(self):
        """
        Converts the WorkEntry object to a dictionary format, including base class attributes and those specific to WorkEntry.

        :return: A dictionary representation of the WorkEntry, suitable for serialization.
        :rtype: dict
        """
        data = super().to_dict()
        data.update({
            "breakTime": self.break_time,
            "activity": self.activity,
            "projectName": self.project_name
        })
        return data

    def to_str_dict(self):
        """
        Converts the WorkEntry object to a dictionary format with string values, including base class attributes and those specific to WorkEntry.

        :return: A dictionary representation of the WorkEntry, suitable for serialization.
        :rtype: dict
        """
        data = super().to_str_dict()
        data.update({
            "breakTime": self.break_time,
            "activity": self.activity,
            "projectName": self.project_name
        })
        return data

    def get_activity_project_str(self):
        """
        Returns the activity and project name as a string.
        :return: The activity and project name as a string.
        """
        return f"{self.activity} - {self.project_name}"

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a WorkEntry instance from a dictionary containing data typically retrieved from a database.

        :param data: A dictionary containing all necessary data keys to instantiate a WorkEntry.
        :type data: dict

        :return: A fully instantiated WorkEntry object.
        :rtype: WorkEntry
        """
        start_datetime = data['startTime']
        end_datetime = data['endTime']

        if isinstance(start_datetime, str):
            start_datetime = datetime.fromisoformat(data['startTime'])

        if isinstance(end_datetime, str):
            end_datetime = datetime.fromisoformat(data['endTime'])
        time_entry_id = data.get('_id', None)
        timesheet_id = data['timesheetId']
        break_time = data.get('breakTime', 0)
        activity = data.get('activity', '')
        project_name = data.get('projectName', '')

        return cls(
            time_entry_id=time_entry_id,
            timesheet_id=timesheet_id,
            start_time=start_datetime,
            end_time=end_datetime,
            break_time=break_time,
            activity=activity,
            project_name=project_name
        )

    @classmethod
    def dict_keys(cls):
        """
        Provides a list of keys that are used in the dictionary representation of a WorkEntry object.

        :return: A list of string keys that represent the attributes of a WorkEntry object.
        :rtype: list[str]
        """
        dummy_start_time = datetime.now()
        dummy_end_time = dummy_start_time + timedelta(hours=1)
        dummy_entry = cls("dummy_timesheet_id", dummy_start_time, dummy_end_time, 0, "", "")
        return list(dummy_entry.to_dict().keys())


    def get_duration(self):

        """
        Calculates and returns the total duration of the work entry, minus break time, expressed in hours.

        :return: The total number of hours worked, excluding break time.
        :rtype: float

        Example:
            - If the start_time is at 9 AM, end_time at 5 PM, and break_time is 60 minutes,
              the duration would be 7.0 hours.
        """

        start_datetime = self.start_time
        end_datetime = self.end_time
        # Calculate the duration
        duration = end_datetime - start_datetime
        # Subtract the break time
        duration -= timedelta(minutes=self.break_time)
        # Return the duration in hours
        return duration.total_seconds() / 3600

    def get_duration(self):
        """
        Calculates the duration of the work entry.
        :return: The duration of the work entry in "hh:mm" format.
        """
        start_datetime = self.start_time
        end_datetime = self.end_time
        # Calculate the duration
        duration = end_datetime - start_datetime
        # Subtract the break time
        duration -= timedelta(minutes=self.break_time)
        # Get the duration in hours as a float
        duration_in_hours = duration.total_seconds() / 3600
        # Get the hours and remaining minutes
        hours, remainder = divmod(duration_in_hours, 1)

        # This fixes the floating point issue with the remainder
        if duration.total_seconds() % 60 >= 1:
            minutes = math.ceil(remainder * 60)
        else:
            minutes = math.floor(remainder * 60)
        # Format the hours and minutes into a string in "hh:mm" format
        duration = float(f"{hours:.0f}.{minutes:.0f}")

        return duration

