class ContractInfo:
    def __init__(self, hourlyWage: float, workingHours: int, vacationHours: int):
        """
        Initializes a new instance of ContractInfo.

        :param hourlyWage: The hourly wage of the employee.
        :param workingHours: Total number of working hours per week.
        :param vacationHours: Remaining vacation hours.
        """
        self.hourlyWage = hourlyWage
        self.workingHours = workingHours
        self.vacationHours = vacationHours

    def updateHourlyWage(self, newWage: float):
        """
        Updates the hourly wage.

        :param newWage: The new hourly wage to be set.
        """
        self.hourlyWage = newWage

    def updateWorkingHours(self, newHours: int):
        """
        Updates the working hours.

        :param newHours: The new number of working hours per week to be set.
        """
        self.workingHours = newHours

    def updateVacationHours(self, newVacationHours: int):
        """
        Updates the remaining vacation hours.

        :param newVacationHours: The new number of remaining vacation hours.
        """
        self.vacationHours = newVacationHours

    def toDict(self):
        """
        Converts the ContractInfo object to a dictionary.

        :return: A dictionary representing the contract information.
        """
        return {
            "hourlyWage": self.hourlyWage,
            "workingHours": self.workingHours,
            "vacationHours": self.vacationHours
        }

    def __str__(self):
        """
        Provides a string representation of the contract information.

        :return: A string representation of the contract details.
        """
        return f"Hourly Wage: {self.hourlyWage}, Working Hours: {self.workingHours}, Vacation Hours: {self.vacationHours}"
