class ContractInfo:
    def __init__(self, hourly_wage: float, working_hours: int, vacation_minutes: int, overtime_minutes: int = 0):
        """
        Initializes a new instance of ContractInfo.

        :param hourly_wage: The hourly wage of the employee.
        :param working_hours: Total number of working hours per week.
        :param vacation_minutes: Remaining vacation hours.
        """
        self.hourly_wage = hourly_wage
        self.working_hours = working_hours
        self.vacation_minutes = vacation_minutes
        self.overtime_minutes = overtime_minutes

    @staticmethod
    def from_dict(data: dict):
        """
        Creates a ContractInfo instance from a dictionary.

        :param dict data: A dictionary containing the keys hourly_wage, working_hours, and vacation_minutes.
        :return: A new instance of ContractInfo.
        """
        hourly_wage = data.get('hourlyWage', 0)
        working_hours = data.get('workingHours', 0)
        vacation_minutes = data.get('vacationMinutes', 0)
        overtime_minutes = data.get('overtimeMinutes', 0)
        return ContractInfo(hourly_wage, working_hours, vacation_minutes, overtime_minutes)

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

    def update_vacation_minutes(self, new_vacation_minutes: int):
        """
        Updates the remaining vacation hours.

        :param new_vacation_minutes: The new number of remaining vacation hours.
        """
        self.vacation_minutes = new_vacation_minutes

    def to_dict(self):
        """
        Converts the ContractInfo object to a dictionary.

        :return: A dictionary representing the contract information.
        """
        return {
            "hourlyWage": self.hourly_wage,
            "workingHours": self.working_hours,
            "vacationMinutes": self.vacation_minutes,
            "overtimeMinutes": self.overtime_minutes
        }

    def __str__(self):
        """
        Provides a string representation of the contract information.

        :return: A string representation of the contract details.
        """
        return f"Hourly Wage: {self.hourly_wage}, Working Hours: {self.working_hours}, Vacation Minutes: {self.vacation_minutes}"
