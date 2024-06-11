from datetime import time, datetime

from model.time_entry import TimeEntry


class VacationEntry(TimeEntry):
    """
    Represents a vacation entry in the timesheet.
    """
    def __init__(self, timesheet_id: str,
                 start_time: datetime, end_time: datetime):
        """
        Initializes a new VacationEntry object with the given parameters.
        :param timesheet_id: Id of the timesheet.
        :param start_time: Start time of the vacation entry.
        :param end_time: End time of the vacation entry.
        """
        super().__init__(timesheet_id, start_time, end_time)

    def get_duration(self):
        """
        Calculates the duration of the vacation entry.
        :return: The duration of the vacation entry.
        """
        # Calculate the duration
        duration = self.end_time - self.start_time
        # Return the duration in hours
        return duration.total_seconds() / 3600
