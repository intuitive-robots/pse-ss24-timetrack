from db import initialize_db
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole

db = initialize_db()


class User:

    def __init__(self, username: str, password_hash: str, personal_info: PersonalInfo, role: UserRole):
        """
        Initializes a new User object with basic details.

        :param username: Unique identifier for the user.
        :param password_hash: Hashed password for secure authentication.
        :param personal_info: An instance of PersonalInfo containing the user's personal details.
        :param role: UserRole enum indicating the user's role within the system.
        """
        self.username = username
        self.password_hash = password_hash
        self.personal_info = personal_info
        self.role = role
        self.account_creation = None
        self.last_login = None

    def is_admin(self):
        """
        Checks if the user's role is 'ADMIN'.

        :return: True if the user is an admin, False otherwise.
        """
        return self.role == UserRole.ADMIN

    @staticmethod
    def from_dict(user_data: dict):
        """
        Creates a User instance from a dictionary.

        :param dict user_data: Dictionary containing user details.
        :return: A new User instance.
        """
        username = user_data["username"]
        password_hash = user_data["passwordHash"]
        personal_info_data = user_data["personalInfo"]
        role = UserRole.get_role_by_value(user_data["role"])

        personal_info = PersonalInfo.from_dict(personal_info_data)

        return User(username, password_hash, personal_info, role)

    def to_dict(self):
        """
        Converts the user object to a dictionary format.

        :return: A dictionary representing the user's data.
        """
        return {
            "username": self.username,
            "passwordHash": self.password_hash,
            "personalInfo": self.personal_info.to_dict(),
            "role": str(self.role),
            "accountCreation": self.account_creation,
            "lastLogin": self.last_login
        }

    @classmethod
    def dict_keys(cls):
        """
        Returns a list of keys used for the dictionary representation of a User object.

        :return: A list of keys representing the user's data fields.
        """
        dummy_user = cls("username", "password_hash", PersonalInfo("", "", "", "", ""), UserRole.ADMIN)
        return list(dummy_user.to_dict().keys())
