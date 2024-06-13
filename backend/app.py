import secrets
from datetime import timedelta, datetime

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required

from auth import init_auth_routes
from controller.time_entry_controller import TimeEntryController, time_entry_blueprint
from controller.timesheet_controller import TimesheetController, timesheet_blueprint
from controller.user_controller import UserController, user_blueprint
from db import initialize_db, check_db_connection
from model.repository.time_entry_repository import TimeEntryRepository
from model.repository.timesheet_repository import TimesheetRepository
from model.repository.user_repository import UserRepository
from model.timesheet import Timesheet
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User
from model.work_entry import WorkEntry
from utils.security_utils import SecurityUtils
from service.timesheet_service import TimesheetService

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
user_blueprint.add_url_rule('/updateUser', view_func=user_view, methods=['POST'], endpoint='update_user')
user_blueprint.add_url_rule('/getProfile', view_func=user_view, methods=['GET'], endpoint='get_profile')
user_blueprint.add_url_rule('/deleteUser', view_func=user_view, methods=['POST'], endpoint='delete_user')
user_blueprint.add_url_rule('/getUsers', view_func=user_view, methods=['GET'], endpoint='get_users')
user_blueprint.add_url_rule('/getUsersByRole', view_func=user_view, methods=['GET'], endpoint='get_users_by_role')
user_blueprint.add_url_rule('/uploadFile', view_func=user_view, methods=['POST'], endpoint='upload_user_file')
user_blueprint.add_url_rule('/getFile', view_func=user_view, methods=['GET'], endpoint='get_user_file')
user_blueprint.add_url_rule('/removeFile', view_func=user_view, methods=['POST'], endpoint='remove_user_file')

app.register_blueprint(user_blueprint, url_prefix='/user')

time_entry_view = TimeEntryController.as_view('time_entry')
time_entry_blueprint.add_url_rule('/createWorkEntry', view_func=time_entry_view, methods=['POST'])
time_entry_blueprint.add_url_rule('/createVacationEntry', view_func=time_entry_view, methods=['POST'])
time_entry_blueprint.add_url_rule('/updateTimeEntry', view_func=time_entry_view, methods=['POST'])
time_entry_blueprint.add_url_rule('/deleteTimeEntry', view_func=time_entry_view, methods=['POST'])
time_entry_blueprint.add_url_rule('/getEntriesByTimesheetId', view_func=time_entry_view, methods=['GET'])

app.register_blueprint(time_entry_blueprint, url_prefix='/timeEntry')


timesheet_view = TimesheetController.as_view('timesheet')
timesheet_blueprint.add_url_rule('/sign', view_func=timesheet_view, methods=['PATCH'], endpoint='sign_timesheet')
timesheet_blueprint.add_url_rule('/approve', view_func=timesheet_view, methods=['PATCH'], endpoint='approve_timesheet')
timesheet_blueprint.add_url_rule('/requestChange', view_func=timesheet_view, methods=['PATCH'],
                                 endpoint='request_change')
timesheet_blueprint.add_url_rule('/get', view_func=timesheet_view, methods=['GET'], endpoint='get_timesheets')
timesheet_blueprint.add_url_rule('/getByUsernameStatus', view_func=timesheet_view, methods=['GET'],
                                 endpoint='get_timesheets_by_username_status')
app.register_blueprint(timesheet_blueprint, url_prefix='/timesheet')

@app.route('/')
def home():
    return "Flask Backend"

def timesheet_to_dict(timesheet):
    timesheet['_id'] = str(timesheet['_id'])  # Convert ObjectId to string
    return timesheet
def work_entry_to_dict(work_entry):
    work_entry['_id'] = str(work_entry['_id'])  # Convert ObjectId to string
    return work_entry

@app.route('/createTestUser')
@jwt_required()
def create_user():
    """
    Creates a test user in the database
    TODO: This is a hardcoded user, replace this with a React form
    :return: A string indicating that the user was created
    """
    password = "test_password"
    hashed_password = SecurityUtils.hash_password(password)

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

@app.route('/test1')
def test1():
    time_entry_repository = TimeEntryRepository.get_instance()
    time_entry = time_entry_repository.get_time_entry_by_id("666611873270f3785020e764")
    return work_entry_to_dict(time_entry), 200

#TODO: This is a hardcoded time entry!
@app.route('/createTestTimeEntry')
@jwt_required()
def create_time_entry():
    """
    Creates a test time entry in the database
    """
    work_entry = WorkEntry(
        timesheet_id="6669af45e93d71a91f35c79b",
        start_time=datetime(year=2022, month=3, day=1, hour=8, minute=0),
        end_time=datetime(year=2022, month=3, day=1, hour=10, minute=0),
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
        username="test123",
        month=6,
        year=2022,
    )
    timesheet_repo = TimesheetRepository.get_instance()
    result = timesheet_repo.create_timesheet(timesheet)

    timesheet_service = TimesheetService()
    timesheet_id = timesheet_service.get_timesheet(timesheet.username, timesheet.month, timesheet.year).data.timesheet_id
    timesheet_service.add_time_entry(timesheet_id, "6668bdd0c1c2ec60ed516ceb")
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
