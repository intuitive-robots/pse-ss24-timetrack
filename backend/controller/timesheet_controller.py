from datetime import datetime

from flask import jsonify, request, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.user.role import UserRole
from service.auth_service import check_access
from service.timesheet_service import TimesheetService

timesheet_blueprint = Blueprint('timesheet', __name__)


class TimesheetController(MethodView):
    def __init__(self):
        self.timesheet_service = TimesheetService()

    def get(self):
        """
        Handles GET requests for retrieving timesheet data
        """
        endpoint_mapping = {
            '/get': self.get_timesheets,
            '/getByUsernameStatus': self.get_timesheets_by_username_status
        }
        return self._dispatch_request(endpoint_mapping)

    def patch(self):
        """
        Handles PATCH requests for updating timesheet data
        """
        endpoint_mapping = {
            '/sign': self.sign_timesheet,
            '/approve': self.approve_timesheet,
            '/requestChange': self.request_change
        }
        return self._dispatch_request(endpoint_mapping)

    @jwt_required()
    @check_access(roles=[UserRole.HIWI])
    def sign_timesheet(self):
        """
        HiWi signs his timesheet
        """
        request_data = request.get_json()
        timesheet_id = request_data['timesheet_id']
        check_existance = self.timesheet_service.ensure_timesheet_exists(get_jwt_identity(),
                                                                         datetime.now().month,
                                                                         datetime.now().year)
        if check_existance.status_code != 200 and check_existance.status_code != 201:
            return jsonify({'error': 'Failed to create timesheet'}), 500

        result = self.timesheet_service.sign_timesheet(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR])
    def approve_timesheet(self):
        """
        Supervisor approves a timesheet
        """
        request_data = request.get_json()
        timesheet_id = request_data['timesheet_id']
        result = self.timesheet_service.approve_timesheet(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR])
    def request_change(self):
        """
        Supervisor requests changes to a timesheet
        """
        request_data = request.get_json()
        timesheet_id = request_data['timesheet_id']
        result = self.timesheet_service.request_change(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def get_timesheets(self):
        """
        Retrieves timesheets for the current user
        """
        username = get_jwt_identity()
        result = self.timesheet_service.get_timesheets_by_username(username)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR, UserRole.SECRETARY])
    def get_timesheets_by_username_status(self):
        """
        Retrieves timesheets for a specific user and status
        """
        request_data = request.get_json()
        username = request_data['username']
        status = request_data['status']
        result = self.timesheet_service.get_timesheets_by_username_status(username, status)
        return jsonify(result.message), result.status_code

    def _dispatch_request(self, endpoint_mapping):
        """
        Dispatches the request to the appropriate handler based on the request path.

        :param endpoint_mapping: Dictionary mapping endpoints to function handlers.
        :return: The response from the handler or an error message if endpoint not found.
        """
        request_path = request.path.replace('/timesheet', '', 1)
        for path, func in endpoint_mapping.items():
            if request_path.endswith(path):
                return func()
        return jsonify({'error': 'Endpoint not found'}), 404