from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from service.UserService import UserService

user_blueprint = Blueprint('user', __name__)


class UserController(MethodView):
    def __init__(self):
        # Initialize user service instance
        self.user_service = UserService()

    @jwt_required()
    def create_user(self):
        print("test")
        """Creates a new user based on provided JSON data.
        Checks if the username already exists before creating the user."""
        # user_data = request.get_json()
        # if self.user_service.find_user(user_data['username']):
        #     return jsonify({"error": "Username already exists"}), 409
        # user_id = self.user_service.create_user(user_data)
        # return jsonify({"user_id": str(user_id)}), 201
        return jsonify("Success"), 200

    def login(self):
        """Authenticates a user and returns a JWT on successful authentication."""
        credentials = request.get_json()
        user = self.user_service.find_user(credentials['username'])
        if user and AuthenticationService.verify_password(user['passwordHash'], credentials['password']):
            access_token = create_access_token(identity=credentials['username'])
            return jsonify(access_token=access_token), 200
        return jsonify({"error": "Invalid credentials"}), 401

    @jwt_required()
    def logout(self):
        """Logs out the current user."""
        return jsonify({"msg": "Logged out successfully"}), 200

    @jwt_required()
    def verify_token(self):
        """Verifies the JWT of the current user and returns the identity."""
        current_user = get_jwt_identity()
        return jsonify({"logged_in_as": current_user}), 200

    @jwt_required()
    def reset_password(self):
        """Resets the password for the specified user based on the provided data."""
        data = request.get_json()
        result = self.user_service.reset_password(data['username'], data['new_password'])
        return jsonify({"result": "Password reset successful"}), 200

    @jwt_required()
    def update_user(self):
        """Updates user data for the current user."""
        username = get_jwt_identity()
        update_data = request.get_json()
        result = self.user_service.update_user(username, update_data)
        return jsonify({"result": "User updated successfully"}), 200

    @jwt_required()
    def delete_user(self):
        """Deletes the specified user."""
        username = get_jwt_identity()
        result = self.user_service.delete_user(username)
        return jsonify({"result": "User deleted successfully"}), 200

    @jwt_required()
    def get_users(self):
        """Returns a list of all users."""
        users = self.user_service.get_all_users()
        return jsonify(users), 200

    @jwt_required()
    def get_users_by_role(self):
        """Returns a list of users associated with a specific role."""
        role = request.args.get('role')
        users = self.user_service.get_users_by_role(role)
        return jsonify(users), 200


# Registering the user routes
# user_view = UserController.as_view('user_api')
# user_blueprint.add_url_rule('/createUser', view_func=user_view, methods=['POST'])
# user_blueprint.add_url_rule('/login', view_func=user_view, methods=['POST'])
# user_blueprint.add_url_rule('/logout', view_func=user_view, methods=['POST'])
# user_blueprint.add_url_rule('/verifyToken', view_func=user_view, methods=['POST'])
# user_blueprint.add_url_rule('/resetPassword', view_func=user_view, methods=['POST'])
# user_blueprint.add_url_rule('/updateUser', view_func=user_view, methods=['PUT'])
# user_blueprint.add_url_rule('/deleteUser', view_func=user_view, methods=['DELETE'])
# user_blueprint.add_url_rule('/getUsers', view_func=user_view, methods=['GET'])
# user_blueprint.add_url_rule('/getUsersByRole', view_func=user_view, methods=['GET'])
