from db import db, initializeDb
from model.personalInformation import PersonalInfo
from model.role import UserRole

db = initializeDb()


class User:

    def __init__(self, username: str, passwordHash: str, personalInfo: PersonalInfo, role: UserRole):
        """
        Initializes a new User object with basic details.

        :param username: Unique identifier for the user.
        :param passwordHash: Hashed password for secure authentication.
        :param personalInfo: An instance of PersonalInfo containing the user's personal details.
        :param role: UserRole enum indicating the user's role within the system.
        """
        self.username = username
        self.passwordHash = passwordHash
        self.personalInfo = personalInfo
        self.role = role
        self.accountCreation = None
        self.lastLogin = None

    def save(self):
        """
        Saves the user object to the database.

        :return: Result of the database insertion operation.
        """
        userData = {
            "username": self.username,
            "passwordHash": self.passwordHash,
            "personalInfo": self.personalInfo.toDict(),
            "employmentDetails": {
                "role": str(self.role),
            },
            "accountCreation": self.accountCreation,
            "lastLogin": self.lastLogin
        }
        return db.users.insert_one(userData)

    @classmethod
    def findByUsername(cls, username):
        """
        Class method to find a user by their username.

        :param username: The username of the user to find.
        :return: A User object if found, otherwise None.
        """
        user = db.users.find_one({"username": username})

        if user:
            return cls(
                username=user['username'],
                passwordHash=user['passwordHash'],
                personalInfo=PersonalInfo(user['personalInfo']['firstName'], user['personalInfo']['lastName'],
                                          user['personalInfo']['email'], user['personalInfo']['personalNumber'],
                                          user['personalInfo']['instituteName']),
                role=user['employmentDetails']['role'],
            )
        return None

    def isAdmin(self):
        """
        Checks if the user's role is 'ADMIN'.

        :return: True if the user is an admin, False otherwise.
        """
        return self.role == UserRole.ADMIN

    def toDict(self):
        """
        Converts the user object to a dictionary format.

        :return: A dictionary representing the user's data.
        """
        return {
            "username": self.username,
            "passwordHash": self.passwordHash,
            "personalInfo": self.personalInfo.toDict(),
            "role": str(self.role),
            "accountCreation": self.accountCreation,
            "lastLogin": self.lastLogin
        }
