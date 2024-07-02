from db import db, initialize_db
from model.personal_information import PersonalInfo
from model.role import UserRole

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
