from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User


class Secretary(User):
    def __init__(self, username: str, password_hash: str,
             personal_info: PersonalInfo, current_timesheet_ids=None):
        """
        Initializes a new instance of the Secretary class, which extends the User class.

        :param current_timesheet_ids:
        :param username: The username for the Secretary account.
        :param password_hash: The hash of the user's password.
        :param personal_info: An instance of PersonalInfo containing the Secretary's personal information.

        """
        super().__init__(username, password_hash, personal_info, UserRole.SECRETARY)
        self.currentTimesheetIds = current_timesheet_ids if current_timesheet_ids is not None else []

    def to_dict(self):
        """
        Converts the Secretary object to a dictionary.

        :return: A dictionary containing all the current attributes of the Secreatry object.
        """
        user_dict = super().to_dict()
        user_dict.update({
            user_dict.update({"timesheets": self.currentTimesheetIds})
        })
        return user_dict
