import gridfs
from numpy import uint32
import calendar
from model.time_entry_type import TimeEntryType
from model.user.contract_information import ContractInfo
from model.user.personal_information import PersonalInfo


class DocumentData:
    """
    Represents the data required for generating a document.
    """

    def __init__(self, month: int, year: int,
                 personal_info: PersonalInfo, contract_info: ContractInfo,
                 overtime_from_previous_month: float, signature, supervisor_signature,
                 time_entries=[], urlaub_anteilig="00:00"):
        """
        Initializes a new DocumentData object with the given parameters.
        """
        self.overtime_from_previous_month = overtime_from_previous_month
        self.month = month
        self.year = year
        self.personal_info = personal_info
        self.contract_info = contract_info
        self.time_entries = time_entries
        self.signature = signature
        self.supervisor_signature = supervisor_signature
        self.urlaub_anteilig = urlaub_anteilig


    def get_monthly_working_hours(self):
        """
        Calculates the total number of working hours in a month.
        :return: The total number of working hours in a month.
        """
        duration_minutes = round(sum(entry.get_duration() for entry in self.time_entries), 2)
        hours, minutes = divmod(duration_minutes, 60)
        duration_str = f"{int(hours):02d}:{int(minutes):02d}"
        return duration_str

    def get_overtime(self):
        """
        Calculates the total number of overtime hours in a month.
        :return: The total number of overtime hours in a month.
        """
        """actual_working_hours = self.get_monthly_working_hours()
        weeks_in_month = len(calendar.monthcalendar(self.year, self.month))
        contract_hours_per_month = self.contract_info.working_hours * weeks_in_month
        overtime = actual_working_hours - contract_hours_per_month + self.overtime_from_previous_month
        return overtime
        """
        return ""

    def get_contract_hours_per_month(self):
        """
        Returns the total number of working hours in a month.
        :return: The total number of working hours in a month.
        """
        return self.contract_info.working_hours

    #TODO: Useless because month and year are seperated in the timesheet pdf
    def get_formatted_time_string(self):
        """
        Returns a formatted string representing the time period of the document.
        :return: A formatted string representing the time period of the document.
        """
        month_name = calendar.month_name[self.month]
        return f"{month_name} / {self.year}"
