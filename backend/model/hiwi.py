from model.contractInformation import ContractInfo
from model.personalInformation import PersonalInfo
from model.role import UserRole
from model.user import User


class Hiwi(User):
    def __init__(self, username: str, passwordHash: str, personalInfo: PersonalInfo,
                 supervisor: str, contract_info: ContractInfo):
        """
        Initializes a new instance of the Hiwi class, which extends the User class.

        :param username: The username for the Hiwi account.
        :param passwordHash: The hash of the user's password.
        :param personalInfo: An instance of PersonalInfo containing the Hiwi's personal information.
        :param supervisor: The username of the Hiwi's supervisor.
        :param contract_info: An instance of ContractInfo containing details about the Hiwi's contract.
        """

        super().__init__(username, passwordHash, personalInfo, UserRole.HIWI)
        self.supervisor = supervisor
        self.timesheets = []
        self.contractInfo = contract_info
        self.signatureImage = None

    def addTimesheet(self, timesheet):
        """
        Adds a timesheet entry to the list of timesheets.

        :param timesheet: The timesheet to be added.
        """
        self.timesheets.append(timesheet)

    def updateContractInfo(self, hourlyWage, workingHours, vacationHours):
        """
        Updates the contract information for the Hiwi.

        :param hourlyWage: The new hourly wage.
        :param workingHours: The new total number of working hours per week.
        :param vacationHours: The new total number of vacation hours per year.
        """
        self.contractInfo = ContractInfo(hourlyWage, workingHours, vacationHours)

    def toDict(self):
        """
        Converts the Hiwi object to a dictionary.

        :return: A dictionary containing all the current attributes of the Hiwi object.
        """
        userDict = super().toDict()
        userDict.update({
            "supervisor": self.supervisor,
            "timesheets": [ts.toDict() for ts in self.timesheets],
            "contract_info": self.contractInfo.toDict(),
        })
        return userDict
