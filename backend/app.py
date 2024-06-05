from flask import Flask, jsonify, request
from model.personal_information import PersonalInfo
from model.repository.user_repository import UserRepository
from model.role import UserRole
from model.user import User
from db import initialize_db, check_db_connection
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta, time
from auth import init_auth_routes, check_access
import secrets
from flask_cors import CORS
from auth import hash_password
from model.work_entry import WorkEntry

app = Flask(__name__)
CORS(app)  # enable CORS for all routes and origins
db = initialize_db()

app.config["JWT_SECRET_KEY"] = secrets.token_bytes(32)  # Generates a random secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
jwt = JWTManager(app)

init_auth_routes(app)


@app.route('/')
def home():
    return "Flask Backend"

def user_to_dict(user):
    user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return user

@app.route('/deleteUser', methods=['DELETE'])
@jwt_required()
@check_access(roles=[UserRole.ADMIN])
def delete_user():
    username = request.json.get('username', None)
    if username is None:
        return {"msg": "Username is required"}, 400
    user_repo = UserRepository.get_instance()
    user = user_repo.find_by_username(username)
    if user is None:
        return {"msg": "User not found"}, 404
    result = user_repo.delete_user(username)
    if result["result"] == "User deleted successfully":
        return {"msg": "User deleted successfully"}, 200
    return {"msg": "User deletion failed"}, 500

@app.route('/createTestUser')
@jwt_required()
def create_user():
    """
    Creates a test user in the database
    TODO: This is a hardcoded user, replace this with a React form
    :return: A string indicating that the user was created
    """
    password = "test_password"
    hashed_password = hash_password(password)

    user = User(
        username="test123",
        password_hash=hashed_password,
        personal_info=PersonalInfo(
            first_name="John",
            last_name="Doe",
            email="test@gmail.com",
            personal_number="123456",
            institute_name="Test Institute"),
        role=UserRole.ADMIN
    )
    user_repo = UserRepository.get_instance()
    result = user_repo.create_user(user)

    return result.to_dict(), result.status_code

@app.route('/readUsers')
@jwt_required()
@check_access(roles=[UserRole.ADMIN])
def read_users():
    """
    Reads all users from the database
    Is only accessible to users with the role ADMIN
    :return: A JSON string containing all users
    """
    user_repo = UserRepository.get_instance()
    users = user_repo.get_users()
    return jsonify([user_to_dict(user) for user in users])


#TODO: This is a hardcoded time entry!
@app.route('/createTestTimeEntry')
@jwt_required()
def create_time_entry():
    """
    Creates a test time entry in the database
    """
    work_entry = WorkEntry(
        time_entry_id="test123",
        timesheet_id="timesheet123",
        date="2022-01-01",
        start_time=time(hour=9, minute=0),
        end_time=time(hour=17, minute=0),
        break_time=1.0,
        activity="Test Activity",
        project_name="Test Project"
    )
    db.timeentries.insert_one(work_entry.to_dict())
    return "Time entry created"

@app.route('/checkMongoDBConnection')
def check_mongodb_connection():
    """
    Check the connection to the MongoDB database
    :return: A string indicating the connection status
    """
    return check_db_connection()


if __name__ == '__main__':
    app.run(debug=True)
