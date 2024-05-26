from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    unset_jwt_cookies, jwt_required
from flask import request, jsonify
from datetime import datetime, timezone, timedelta
import json


def init_auth_routes(app, jwt):
    """
    This function initializes the authentication routes for the application.
    :param app: The flask application
    :param jwt: The JWTManager instance
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
            # Case where there is not a valid JWT. Just return the original respone
            return response

    @app.route('/token', methods=["POST"])
    def create_token():
        """
        This function creates a JWT token for the user.
        :return: A JSON object containing the JWT token
        """
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        # TODO: This is a hardcoded check, replace this with a database check
        if email != "test" or password != "test":
            return {"msg": "Wrong email or password"}, 401

        access_token = create_access_token(identity=email)
        response = {"access_token": access_token}
        return response

    @app.route('/profile')
    @jwt_required()  # This API Endpoint requires authentication
    def my_profile():
        """
        This method should return the profile of the user.
        TODO: Implement this method -> Right now it returns a hardcoded profile
        :return: A JSON object containing the profile of the user
        """
        response_body = {
            "name": "Nagato",
            "about": "Hello! I'm a full stack developer that loves python and javascript"
        }

        return response_body

    @app.route("/logout", methods=["POST"])
    def logout():
        """
        This method logs out the user by unsetting the JWT cookies.
        :return: A JSON object containing a message that the logout was successful
        """
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response
