from model.role import UserRole
from model.user import User


class UserService:

    def __init__(self):
        """
        Initializes a new instance of the UserService class.

        This service is responsible for managing user data operations, interfacing
        with both the user repository for data storage and retrieval and possibly
        a user factory for creating user instances, as well as a validator for
        user data validation
        """
        self.user_repository = None
        self.user_factory = None
        self.user_validator = None

    def create_user(self, user_data: dict):
        """
        Creates a new user in the system based on the provided user data.

        :param dict user_data: A dictionary containing user attributes necessary for creating a new user.
        :return: An instance of the User model representing the newly created user.
        :rtype: RequestResult object containing the result of the create operation.
        """
        return self.user_repository.create_user(user_data)

    def update_user(self, user_data: dict):
        """
        Updates an existing user in the system with the provided user data.

        :param dict user_data: A dictionary with user attributes that should be updated.
        :return: RequestResult object containing the result of the update operation.
        """
        return self.user_repository.update_user(user_data)

    def get_users(self) -> list[User]:
        """
        Retrieves a list of all users in the system.

        :return: A list of User model instances representing all users in the system.
        :rtype: list[User]
        """
        return self.user_repository.get_users()

    def get_users_by_role(self, role: UserRole) -> list[User]:
        """
        Retrieves a list of users in the system filtered by a specific role.

        :param UserRole role: The role to filter users by.
        :return: A list of User model instances that match the specified role.
        :rtype: list[User]
        """
        return self.user_repository.get_users_by_role(role)

    def get_profile(self, username: str) -> User:
        """
        Retrieves the profile of a specific user identified by their username.

        :param str username: The username of the user whose profile is being requested.
        :return: A User model instance representing the user's profile.
        :rtype: User
        """
        return self.user_repository.get_profile(username)
