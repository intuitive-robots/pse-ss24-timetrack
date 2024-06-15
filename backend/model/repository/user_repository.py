from db import initialize_db
from model.request_result import RequestResult
from model.user.role import UserRole
from model.user.user import User


class UserRepository:
    """
    Repository class for managing user data in the database. It provides functionalities
    for creating, retrieving, updating, and deleting users, as well as retrieving them by
    specific criteria such as username or role.
    """
    _instance = None  # Singleton instance of the UserRepository class.

    @staticmethod
    def get_instance():
        """
        Retrieves the singleton instance of the UserRepository class.

        :return: Singleton instance of UserRepository, ensuring that only one instance exists globally.
        """
        if UserRepository._instance is None:
            UserRepository._instance = UserRepository()
        return UserRepository._instance

    def __init__(self):
        """
        Initializes the UserRepository class by establishing a connection to the database.
        This connection is used for all data operations within this repository.
        """
        self.db = initialize_db()

    def create_user(self, user: User):
        """
        Creates a new user in the database. Checks if the user already exists to prevent duplicates.

        :param user: The User object to be created in the database.
        :return: RequestResult indicating the success or failure of the create operation,
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
        Retrieves a user's data from the database by their username.

        :param username: The username of the user to find.
        :return: A dictionary with the user's data if found, otherwise None.
        """
        if username is None:
            return None
        user_data = self.db.users.find_one({"username": username})

        return user_data

    def update_user(self, user: User) -> RequestResult:
        """
        Updates an existing user in the database based on the provided User object.

        :param user: The User object containing updated data for the user.
        :return: RequestResult indicating the success or failure of the update operation.
        """
        result = self.db.users.update_one({"username": user.username}, {"$set": user.to_dict()})
        if result.matched_count == 0:
            return RequestResult(False, "User not found", 404)
        if result.modified_count == 0:
            return RequestResult(False, "User update failed", 500)
        if result.acknowledged:
            return RequestResult(True, "User updated successfully", 200)
        return RequestResult(False, "User update failed", 500)

    def delete_user(self, username) -> RequestResult:
        """
        Deletes a user from the database by their username.

        :param username: The username of the user to delete.
        :return: RequestResult indicating the success or failure of the deletion process.
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

    def get_users(self) -> list[dict]:
        """
        Retrieves all users from the database.

        :return: A list of dictionaries, each containing the data of one user.
        """
        users_data = self.db.users.find()
        return list(users_data)

    def get_users_by_role(self, role: UserRole) -> list[dict]:
        """
        Retrieves all users from the database with a specified role.

        :param role: The UserRole to filter users by.
        :return: A list of dictionaries, each containing the data of one user with the specified role.
        """
        users_data = self.db.users.find({"role": role.value})
        return list(users_data)
