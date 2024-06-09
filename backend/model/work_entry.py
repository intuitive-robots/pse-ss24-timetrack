from datetime import time, datetime, timedelta

from model.time_entry import TimeEntry
from model.time_entry_validator.break_length_strategy import BreakLengthStrategy
from model.time_entry_validator.holiday_strategy import HolidayStrategy
from model.time_entry_validator.working_time_strategy import WorkingTimeStrategy


class WorkEntry(TimeEntry):
    """
    Represents a work entry in the timesheet.
    """
    def __init__(self, time_entry_id: str, timesheet_id: str, date: str,
                 start_time: time, end_time: time, break_time: float,
                 activity: str, project_name: str):
        """
        Initializes a new WorkEntry object with the given parameters.
        :param time_entry_id: Id of the work entry.
        :param timesheet_id: Id of the timesheet.
        :param date: Date of the work entry.
        :param start_time: Start time of the work entry.
        :param end_time: End time of the work entry.
        :param break_time: Break time in minutes of the work entry.
        :param activity: Activity of the work entry.
        :param project_name: Project name of the work entry.
        """
        super().__init__(time_entry_id, timesheet_id, date, start_time, end_time)

        self.break_time = break_time
        self.activity = activity
        self.project_name = project_name
        self.time_entry_validator.add_validation_rule(WorkingTimeStrategy())
        self.time_entry_validator.add_validation_rule(HolidayStrategy())
        self.time_entry_validator.add_validation_rule(BreakLengthStrategy())

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

    def get_duration(self):
        """
        Calculates the duration of the work entry.
        :return: The duration of the work entry.
        """
        start_datetime = datetime.combine(datetime.min.date(), self.start_time)
        end_datetime = datetime.combine(datetime.min.date(), self.end_time)
        # Calculate the duration
        duration = end_datetime - start_datetime
        # Subtract the break time
        duration -= timedelta(minutes=self.break_time)
        # Return the duration in hours
        return duration.total_seconds() / 3600
