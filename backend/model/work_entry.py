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
    Represents a work entry in the timesheet.
    """

    def __init__(self, timesheet_id: str,
                 start_time: datetime, end_time: datetime, break_time: float,
                 activity: str, project_name: str, time_entry_id=None):
        """
        Initializes a new WorkEntry object with the given parameters.
        :param timesheet_id: Id of the timesheet.
        :param start_time: Start time of the work entry.
        :param end_time: End time of the work entry.
        :param break_time: Break time in minutes of the work entry.
        :param activity: Activity of the work entry.
        :param project_name: Project name of the work entry.
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
        Converts the WorkEntry object to a dictionary format.
        :return: A dictionary representing the work entry.
        """
        data = super().to_dict()
        data.update({
            "breakTime": self.break_time,
            "activity": self.activity,
            "projectName": self.project_name
        })
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a WorkEntry instance from a dictionary containing MongoDB data,
        utilizing the superclass method to handle common fields.
        """
        start_datetime = data['startTime']
        end_datetime = data['endTime']

        if isinstance(start_datetime, str):
            start_datetime = datetime.fromisoformat(data['startTime'])

        if isinstance(end_datetime, str):
            end_datetime = datetime.fromisoformat(data['endTime'])

        timesheet_id = data['timesheetId']
        break_time = data.get('breakTime', 0)
        activity = data.get('activity', '')
        project_name = data.get('projectName', '')

        return cls(
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
        Returns a list of keys used for the dictionary representation of a TimeEntry object by creating a dummy instance.

        :return: A list of keys representing the time entry data fields.
        """
        dummy_start_time = datetime.now()
        dummy_end_time = dummy_start_time + timedelta(hours=1)
        dummy_entry = cls("dummy_timesheet_id", dummy_start_time, dummy_end_time, 0, "", "")
        return list(dummy_entry.to_dict().keys())

    """
    def get_duration(self):
        
        Calculates the duration of the work entry.
        :return: The duration of the work entry.
       
        start_datetime = self.start_time
        end_datetime = self.end_time
        # Calculate the duration
        duration = end_datetime - start_datetime
        # Subtract the break time
        duration -= timedelta(minutes=self.break_time)
        # Return the duration in hours
        return duration.total_seconds() / 3600
    """

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
        test = float(f"{hours:.0f}.{minutes:.0f}")

        return test

