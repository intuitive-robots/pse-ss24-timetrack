from model.contract_information import ContractInfo
from model.personal_information import PersonalInfo
from model.role import UserRole
from model.user import User


class Hiwi(User):
    def __init__(self, username: str, password_hash: str, personal_info: PersonalInfo,
                 supervisor: str, contract_info: ContractInfo):
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
        self.timesheets = []
        self.contract_info = contract_info
        self.signature_image = None

    def add_timesheet(self, timesheet):
        """
        Adds a timesheet entry to the list of timesheets.

        :param timesheet: The timesheet to be added.
        """
        self.timesheets.append(timesheet)

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
            "timesheets": [ts.to_dict() for ts in self.timesheets],
            "contract_info": self.contract_info.to_dict(),
        })
        return user_dict
