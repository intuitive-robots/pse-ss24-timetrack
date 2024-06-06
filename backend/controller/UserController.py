from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from service.UserService import UserService

user_blueprint = Blueprint('user', __name__)


class UserController(MethodView):
    def __init__(self):
        self.user_service = UserService()
        self.auth_service = None

    def post(self):
        endpoint_mapping = {
            '/createUser': self.create_user,
            '/login': self.login,
            '/logout': self.logout,
            '/resetPassword': self.reset_password,
            '/deleteUser': self.delete_user
        }
        return self._dispatch_request(endpoint_mapping)

    def put(self):
        endpoint_mapping = {
            '/updateUser': self.update_user,
        }
        return self._dispatch_request(endpoint_mapping)

    def get(self):
        endpoint_mapping = {
            '/getProfile': self.get_profile,
            '/getUsers': self.get_users,
            '/getUsersByRole': self.get_users_by_role,
        }
        return self._dispatch_request(endpoint_mapping)

    def _dispatch_request(self, endpoint_mapping):
        request_path = request.path.replace('/user', '', 1)
        for path, func in endpoint_mapping.items():
            if request_path.endswith(path):
                return func()
        return jsonify({'error': 'Endpoint not found'}), 404

    @jwt_required()
    def create_user(self):
        user_data = request.get_json()
        return jsonify(self.user_service.create_user(user_data)), 201

    def login(self):
        credentials = request.get_json()
        user = self.user_service.find_user(credentials['username'])
        if user and self.auth_service.verify_password(user['password'], credentials['password']):
            access_token = create_access_token(identity=user['username'])
            return jsonify({"access_token": access_token}), 200
        return jsonify({"error": "Invalid credentials"}), 401

    @jwt_required()
    def logout(self):
        return jsonify({"message": "Logged out successfully"}), 200

    @jwt_required()
    def verify_token(self):
        result = self.auth_service.verify_token()
        return result.message, 200

    @jwt_required()
    def reset_password(self):
        data = request.get_json()
        result = self.auth_service.reset_password(data['username'], data['new_password'])
        return jsonify({"result": "Password reset successful"}), 200

    @jwt_required()
    def update_user(self):
        credentials = request.get_json()
        result = self.auth_service.login(credentials['username'], credentials['password'])
        return jsonify({"result": "User updated successfully"}), 200

    @jwt_required()
    def delete_user(self):
        result = self.user_service.delete_user(get_jwt_identity())
        return jsonify({"result": "User deleted successfully"}), 200

    @jwt_required()
    def get_profile(self):
        user_profile = self.user_service.get_profile(get_jwt_identity())
        return jsonify(user_profile), 200

    @jwt_required()
    def get_users(self):
        users = self.user_service.get_all_users()
        return jsonify(users), 200

    @jwt_required()
    def get_users_by_role(self):
        role = request.args.get('role')
        users = self.user_service.get_users_by_role(role)
        return jsonify(users), 200