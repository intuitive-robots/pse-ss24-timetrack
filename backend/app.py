""" This is the main python module where we call the run method of the flask app."""

import secrets
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import init_auth_routes

from controller.document_controller import DocumentController, document_blueprint
from controller.notification_controller import NotificationController, notification_blueprint
from controller.time_entry_controller import TimeEntryController, time_entry_blueprint
from controller.timesheet_controller import TimesheetController, timesheet_blueprint
from controller.user_controller import UserController, user_blueprint
from db import initialize_db
from service.notification_service import NotificationService
from apscheduler.schedulers.background import BackgroundScheduler
from service.setup_service import SetupService

app = Flask(__name__)
CORS(app)  # enable CORS for all routes and origins
db = initialize_db()

setup_service = SetupService()
setup_service.run_setup()


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
user_blueprint.add_url_rule('/archiveUser', view_func=user_view, methods=['POST'], endpoint='archive_user')
user_blueprint.add_url_rule('/unarchiveUser', view_func=user_view, methods=['POST'], endpoint='unarchive_user')
user_blueprint.add_url_rule('/getProfile', view_func=user_view, methods=['GET'], endpoint='get_profile')
user_blueprint.add_url_rule('getContractInfo', view_func=user_view, methods=['GET'], endpoint='get_contract_info')
user_blueprint.add_url_rule('/deleteUser', view_func=user_view, methods=['DELETE'], endpoint='delete_user')
user_blueprint.add_url_rule('/getUsers', view_func=user_view, methods=['GET'], endpoint='get_users')
user_blueprint.add_url_rule('/getArchivedUsers', view_func=user_view, methods=['GET'], endpoint='get_archived_users')
user_blueprint.add_url_rule('/getUsersByRole', view_func=user_view, methods=['GET'], endpoint='get_users_by_role')
user_blueprint.add_url_rule('/uploadFile', view_func=user_view, methods=['POST'], endpoint='upload_user_file')
user_blueprint.add_url_rule('/getFile', view_func=user_view, methods=['GET'], endpoint='get_user_file')
user_blueprint.add_url_rule('/deleteFile', view_func=user_view, methods=['DELETE'], endpoint='delete_user_file')
user_blueprint.add_url_rule('/getHiwis', view_func=user_view, methods=['GET'], endpoint='get_hiwis')
user_blueprint.add_url_rule('/getSupervisor', view_func=user_view, methods=['GET'], endpoint='get_supervisor')
user_blueprint.add_url_rule('/getSupervisors', view_func=user_view, methods=['GET'], endpoint='get_supervisors')
app.register_blueprint(user_blueprint, url_prefix='/user')

notification_view = NotificationController.as_view('notification')
notification_blueprint.add_url_rule('/delete', view_func=notification_view, methods=['DELETE'],
                                    endpoint='delete_notification')
notification_blueprint.add_url_rule('/readAll', view_func=notification_view, methods=['GET'],
                                    endpoint='read_all_notifications')
notification_blueprint.add_url_rule('/doesUnreadMessageExist', view_func=notification_view, methods=['GET'],
                                    endpoint='does_unread_messages_exist')
app.register_blueprint(notification_blueprint, url_prefix='/notification')

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

timesheet_blueprint.add_url_rule('/ensureExists', view_func=timesheet_view, methods=['POST'],
                                 endpoint='ensure_timesheet_exists')

timesheet_blueprint.add_url_rule('/getCurrentTimesheet', view_func=timesheet_view, methods=['GET'],
                                 endpoint='get_current_timesheet')

timesheet_blueprint.add_url_rule('getHighestPriorityTimesheet', view_func=timesheet_view, methods=['GET'],
                                 endpoint='get_highest_priority_timesheet')
timesheet_blueprint.add_url_rule('/getByMonthYear', view_func=timesheet_view, methods=['GET'],
                                 endpoint='get_timesheets_by_month_year')

app.register_blueprint(timesheet_blueprint, url_prefix='/timesheet')

document_view = DocumentController.as_view('document')
document_blueprint.add_url_rule('/generateDocument', view_func=document_view, methods=['GET'])
document_blueprint.add_url_rule('/generateMultipleDocuments', view_func=document_view, methods=['GET'])
app.register_blueprint(document_blueprint, url_prefix='/document')

scheduler = BackgroundScheduler()
notification_service = NotificationService()
scheduler.add_job(func=notification_service.send_scheduled_reminders, trigger="interval", days=1)
scheduler.start()

@app.route('/')
def home():
    return "Clockwise 1.0, Developed by Dominik, Phil, Johann, Alina and José"


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
