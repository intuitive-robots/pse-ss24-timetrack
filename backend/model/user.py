from datetime import datetime
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

    def save(self):
        """
        Saves the user object to the database.

        :return: Result of the database insertion operation.
        """
        user_data = {
            "username": self.username,
            "password_hash": self.password_hash,
            "personal_info": self.personal_info.to_dict(),
            "employment_details": {
                "role": str(self.role),
            },
            "account_creation": self.account_creation,
            "last_login": self.last_login
        }
        return db.users.insert_one(user_data)

    @classmethod
    def find_by_username(cls, username):
        """
        Class method to find a user by their username.

        :param username: The username of the user to find.
        :return: A User object if found, otherwise None.
        """
        user = db.users.find_one({"username": username})

        if user:
            return cls(
                username=user['username'],
                password_hash=user['password_hash'],
                personal_info=PersonalInfo(user['personal_info']['first_name'], user['personal_info']['last_name'],
                                           user['personal_info']['email'], user['personal_info']['personal_number'],
                                           user['personal_info']['institute_name']),
                role=user['employment_details']['role'],
            )
        return None

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
            "password_hash": self.password_hash,
            "personal_info": self.personal_info.to_dict(),
            "role": str(self.role),
            "account_creation": self.account_creation,
            "last_login": self.last_login
        }
