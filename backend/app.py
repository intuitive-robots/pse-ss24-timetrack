from flask import Flask, jsonify, request
from model.user.personal_information import PersonalInfo
from model.personal_information import PersonalInfo
from model.repository.time_entry_repository import TimeEntryRepository
from model.repository.timesheet_repository import TimesheetRepository
from model.repository.user_repository import UserRepository
from model.user.role import UserRole
from model.role import UserRole
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus
from model.user import User
from db import initialize_db, check_db_connection
from flask_jwt_extended import JWTManager, jwt_required
from datetime import timedelta
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta, time, datetime
from auth import init_auth_routes, check_access
import secrets
from flask_cors import CORS
from auth import hash_password
from controller.UserController import UserController
from controller.UserController import user_blueprint
from model.work_entry import WorkEntry

app = Flask(__name__)
CORS(app)  # enable CORS for all routes and origins
db = initialize_db()

app.config["JWT_SECRET_KEY"] = secrets.token_bytes(32)  # Generates a random secret key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
jwt = JWTManager(app)

init_auth_routes(app)


# Registering the user routes
user_view = UserController.as_view('user')
user_blueprint.add_url_rule('/createUser', view_func=user_view, endpoint='create_user')
user_blueprint.add_url_rule('/login', view_func=user_view, methods=['POST'], endpoint='login')
user_blueprint.add_url_rule('/logout', view_func=user_view, methods=['POST'], endpoint='logout')
user_blueprint.add_url_rule('/verifyToken', view_func=user_view, methods=['POST'], endpoint='verify_token')
user_blueprint.add_url_rule('/resetPassword', view_func=user_view, methods=['POST'], endpoint='reset_password')
user_blueprint.add_url_rule('/updateUser', view_func=user_view, methods=['PUT'], endpoint='update_user')
user_blueprint.add_url_rule('/deleteUser', view_func=user_view, methods=['DELETE'], endpoint='delete_user')
user_blueprint.add_url_rule('/getUsers', view_func=user_view, methods=['GET'], endpoint='get_users')
user_blueprint.add_url_rule('/getUsersByRole', view_func=user_view, methods=['GET'], endpoint='get_users_by_role')

app.register_blueprint(user_blueprint, url_prefix='/user')



@app.route('/')
def home():
    return "Flask Backend"

def user_to_dict(user):
    user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return user

def timesheet_to_dict(timesheet):
    timesheet['_id'] = str(timesheet['_id'])  # Convert ObjectId to string
    return timesheet
def work_entry_to_dict(work_entry):
    work_entry['_id'] = str(work_entry['_id'])  # Convert ObjectId to string
    return work_entry
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
        time_entry_id="test1233",
        timesheet_id="timesheet123",
        date="2022-01-01",
        start_time=time(hour=9, minute=0),
        end_time=time(hour=17, minute=0),
        break_time=15.0,
        activity="Test Activity",
        project_name="Test Project"
    )
    entry_repo = TimeEntryRepository.get_instance()
    result = entry_repo.create_time_entry(work_entry)
    return result.to_dict(), result.status_code

#TODO: This works only for work entries, not vacation entries!
@app.route('/readTimeEntries')
@jwt_required()
def read_time_entries():
    """
    Reads all time entries from the database
    :return: A JSON string containing all time entries
    """
    entry_repo = TimeEntryRepository.get_instance()
    time_entries = entry_repo.get_time_entries()
    return jsonify([work_entry_to_dict(time_entry) for time_entry in time_entries])

@app.route('/readTimesheets')
@jwt_required()
def read_timesheets():
    """
    Reads all timesheets from the database
    :return: A JSON string containing all timesheets
    """
    timesheet_repo = TimesheetRepository.get_instance()
    timesheets = timesheet_repo.get_timesheets()
    return jsonify([timesheet_to_dict(timesheet) for timesheet in timesheets])

#TODO: This is a hardcoded timesheet!
@app.route('/createTimesheet')
@jwt_required()
def create_timesheet():
    """
    Creates a test timesheet in the database
    """
    timesheet = Timesheet(
        timesheet_id="timesheet123",
        username="test123",
        month=3,
        year=2022,
        status=TimesheetStatus.NOTSUBMITTED,
        total_time=40.0,
        overtime=5.0,
        last_signature_change=datetime.now()
    )
    timesheet_repo = TimesheetRepository.get_instance()
    result = timesheet_repo.create_timesheet(timesheet)
    return result.to_dict(), result.status_code
@app.route('/checkMongoDBConnection')
def check_mongodb_connection():
    """
    Check the connection to the MongoDB database
    :return: A string indicating the connection status
    """
    return check_db_connection()


if __name__ == '__main__':
    app.run(debug=True)
