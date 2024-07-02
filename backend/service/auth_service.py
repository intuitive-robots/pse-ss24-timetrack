from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, unset_jwt_cookies, create_access_token
from flask_jwt_extended.exceptions import NoAuthorizationError

from controller.factory.user_factory import UserFactory
from model.repository.user_repository import UserRepository
from model.request_result import RequestResult
from model.user.role import UserRole
from utils.security_utils import SecurityUtils


class AuthenticationService:
    """
    Provides authentication services including login, logout, token generation, and password reset.
    This service interfaces with the UserRepository to manage user data and security operations.
    """

    def __init__(self):
        """
        Initializes the AuthenticationService with an instance of UserRepository.
        """
        self.user_repository = UserRepository.get_instance()

    def create_token(self, username: str, role: UserRole) -> str:
        """
        Generates a JWT token for a given user with additional claims.

        :param username: The username of the user.
        :type username: str
        :param role: The role of the user.
        :type role: UserRole
        :return: A JWT access token as a string.
        :rtype: str
        """
        additional_claims = {"role": str(role)}
        return create_access_token(identity=username, additional_claims=additional_claims)

    def get_user_from_token(self):
        """
        Retrieves a user based on the JWT identity from the current request context.

        :return: A User object if the token is valid, otherwise None.
        :rtype: User or None
        """
        username = get_jwt_identity()
        if not username:
            return None

        user_data = self.user_repository.find_by_username(username)

        user = UserFactory.create_user_if_factory_exists(user_data)
        return user

    def logout(self):
        """
        Logs out the user by unsetting the JWT cookies.

        :return: A RequestResult indicating the success of the logout operation.
        :rtype: RequestResult
        """
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return RequestResult(True, "Logout successful", status_code=200)

    def login(self, username, password):
        """
        Authenticates a user and returns a JWT token if the credentials are valid.

        :param username: The username of the user.
        :type username: str
        :param password: The password of the user.
        :type password: str
        :return: A RequestResult including a token if authentication is successful, otherwise an error message.
        :rtype: RequestResult
        """
        user_data = self.user_repository.find_by_username(username)
        if not user_data:
            return RequestResult(False, "Invalid username", status_code=401)
        user = UserFactory.create_user_if_factory_exists(user_data)
        if user and SecurityUtils.check_password(password, user.password_hash):
            access_token = self.create_token(username, user.role)
            return RequestResult(True, "Authentication successful", data={'accessToken': access_token}, status_code=200)
        return RequestResult(False, "Invalid username or password", status_code=401)

    def reset_password(self, username, new_password):
        """
        Resets the password for a given username.

        :param username: The username for which to reset the password.
        :type username: str
        :param new_password: The new password.
        :type new_password: str
        :return: A RequestResult indicating the success or failure of the reset process.
        :rtype: RequestResult
        """
        if not username or not new_password:
            return RequestResult(False, "Username and new password must be provided", status_code=400)

        user_data = self.user_repository.find_by_username(username)
        if not user_data:
            return RequestResult(False, "User not found", status_code=404)

        user = UserFactory.create_user_if_factory_exists(user_data)
        if not user:
            return RequestResult(False, "Failed to create user object", status_code=500)

        user.password_hash = SecurityUtils.hash_password(new_password)

        result = self.user_repository.update_user(user)
        if result.is_successful:
            return RequestResult(True, "Password reset successful", status_code=200)

        return result


def check_access(roles: [UserRole] = []):
    """
    Decorator function to check if the user has the required role to access the endpoint.

    :param roles: A list of UserRole objects that are allowed to access the endpoint.
    :type roles: list[UserRole]
    :return: The decorator function.
    :rtype: function
    """

    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            """
            Decorated function to verify JWT and check user role.

            :param args: Positional arguments to pass to the original function.
            :param kwargs: Keyword arguments to pass to the original function.
            :return: The original function if access is granted, or raises NoAuthorizationError.
            :rtype: function
            """

            # calling @jwt_required()
            verify_jwt_in_request()
            # fetching current user from db
            current_user_data = UserRepository.get_instance().find_by_username(get_jwt_identity())
            # checking user role
            if current_user_data is None:
                raise NoAuthorizationError("User not found.")
            current_user_role = UserRole.get_role_by_value(current_user_data['role'])
            if current_user_role not in roles:
                raise NoAuthorizationError("Role is not allowed.")
            return f(*args, **kwargs)

        return decorator_function

    return decorator
