from datetime import time, datetime

from model.time_entry import TimeEntry


class VacationEntry(TimeEntry):
    """
    Represents a vacation entry in the timesheet.
    """
    def __init__(self, timesheet_id: str, date: str,
                 start_time: time, end_time: time):
        """
        Initializes a new VacationEntry object with the given parameters.
        :param timesheet_id: Id of the timesheet.
        :param date: Date of the vacation entry.
        :param start_time: Start time of the vacation entry.
        :param end_time: End time of the vacation entry.
        """
        super().__init__(timesheet_id, date, start_time, end_time)

    def get_duration(self):
        """
        Calculates the duration of the vacation entry.
        :return: The duration of the vacation entry.
        """
        start_datetime = datetime.combine(datetime.min.date(), self.start_time)
        end_datetime = datetime.combine(datetime.min.date(), self.end_time)
        # Calculate the duration
        duration = end_datetime - start_datetime
        # Return the duration in hours
        return duration.total_seconds() / 3600
