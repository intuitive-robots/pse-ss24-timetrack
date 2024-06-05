from datetime import time, datetime, timedelta

from model.time_entry import TimeEntry


class WorkEntry(TimeEntry):
    def __init__(self, time_entry_id: str, timesheet_id: str, date: str,
                 start_time: time, end_time: time, break_time: float,
                 activity: str, project_name: str):
        super().__init__(time_entry_id, timesheet_id, date, start_time, end_time)

        self.break_time = break_time
        self.activity = activity
        self.project_name = project_name

    def to_dict(self):
        return {
            "timeEntryId": self.time_entry_id,
            "timesheetId": self.timesheet_id,
            "date": self.date,
            "startTime": self.start_time.strftime("%H:%M"),
            "endTime": self.end_time.strftime("%H:%M"),
            "breakTime": self.break_time,
            "activity": self.activity,
            "projectName": self.project_name
        }

    def get_duration(self):
        start_datetime = datetime.combine(datetime.min.date(), self.start_time)
        end_datetime = datetime.combine(datetime.min.date(), self.end_time)
        # Calculate the duration
        duration = end_datetime - start_datetime
        # Subtract the break time
        duration -= timedelta(minutes=self.break_time)
        # Return the duration in hours
        return duration.total_seconds() / 3600

# Path: model/work_entry.py
