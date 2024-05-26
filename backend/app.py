from flask import Flask, jsonify
from model.personal_information import PersonalInfo
from model.user import User
from db import initialize_db, check_db_connection
from flask_jwt_extended import JWTManager, jwt_required
from datetime import timedelta
from auth import init_auth_routes
import secrets

app = Flask(__name__)
db = initialize_db()

app.config["JWT_SECRET_KEY"] = secrets.token_bytes(32)  # Generates a random secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
jwt = JWTManager(app)

init_auth_routes(app, jwt)


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
        role="ADMIN"
    )
    user.save()
    return "User created"


@app.route('/find_user_by_username')
@jwt_required()
def find_user_by_username():
    """
    Finds a user by username
    TODO: This is a hardcoded username, replace this with React data
    :return: A JSON object containing the user
    """
    user = User.find_by_username("test_user")
    return jsonify(user.to_dict())


@app.route('/read_users')
@jwt_required()
def read_users():
    """
    Reads all users from the database
    TODO: This function should only be available to admins
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
