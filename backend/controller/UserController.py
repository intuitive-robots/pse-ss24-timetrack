from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from model.user.role import UserRole
from service.AuthService import AuthenticationService
from service.UserService import UserService

user_blueprint = Blueprint('user', __name__)


class UserController(MethodView):
    def __init__(self):
        """
        Initialize the UserController with instances of UserService and AuthService.
        """
        self.user_service = UserService()
        self.auth_service = AuthenticationService()

    def post(self):
        """
        Handles POST requests to manage user-related actions such as create, login, logout,
        reset password, and delete user based on the specific endpoint.
        """
        endpoint_mapping = {
            '/createUser': self.create_user,
            '/login': self.login,
            '/logout': self.logout,
            '/resetPassword': self.reset_password,
            '/deleteUser': self.delete_user
        }
        return self._dispatch_request(endpoint_mapping)

    def put(self):
        """
        Handles PUT requests for updating user information.
        """
        endpoint_mapping = {
            '/updateUser': self.update_user,
        }
        return self._dispatch_request(endpoint_mapping)

    def get(self):
        """
        Handles GET requests for retrieving user profiles, user lists, or users by specific roles.
        """
        endpoint_mapping = {
            '/getProfile': self.get_profile,
            '/getUsers': self.get_users,
            '/getUsersByRole': self.get_users_by_role,
        }
        return self._dispatch_request(endpoint_mapping)

    def _dispatch_request(self, endpoint_mapping):
        """
        Dispatches the request to the appropriate handler based on the request path.

        :param endpoint_mapping: Dictionary mapping endpoints to function handlers.
        :return: The response from the handler or an error message if endpoint not found.
        """
        request_path = request.path.replace('/user', '', 1)
        for path, func in endpoint_mapping.items():
            if request_path.endswith(path):
                return func()
        return jsonify({'error': 'Endpoint not found'}), 404

    @jwt_required()
    def create_user(self):
        """
        Creates a new user with the provided JSON data.
        """
        user_data = request.get_json()
        result = self.user_service.create_user(user_data)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def update_user(self):
        """
        Updates an existing user's data with the provided JSON data.
        """
        user_data = request.get_json()
        result = self.user_service.update_user(user_data)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def delete_user(self):
        """
        Deletes a user identified by their username provided in JSON data.
        """
        username = request.get_json()
        result = self.user_service.delete_user(username)
        return jsonify(result.message), result.status_code

    def login(self):
        """
        Authenticates a user and returns a JWT token if successful.
        """
        credentials = request.get_json()
        result = self.auth_service.login(credentials['username'], credentials['password'])
        if result:
            return jsonify({"access_token": result}), 200
        return jsonify({"error": "Invalid credentials"}), 401

    @jwt_required()
    def logout(self):
        """
        Logs out a user by terminating their session or token.
        """
        result = self.auth_service.logout()
        return jsonify(result.message), result.status_code

    @jwt_required()
    def verify_token(self):
        """
        Verifies the current user's token and returns the status.
        """
        result = self.auth_service.verify_token()
        return jsonify(result.message), result.status_code

    @jwt_required()
    def reset_password(self):
        """
        Resets the password for a user based on the provided JSON data.
        """
        data = request.get_json()
        result = self.auth_service.reset_password(data)
        return jsonify(result), 200

    @jwt_required()
    def get_profile(self):
        """
        Retrieves the profile information for the currently authenticated user.
        """
        user_profile = self.user_service.get_profile(get_jwt_identity())
        return jsonify(user_profile), 200

    @jwt_required()
    def get_users(self):
        """
        Retrieves a list of all users in the system.
        """
        users = self.user_service.get_users()
        user_dict_list = [user.to_dict() for user in users]
        return jsonify(user_dict_list), 200

    @jwt_required()
    def get_users_by_role(self):
        """
        Retrieves a list of users filtered by a specific role provided via query parameters.
        """
        role = UserRole.get_role_by_value(request.args.get('role'))
