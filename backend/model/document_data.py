from datetime import datetime

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
                 overtime_from_previous_month, signature, supervisor_signature, overtime,
                 time_entries=[], urlaub_anteilig="00:00", last_signature_changed=datetime.now()):
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
        self.overtime = overtime
        self.last_signature_changed = last_signature_changed



    def get_monthly_working_hours(self):
        """
        Calculates the total number of working hours in a month.
        :return: The total number of working hours in a month.
        """
        if not self.time_entries:
            return f"{0:02d}:{0:02d}"
        duration_minutes = round(sum(entry.get_duration() for entry in self.time_entries), 2) or 0
        hours, minutes = divmod(duration_minutes, 60)
        duration_str = f"{int(hours):02d}:{int(minutes):02d}"
        return duration_str


    def get_contract_hours_per_month(self):
        """
        Returns the total number of working hours in a month.
        :return: The total number of working hours in a month.
        """
        contracted_hours = self.contract_info.working_hours
        return f"{contracted_hours}:00"

    #TODO: Useless because month and year are seperated in the timesheet pdf
    def get_formatted_time_string(self):
        """
        Returns a formatted string representing the time period of the document.
        :return: A formatted string representing the time period of the document.
        """
        month_name = calendar.month_name[self.month]
        return f"{month_name} / {self.year}"
