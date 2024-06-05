from db import initialize_db
from model.personal_information import PersonalInfo
from model.user import User


class UserRepository:
    """
    Repository class for managing user data in the database.
    """
    _instance = None  # Singleton instance of the UserRepository class.

    @staticmethod
    def get_instance():
        """
        Singleton instance of the UserRepository class.
        :return:
        """
        if UserRepository._instance is None:
            UserRepository._instance = UserRepository()
        return UserRepository._instance

    def __init__(self):
        self.db = initialize_db()

    def create_user(self, user: User):
        """
        Creates a new user in the database.

        :param user: The user object to be created.
        :return: The ID of the newly created user.
        """
        user_data = {
            "username": user.username,
            "passwordHash": user.password_hash,
            "personalInfo": user.personal_info.to_dict(),
            "employmentDetails": {
                "role": str(user.role),
            },
            "accountCreation": user.account_creation,
            "lastLogin": user.last_login
        }
        result = self.db.users.insert_one(user_data)
        if result.acknowledged:
            return {"result": "User created successfully", "id": str(result.inserted_id)}
        return {"result": "User creation failed"}

    def find_by_username(self, username):
        """
        Finds a user in the database by their username.

        :param username: The username of the user to find.
        :return: The user object if found, otherwise None.
        """
        user = self.db.users.find_one({"username": username})

        if user:
            return User(
                username=user['username'],
                password_hash=user['passwordHash'],
                personal_info=PersonalInfo(user['personalInfo']['firstName'], user['personalInfo']['lastName'],
                                           user['personalInfo']['email'], user['personalInfo']['personalNumber'],
                                           user['personalInfo']['instituteName']),
                role=user['employmentDetails']['role'],
            )
        return None

    def update_user(self, user: User):
        """
        Updates a user in the database.

        :param user: The user object to be updated.
        :return: The ID of the updated user.
        """
        user_data = {
            "username": user.username,
            "passwordHash": user.password_hash,
            "personalInfo": user.personal_info.to_dict(),
            "employmentDetails": {
                "role": str(user.role),
            },
            "accountCreation": user.account_creation,
            "lastLogin": user.last_login
        }

        result = self.db.users.update_one({"username": user.username}, {"$set": user_data})
        if result.acknowledged:
            return {"result": "User updated successfully"}
        return {"result": "User update failed"}

    def delete_user(self, username):
        """
        Deletes a user from the database.

        :param username: The username of the user to be deleted.
        :return: The ID of the deleted user.
        """
        result = self.db.users.delete_one({"username": username})
        if result.acknowledged:
            return {"result": "User deleted successfully"}
        return {"result": "User deletion failed"}

    def get_users(self):
        """
        Gets all users from the database.

        :return: A list of all users in the database.
        """
        users = self.db.users.find()
        return [user for user in users]

    def get_users_by_role(self, role):
        """
        Gets all users from the database with a specific role.

        :param role: The role of the users to retrieve.
        :return: A list of users with the specified role.
        """
        users = self.db.users.find({"employmentDetails.role": role})
        return [user for user in users]
