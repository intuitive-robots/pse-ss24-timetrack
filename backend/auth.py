from enum import Enum
from functools import wraps

from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    unset_jwt_cookies, jwt_required, verify_jwt_in_request
from flask import request, jsonify
from datetime import datetime, timezone, timedelta
import json

from flask_jwt_extended.exceptions import NoAuthorizationError

from db import initializeDb
from model.user import User
from model.role import UserRole

db = initializeDb()
def initAuthRoutes(app):
    """
    This function initializes the authentication routes for the application.
    :param app: The flask application
    """

    @app.after_request
    def refreshExpiringJWTs(response):
        """
        This function refreshes the JWT token if it is about to expire.
        For more information check out how the after_request decorator works in Flask.
        :param response: The response object of a request
        :return: The response object of the request
        """
        try:
            expTimestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            targetTimestamp = datetime.timestamp(now + timedelta(minutes=30))
            if targetTimestamp > expTimestamp:
                accessToken = create_access_token(identity=get_jwt_identity())
                data = response.get_json()
                if type(data) is dict:
                    data["access_token"] = accessToken
                    response.data = json.dumps(data)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    @app.route('/token', methods=["POST"])
    def createToken():
        """
        This function creates a JWT token for the user.
        :return: A JSON object containing the JWT token
        """
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        user = User.findByUsername(username)
        if user is None:
            return {"msg": "Invalid Username"}, 401
        if user.passwordHash != password:
            return {"msg": "Invalid Password"}, 401

        additional_claims = {"role": user.role}
        accessToken = create_access_token(identity=username, additional_claims=additional_claims)
        response = {"accessToken": accessToken}
        return response

    @app.route('/profile')
    @jwt_required()  # This API Endpoint requires authentication
    def myProfile():
        """
        This method should return the profile data of the user.
        :return: A JSON object containing the profile of the user
        """
        # Get MongoDB user and return it
        username = get_jwt_identity()
        user = User.findByUsername(username)
        return jsonify(user.toDict())

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
            current_user = User.findByUsername(get_jwt_identity())
            # checking user role
            if UserRole[current_user.role] not in roles:
                raise NoAuthorizationError("Role is not allowed.")
            return f(*args, **kwargs)
        return decorator_function
    return decorator
