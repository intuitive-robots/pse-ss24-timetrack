import json
from datetime import datetime, timezone, timedelta

import bcrypt
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity

from db import initialize_db
from model.repository.user_repository import UserRepository

db = initialize_db()
user_repo = UserRepository.get_instance()

def init_auth_routes(app):
    """
    This function initializes the authentication routes for the application.
    
    :param app: The flask application.
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
