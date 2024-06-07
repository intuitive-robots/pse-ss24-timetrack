import bcrypt

from controller.factory.UserFactory import UserFactory
from controller.input_validator.UserDataValidator import UserDataValidator
from controller.input_validator.ValidationStatus import ValidationStatus
from model.repository.user_repository import UserRepository
from model.request_result import RequestResult
from model.user.role import UserRole
from model.user.user import User


class UserService:

    def __init__(self):
        """
        Initializes a new instance of the UserService class.

        This service is responsible for managing user data operations, interfacing
        with both the user repository for data storage and retrieval and possibly
        a user factory for creating user instances, as well as a validator for
        user data validation
        """
        self.user_repository = UserRepository.get_instance()
        self.user_validator = UserDataValidator()

    def _hash_password(self, password: str) -> str:
        """
        This function hashes a password using bcrypt.
        :param password: The password to hash
        :return: The hashed password
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def create_user(self, user_data):
        """
        Creates a new user in the system based on the provided user data.

        :param dict user_data: A dictionary containing user attributes necessary for creating a new user.
        :return: An instance of the User model representing the newly created user.
        :rtype: RequestResult object containing the result of the create operation.
        """
        if not user_data['password']:  # plain password is required on creation
            return RequestResult(False, "Password is required", status_code=400)

        user_data['passwordHash'] = self._hash_password(user_data['password'])
        del user_data['password']  # Remove the plain text password from the data

        for key in User.dict_keys():
            if key not in user_data.keys():
                return RequestResult(False, f"Missing required field: {key}", status_code=400)

        self.user_validator.is_valid(user_data)  # check if field format is valid

        user_factory = UserFactory.get_factory(user_data['role'])
        if not user_factory:
            return RequestResult(False, "Invalid user role specified", status_code=400)

        user = user_factory.create_user(user_data)
        if not user:
            return RequestResult(False, "User creation failed", status_code=500)

        return self.user_repository.create_user(user)

    def update_user(self, user_data: dict):
        """
        Updates an existing user in the system with the provided user data.

        :param dict user_data: A dictionary with user attributes that should be updated.
        :return: RequestResult object containing the result of the update operation.
        """
        if 'username' not in user_data:
            return RequestResult(False, "Username must be provided for user update", status_code=400)

        existing_user_data = self.user_repository.find_by_username(user_data['username']).to_dict()
        if not existing_user_data:
            return RequestResult(False, "User not found", status_code=404)

            # Update existing user data with provided updates
        for key, value in user_data.items():
            if key in existing_user_data and key != 'username':  # Skip updating username
                existing_user_data[key] = value

        # Validate the updated user data
        validation_result = self.user_validator.is_valid(existing_user_data)
        if validation_result.status == ValidationStatus.FAILURE:
            return RequestResult(False, validation_result.message, status_code=400)

        # Create a user object using the factory
        updated_user = UserFactory.get_factory(existing_user_data['role']).create_user(existing_user_data)
        if not updated_user:
            return RequestResult(False, "Failed to create user object with updated data", status_code=400)

        return self.user_repository.update_user(updated_user)

    def delete_user(self, username: str):
        """
        Deletes a user from the system identified by their username.

        :param str username: The username of the user to be deleted.
        :return: A RequestResult object containing the result of the delete operation.
        """
        return self.user_repository.delete_user(username)

    def get_users(self) -> list[User]:
        """
        Retrieves a list of all users in the system.

        :return: A list of User model instances representing all users in the system.
        :rtype: list[User]
        """
        users_data = self.user_repository.get_users()
        users = list(filter(None, map(UserFactory.create_user_if_factory_exists, users_data)))

        return users

    def get_users_by_role(self, role: UserRole) -> list[User]:
        """
        Retrieves a list of users in the system filtered by a specific role.

        :param UserRole role: The role to filter users by.
        :return: A list of User model instances that match the specified role.
        :rtype: list[User]
        """
        users_data = self.user_repository.get_users_by_role(role)
        users = list(filter(None, map(UserFactory.create_user_if_factory_exists, users_data)))

        return users

    def get_profile(self, username: str) -> User:
        """
        Retrieves the profile of a specific user identified by their username.

        :param str username: The username of the user whose profile is being requested.
        :return: A User model instance representing the user's profile.
        :rtype: User Profile
        """
        user_data = self.user_repository.find_by_username(username)

        return UserFactory.create_user_if_factory_exists(user_data)
