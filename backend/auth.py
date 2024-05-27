from enum import Enum
from functools import wraps

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    unset_jwt_cookies, jwt_required, verify_jwt_in_request
from flask import request, jsonify
from datetime import datetime, timezone, timedelta
import json

from flask_jwt_extended.exceptions import NoAuthorizationError

from db import initialize_db
from model.user import User
from model.role import UserRole

db = initialize_db()
def init_auth_routes(app):
    """
    This function initializes the authentication routes for the application.
    :param app: The flask application
    """

    @app.after_request
    def refresh_expiring_jwts(response):
        """
        This function refreshes the JWT token if it is about to expire.
        For more information check out how the after_request decorator works in Flask.
        :param response: The response object of a request
        :return: The response object of the request
        """
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                data = response.get_json()
                if type(data) is dict:
                    data["access_token"] = access_token
                    response.data = json.dumps(data)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    @app.route('/token', methods=["POST"])
    def create_token():
        """
        This function creates a JWT token for the user.
        :return: A JSON object containing the JWT token
        """
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = User.find_by_username(username)
        if user is None:
            return {"msg": "Invalid Username"}, 401
        if user.password_hash != password:
            return {"msg": "Invalid Password"}, 401

        access_token = create_access_token(identity=username)
        response = {"access_token": access_token}
        return response

    @app.route('/profile')
    @jwt_required()  # This API Endpoint requires authentication
    def my_profile():
        """
        This method should return the profile data of the user.
        :return: A JSON object containing the profile of the user
        """
        # Get MongoDB user and return it
        username = get_jwt_identity()
        user = User.find_by_username(username)
        return jsonify(user.to_dict())

    @app.route("/logout", methods=["POST"])
    def logout():
        """
        This method logs out the user by unsetting the JWT cookies.
        :return: A JSON object containing a message that the logout was successful
        """
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response

# @check_access decorator function
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
            current_user = User.find_by_username(get_jwt_identity())
            # checking user role
            if current_user.role not in roles:
                raise NoAuthorizationError("Role is not allowed.")
            return f(*args, **kwargs)
        return decorator_function
    return decorator