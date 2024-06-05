from datetime import time, datetime

from model.time_entry import TimeEntry


class VacationEntry(TimeEntry):
    def __init__(self, time_entry_id: str, timesheet_id: str, date: str,
                 start_time: time, end_time: time):
        super().__init__(time_entry_id, timesheet_id, date, start_time, end_time)

    def to_dict(self):
        return {
            "timeEntryId": self.time_entry_id,
            "timesheetId": self.timesheet_id,
            "date": self.date,
            "startTime": self.start_time.strftime("%H:%M"),
            "endTime": self.end_time.strftime("%H:%M")
        }

    def get_duration(self):
        start_datetime = datetime.combine(datetime.min.date(), self.start_time)
        end_datetime = datetime.combine(datetime.min.date(), self.end_time)
        # Calculate the duration
        duration = end_datetime - start_datetime
        # Return the duration in hours
        return duration.total_seconds() / 3600
