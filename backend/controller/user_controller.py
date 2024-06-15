from flask import Blueprint, request, jsonify, send_file
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.file.FileType import FileType
from model.user.role import UserRole
from service.auth_service import AuthenticationService, check_access
from service.file_service import FileService
from service.user_service import UserService

user_blueprint = Blueprint('user', __name__)


class UserController(MethodView):
    """
    Controller for managing user-related actions like creating, updating, and deleting users,
    managing login sessions, and handling user files.
    """

    def __init__(self):
        """
        Initializes UserController with UserService, AuthenticationService, and FileService instances.
        """
        self.user_service = UserService()
        self.auth_service = AuthenticationService()
        self.file_service = FileService()

    def post(self):
        """
        Handles POST requests to manage user-related actions based on the specific endpoint.

        :return: JSON response based on the action performed.
        """
        endpoint_mapping = {
            '/createUser': self.create_user,
            '/updateUser': self.update_user,
            '/login': self.login,
            '/logout': self.logout,
            '/resetPassword': self.reset_password,
            '/deleteUser': self.delete_user,
            '/uploadFile': self.upload_user_file,
        }
        return self._dispatch_request(endpoint_mapping)

    def get(self):
        """
        Handles GET requests for retrieving user profiles, user lists, or users by specific roles.

        :return: JSON response with user data or an error message.
        """
        endpoint_mapping = {
            '/getProfile': self.get_profile,
            '/getUsers': self.get_users,
            '/getUsersByRole': self.get_users_by_role,
            '/getFile': self.get_user_file,
        }
        return self._dispatch_request(endpoint_mapping)

    def delete(self):
        """
        Handles DELETE requests to delete user files.

        :return: JSON response indicating the outcome of the file deletion.
        """
        endpoint_mapping = {
            '/deleteFile': self.delete_user_file
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
    @check_access(roles=[UserRole.ADMIN])
    def create_user(self):
        """
        Creates a new user with the provided JSON data.

        :return: JSON response containing the status message and status code.
        """
        user_data = request.get_json()
        result = self.user_service.create_user(user_data)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.ADMIN])
    def update_user(self):
        """
        Updates an existing user's data with the provided JSON data.

        :return: JSON response containing the status message and status code.
        """
        user_data = request.get_json()
        result = self.user_service.update_user(user_data)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.ADMIN])
    def delete_user(self):
        """
        Deletes a user identified by their username provided in JSON data.

        :return: JSON response containing the status message and status code.
        """
        username_data = request.get_json()
        result = self.user_service.delete_user(username_data['username'])
        return jsonify(result.message), result.status_code

    def login(self):
        """
        Deletes a user identified by their username provided in JSON data.

        :return: JSON response containing the status message and status code.
        """
        credentials = request.get_json()
        result = self.auth_service.login(credentials['username'], credentials['password'])
        if not result.is_successful:
            return jsonify(result.message), result.status_code
        return jsonify(result.data), result.status_code

    @jwt_required()
    def logout(self):
        """
        Logs out a user by terminating their session or token.

        :return: JSON response with the logout confirmation message.
        """
        result = self.auth_service.logout()
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.ADMIN])
    def reset_password(self):
        """
        Resets the password for a user based on the provided JSON data.

        :return: JSON response with the result of the password reset attempt.
        """
        credentials = request.get_json()
        result = self.auth_service.reset_password(credentials['username'], credentials['password'])
        return jsonify(result), result.status_code

    @jwt_required()
    def get_profile(self):
        """
        Retrieves the profile information for the currently authenticated user.

        :return: JSON response containing the user's profile data.
        """
        user_profile = self.user_service.get_profile(get_jwt_identity())
        return jsonify(user_profile.to_dict()), 200

    @jwt_required()
    @check_access(roles=[UserRole.ADMIN])
    def get_users(self):
        """
        Retrieves a list of all users in the system.

        :return: JSON response containing a list of user profiles.
        """
        users = self.user_service.get_users()
        user_dict_list = [user.to_dict() for user in users]
        return jsonify(user_dict_list), 200

    @jwt_required()
    @check_access(roles=[UserRole.ADMIN])
    def get_users_by_role(self):
        """
        Retrieves a list of users filtered by a specific role provided via query parameters.

        :return: JSON response containing a list of user profiles filtered by role.
        """
        data = request.get_json()
        users_data = self.user_service.get_users_by_role(data['role'])
        result = [user.to_dict() for user in users_data]
        return jsonify(result), 200

    @jwt_required()
    def upload_user_file(self):
        """
        Handles the uploading of a file for the currently authenticated user. The file type is determined
        from form data or a query parameter, and the file is then processed and stored accordingly.

        :return: JSON response with the status message and HTTP status code.
        """
        username = get_jwt_identity()
        file = request.files.get('file')

        file_type_str = request.form.get('fileType') or request.args.get('fileType')

        if not file or not file_type_str:
            return jsonify("Missing file or file type"), 400

        file_type = FileType.get_type_by_value(file_type_str)
        if not file_type:
            return jsonify("Invalid file type"), 400

        result = self.file_service.upload_image(file, username, file_type)

        return jsonify(result.message), result.status_code

    @jwt_required()
    def get_user_file(self):
        """
        Retrieves a file for the specified username and file type

        :return: The file as a download if found, or a JSON response indicating an error with an appropriate HTTP status code if not found or if parameters are missing.
        """
        username = request.args.get('username')
        file_type = FileType.get_type_by_value(request.args.get('fileType'))

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        if not file_type:
            return jsonify({'error': 'Valid File type is required'}), 400

        file_stream = self.file_service.get_image(username, file_type)
        if not file_stream:
            return jsonify({'error': 'File not found'}), 404

        return send_file(
            file_stream,
            as_attachment=True,
            download_name=f"{username}_{file_type}.jpg"
        )


    @jwt_required()
    def delete_user_file(self):
        """
        Deletes a file associated with the given username and specified file type.

        :return: A JSON response with the result of the deletion attempt and an appropriate HTTP status code.
        """
        username = request.args.get('username')
        file_type = FileType.get_type_by_value(request.args.get('fileType'))
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        if not file_type:
            return jsonify({'error': 'Valid File type is required'}), 400

        result = self.file_service.delete_image(username, file_type)
        return jsonify(result.message), result.status_code
