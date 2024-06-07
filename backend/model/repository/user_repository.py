from db import initialize_db
from model.personal_information import PersonalInfo
from model.request_result import RequestResult
from model.role import UserRole
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
        if user is None:
            return RequestResult(False, "User object is None", 400)
        if self.find_by_username(user.username):
            return RequestResult(False, "User already exists", 409)
        result = self.db.users.insert_one(user.to_dict())
        if result.acknowledged:
            return RequestResult(True, f'User created successfully with ID: {str(result.inserted_id)}', 201)
        return RequestResult(False, "User creation failed", 500)

    def find_by_username(self, username):
        """
        Finds a user in the database by their username.

        :param username: The username of the user to find.
        :return: The user object if found, otherwise None.
        """
        if username is None:
            return None
        user_data = self.db.users.find_one({"username": username})

        if user_data:
            return User(
                username=user_data['username'],
                password_hash=user_data['passwordHash'],
                personal_info=PersonalInfo(user_data['personalInfo']['firstName'], user_data['personalInfo']['lastName'],
                                           user_data['personalInfo']['email'], user_data['personalInfo']['personalNumber'],
                                           user_data['personalInfo']['instituteName']),
                role=UserRole.get_role_by_value(user_data['role']),
            )
        return None

    def update_user(self, user: User):
        """
        Updates a user in the database.

        :param user: The user object to be updated.
        :return: The ID of the updated user.
        """

        result = self.db.users.update_one({"username": user.username}, {"$set": user.to_dict()})
        if result.matched_count == 0:
            return RequestResult(False, "User not found", 404)
        if result.modified_count == 0:
            return RequestResult(False, "User update failed", 500)
        if result.acknowledged:
            return RequestResult(True, "User updated successfully", 200)
        return RequestResult(False, "User update failed", 500)

    def delete_user(self, username):
        """
        Deletes a user from the database.

        :param username: The username of the user to be deleted.
        :return: The ID of the deleted user.
        """
        if username is None:
            return RequestResult(False, "Please provide a username to delete the user.", 400)
        if self.find_by_username(username) is None:
            return RequestResult(False, "User not found", 404)
        result = self.db.users.delete_one({"username": username})
        if result.deleted_count == 0:
            return RequestResult(False, "User deletion failed", 500)
        if result.acknowledged:
            return RequestResult(True, "User deleted successfully", 200)
        return RequestResult(False, "User deletion failed", 500)

    def get_users(self):
        """
        Gets all users from the database.

        :return: A list of all users in the database.
        """
        users = self.db.users.find()
        return list(users)

    def get_users_by_role(self, role):
        """
        Gets all users from the database with a specific role.

        :param role: The role of the users to retrieve.
        :return: A list of users with the specified role.
        """
        users = self.db.users.find({"employmentDetails.role": role})
        return list(users)
