from functools import wraps

import bcrypt
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, unset_jwt_cookies, create_access_token
from flask_jwt_extended.exceptions import NoAuthorizationError

from model.repository.user_repository import UserRepository
from model.request_result import RequestResult
from model.user.role import UserRole


class AuthenticationService:
    def __init__(self):
        """
        Initializes the AuthenticationService with an instance of UserRepository.
        """
        self.user_repository = UserRepository.get_instance()

    def _hash_password(self, password: str) -> str:
        """
        This function hashes a password using bcrypt.
        :param password: The password to hash
        :return: The hashed password
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _check_password(self, password: str, hashed_password: str) -> bool:
        """
        This function checks if a password matches a hashed password.
        :param password: The password to check
        :param hashed_password: The hashed password to compare against
        :return: True if the password matches the hashed password, False otherwise
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def create_token(self, username, role):
        """
        Generates a JWT token for a given user with additional claims.
        :param username: Username of the user.
        :param role: The role of the user.
        :return: JWT access token.
        """
        additional_claims = {"role": str(role)}
        return create_access_token(identity=username, additional_claims=additional_claims)

    def get_user_from_token(self):
        """
        Retrieves a user based on the JWT identity from the current request context.
        :return: User object if the token is valid, otherwise None.
        """
        username = get_jwt_identity()
        if username:
            return self.user_repository.find_by_username(username)
        return None

    def logout(self):
        """
        Logs out the user by unsetting the JWT cookies.
        """
        response = {"msg": "logout successful"}
        unset_jwt_cookies(response)
        return response, 200

    def login(self, username, password):
        """
        Authenticates a user and returns a JWT token if the credentials are valid.
        :param username: The username of the user.
        :param password: The password of the user.
        :return: RequestResult including a token if authentication is successful, else error message.
        """
        user = self.user_repository.find_by_username(username)
        if user and self._check_password(password, user.password_hash):
            access_token = self.create_token(username, user.role)
            return RequestResult(True, "Authentication successful", data={'access_token': access_token}, status_code=200)
        return RequestResult(False, "Invalid username or password", status_code=401)

    def reset_password(self, username, new_password):
        """
        Resets the password for a given username.
        :param username: The username for which to reset the password.
        :param new_password: The new password.
        :return: RequestResult indicating the success or failure of the reset process.
        """
        # Hash the new password before updating
        hashed_new_password = self._hash_password(new_password)
        return self.user_repository.update_user(username, {'passwordHash': hashed_new_password})


def check_access(roles: [UserRole] = []):
    """
    This function checks if the user has the required role to access the endpoint.
    :param roles: The roles that are allowed to access the endpoint
    :return: The decorator function
    """

    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            # calling @jwt_required()
            verify_jwt_in_request()
            # fetching current user from db
            current_user = UserRepository.get_instance().find_by_username(get_jwt_identity())
            # checking user role
            if current_user is None:
                raise NoAuthorizationError("User not found.")
            current_user_role = UserRole.get_role_by_value(current_user.role)
            if current_user_role not in roles:
                raise NoAuthorizationError("Role is not allowed.")
            return f(*args, **kwargs)

        return decorator_function

    return decorator
