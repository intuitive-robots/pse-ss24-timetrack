from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User


class Admin(User):
    def __init__(self, username: str, password_hash: str, personal_info: PersonalInfo, role: UserRole, slack_id: str = None):
        """
        Initializes a new instance of the Admin class, which extends the User class.

        :param username: The username for the Admin account.
        :param password_hash: The hash of the user's password.
        :param personal_info: An instance of PersonalInfo containing the Admin's personal information.

        """
        super().__init__(username, password_hash, personal_info, UserRole.ADMIN, slack_id)


    def to_dict(self):
        """
        Converts the Admin object to a dictionary.

        :return: A dictionary containing all the current attributes of the Admin object.
        """
        return super().to_dict()
