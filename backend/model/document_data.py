from numpy import uint32
import calendar
from model.time_entry_type import TimeEntryType
from model.user.contract_information import ContractInfo
from model.user.personal_information import PersonalInfo


class DocumentData:

    def __init__(self, month: int, year: int,
                 personal_info: PersonalInfo, contract_info: ContractInfo,
                 overtime_from_previous_month: float,
                 time_entries=[]):
        self.overtime_from_previous_month = overtime_from_previous_month
        self.month = month
        self.year = year
        self.personal_info = personal_info
        self.contract_info = contract_info
        self.time_entries = time_entries
        #TODO: Add signature field

    def get_monthly_working_hours(self):
        """
        Calculates the total number of working hours in a month.
        :return: The total number of working hours in a month.
        """
        working_hours = 0.0
        for time_entry in self.time_entries:
            working_hours += time_entry.get_duration()
        #Round up to the next minute
        working_hours = round(working_hours, 2)
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

    def get_contract_hours_per_month(self):
        """
        Calculates the total number of working hours in a month.
        :return: The total number of working hours in a month.
        """
        weeks_in_month = len(calendar.monthcalendar(self.year, self.month))
        return float(self.contract_info.working_hours * weeks_in_month)

    #TODO: Useless because month and year are seperated in the timesheet pdf
    def get_formatted_time_string(self):
        """
        Returns a formatted string representing the time period of the document.
        :return: A formatted string representing the time period of the document.
        """
        month_name = calendar.month_name[self.month]
        return f"{month_name} / {self.year}"
