from bson import ObjectId

from model.timesheet import Timesheet
from model.user.contract_information import ContractInfo
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User


class Hiwi(User):
    def __init__(self, username: str, password_hash: str, personal_info: PersonalInfo,
                 supervisor: str, contract_info: ContractInfo, timesheets=[]):
        """
        Initializes a new instance of the Hiwi class, which extends the User class.

        :param username: The username for the Hiwi account.
        :param password_hash: The hash of the user's password.
        :param personal_info: An instance of PersonalInfo containing the Hiwi's personal information.
        :param supervisor: The username of the Hiwi's supervisor.
        :param contract_info: An instance of ContractInfo containing details about the Hiwi's contract.
        """

        super().__init__(username, password_hash, personal_info, UserRole.HIWI)
        self.supervisor = supervisor
        self.timesheets = timesheets
        self.contract_info = contract_info

    def add_timesheet(self, timesheet_id: ObjectId):
        """
        Adds a timesheet entry to the list of timesheets.

        :param timesheet: The timesheet to be added.
        """
        self.timesheets.append(timesheet_id)

    def remove_timesheet(self, timesheet_id: ObjectId):
        self.timesheets.remove(timesheet_id)

    def update_contract_info(self, hourly_wage, working_hours, vacation_hours):
        """
        Updates the contract information for the Hiwi.

        :param hourly_wage: The new hourly wage.
        :param working_hours: The new total number of working hours per week.
        :param vacation_hours: The new total number of vacation hours per year.
        """
        self.contract_info = ContractInfo(hourly_wage, working_hours, vacation_hours)

    def to_dict(self):
        """
        Converts the Hiwi object to a dictionary.

        :return: A dictionary containing all the current attributes of the Hiwi object.
        """
        user_dict = super().to_dict()
        user_dict.update({
            "supervisor": self.supervisor,
            "timesheets": [ts for ts in self.timesheets],
            "contractInfo": self.contract_info.to_dict() if self.contract_info is not None else {},
        })
        return user_dict

    @classmethod
    def from_dict(cls, data: dict):
        """
        Creates a Hiwi instance from a dictionary containing data typically retrieved from a database.

        :param data: A dictionary containing all necessary data keys to instantiate a Hiwi.
        :type data: dict

        :return: A fully instantiated Hiwi object.
        :rtype: Hiwi
        """
        user = super().from_dict(data)
        supervisor = data['supervisor']
        contract_info = ContractInfo.from_dict(data['contractInfo'])
        hiwi = cls(user.username, user.password_hash, user.personal_info, supervisor, contract_info)
        hiwi.timesheets = [Timesheet.from_dict(ts) for ts in data['timesheets']]
        return hiwi

