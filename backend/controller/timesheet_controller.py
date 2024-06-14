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

    def post(self):
        """
        Handles POST requests for creating timesheets
        """
        endpoint_mapping = {
            '/ensureExists': self.ensure_timesheet_exists
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
    def ensure_timesheet_exists(self):
        """
        Ensures that a timesheet exists for the given username, month, and year.
        If the timesheet does not exist, it will be created.
        :return: The timesheet object
        """
        if not request.is_json:
            return jsonify({'error': 'Request must be in JSON format'}), 400
        request_data = request.get_json()
        if request_data is None:
            return jsonify({'error': 'Request data is missing'}), 400
        username = request_data['username']
        month = request_data['month']
        year = request_data['year']
        if not username or not month or not year:
            return jsonify({'error': 'Missing required fields'}), 400
        result = self.timesheet_service.ensure_timesheet_exists(username, month, year)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.HIWI])
    def sign_timesheet(self):
        """
        HiWi signs his timesheet
        """
        request_data = request.get_json()
        timesheet_id = request_data['timesheetId']
        
        result = self.timesheet_service.sign_timesheet(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR])
    def approve_timesheet(self):
        """
        Supervisor approves a timesheet
        """
        request_data = request.get_json()
        timesheet_id = request_data['timesheetId']
        result = self.timesheet_service.approve_timesheet(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR])
    def request_change(self):
        """
        Supervisor requests changes to a timesheet
        """
        request_data = request.get_json()
        timesheet_id = request_data['timesheetId']
        result = self.timesheet_service.request_change(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def get_timesheets(self):
        """
        Retrieves timesheets for the current user
        """
        request_data = request.get_json()
        username = request_data['username']
        result = self.timesheet_service.get_timesheets_by_username(username)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def get_timesheets_by_month_year(self):
        """
        Retrieves timesheets for the current user by month and year
        """
        request_data = request.get_json()
        username = request_data['username']
        month = request_data['month']
        year = request_data['year']
        result = self.timesheet_service.get_timesheet(username, month, year)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify(result.data.to_dict()), result.status_code

    @jwt_required()
    def get_current_timesheet(self):
        """
        Retrieves the current timesheet for a user
        """
        username = request.get_json()['username']
        result = self.timesheet_service.get_current_timesheet(username)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify(result.data.to_dict()), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR, UserRole.SECRETARY])
    def get_timesheets_by_username_status(self):
        """
        Retrieves timesheets for a specific user and status
        """
        request_data = request.get_json()
        username = request_data['username']
        status = request_data['status']
        timesheets = self.timesheet_service.get_timesheets_by_username_status(username, status)
        if timesheets is None or len(timesheets) == 0:
            return jsonify({'error': 'No timesheets found'}), 404
        return jsonify([timesheet.to_dict() for timesheet in timesheets]), 200

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
