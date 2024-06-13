from numpy import uint32
import calendar
from model.time_entry_type import TimeEntryType
from model.user.contract_information import ContractInfo
from model.user.personal_information import PersonalInfo


class DocumentData:

    def __init__(self, month: int, year: int, signature: uint32,
                 personal_info: PersonalInfo, contract_info: ContractInfo,
                 overtime_from_previous_month: float,
                 time_entries=[]):
        self.overtime_from_previous_month = overtime_from_previous_month
        self.month = month
        self.year = year
        self.signature = signature
        self.personal_info = personal_info
        self.contract_info = contract_info
        self.time_entries = time_entries

    def get_monthly_working_hours(self):
        """
        Calculates the total number of working hours in a month.
        :return: The total number of working hours in a month.
        """
        working_hours = 0.0
        for time_entry in self.time_entries:
            working_hours += time_entry.get_duration()
        return working_hours

    def get_overtime(self):
        """
        Calculates the total number of overtime hours in a month.
        :return: The total number of overtime hours in a month.
        """
        working_hours = self.get_monthly_working_hours()
        weeks_in_month = len(calendar.monthcalendar(self.year, self.month))
        contract_hours_per_month = self.contract_info.working_hours * weeks_in_month
        overtime = working_hours - contract_hours_per_month + self.overtime_from_previous_month
        return overtime

    def get_formatted_time_string(self):
        """
        Returns a formatted string representing the time period of the document.
        :return: A formatted string representing the time period of the document.
        """
        month_name = calendar.month_name[self.month]
        return f"{month_name} / {self.year}"
