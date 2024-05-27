from flask import Flask, jsonify
from model.personal_information import PersonalInfo
from model.role import UserRole
from model.user import User
from db import initialize_db, check_db_connection
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from auth import init_auth_routes, check_access
import secrets

app = Flask(__name__)
db = initialize_db()

app.config["JWT_SECRET_KEY"] = secrets.token_bytes(32)  # Generates a random secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
jwt = JWTManager(app)

init_auth_routes(app)


@app.route('/')
def home():
    return "Flask Backend"


@app.route('/create_testUser')
@jwt_required()
def create_user():
    """
    Creates a test user in the database
    TODO: This is a hardcoded user, replace this with a React form
    :return: A string indicating that the user was created
    """
    user = User(
        username="test_user",
        password_hash="test_password",
        personal_info=PersonalInfo(
            first_name="John",
            last_name="Doe",
            email="test@gmail.com",
            personal_number="123456",
            instituteName="Test Institute"),
        role=UserRole.ADMIN
    )
    user.save()
    return "User created"

@app.route('/read_users')
@jwt_required()
@check_access(roles=[UserRole.ADMIN])
def read_users():
    """
    Reads all users from the database
    Is only accessible to users with the role ADMIN
    :return: A JSON string containing all users
    """
    all_users = list(db.users.find())
    return str(all_users)


@app.route('/check_mongoDB_connection')
def check_mongodb_connection():
    """
    Check the connection to the MongoDB database
    :return: A string indicating the connection status
    """
    return check_db_connection()


if __name__ == '__main__':
    app.run(debug=True)
