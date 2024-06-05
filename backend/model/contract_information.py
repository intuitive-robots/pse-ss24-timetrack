class ContractInfo:
    def __init__(self, hourly_wage: float, working_hours: int, vacation_hours: int):
        """
        Initializes a new instance of ContractInfo.

        :param hourly_wage: The hourly wage of the employee.
        :param working_hours: Total number of working hours per week.
        :param vacation_hours: Remaining vacation hours.
        """
        self.hourly_wage = hourly_wage
        self.working_hours = working_hours
        self.vacation_hours = vacation_hours

    def update_hourly_wage(self, new_wage: float):
        """
        Updates the hourly wage.

        :param new_wage: The new hourly wage to be set.
        """
        self.hourly_wage = new_wage

    def update_working_hours(self, new_hours: int):
        """
        Updates the working hours.

        :param new_hours: The new number of working hours per week to be set.
        """
        self.working_hours = new_hours

    def update_vacation_hours(self, new_vacation_hours: int):
        """
        Updates the remaining vacation hours.

        :param new_vacation_hours: The new number of remaining vacation hours.
        """
        self.vacation_hours = new_vacation_hours

    def to_dict(self):
        """
        Converts the ContractInfo object to a dictionary.

        :return: A dictionary representing the contract information.
        """
        return {
            "hourlyWage": self.hourly_wage,
            "workingHours": self.working_hours,
            "vacationHours": self.vacation_hours
        }

    def __str__(self):
        """
        Provides a string representation of the contract information.

        :return: A string representation of the contract details.
        """
        return f"Hourly Wage: {self.hourly_wage}, Working Hours: {self.working_hours}, Vacation Hours: {self.vacation_hours}"
