from flask import jsonify, request, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from model.user.role import UserRole
from service.auth_service import check_access
from service.timesheet_service import TimesheetService

timesheet_blueprint = Blueprint('timesheet', __name__)


class TimesheetController(MethodView):
    """
    Controller for managing timesheet-related operations such as retrieval, creation, modification,
    and deletion of timesheet entries.
    """

    def __init__(self):
        """
        Initializes TimesheetController with an instance of TimesheetService.
        """
        self.timesheet_service = TimesheetService()

    def get(self):
        """
        Handles GET requests for retrieving timesheet data based on the endpoint.

        :return: JSON response with the timesheet data or an error message.
        """
        endpoint_mapping = {
            '/get': self.get_timesheets,
            '/getByUsernameStatus': self.get_timesheets_by_username_status,
            '/getCurrentTimesheet': self.get_current_timesheet,
            '/getByMonthYear': self.get_timesheets_by_month_year
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
        Handles PATCH requests for updating timesheet data based on the endpoint.

        :return: JSON response with the result of the update operation or an error message.
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
        #TODO: Get Methode falls Felder fehlen / Wiederholte Codezeilen -> Prüfung auslagern
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
        Allows a HiWi to sign his timesheet.

        :return: JSON response containing the status message and status code.
        """
        #TODO: Add this for every Post / Patch Endpoint
        if not request.is_json:
            return jsonify({'error': 'Request data must be in JSON format'}), 400
        request_data = request.get_json()
        timesheet_id = request_data['timesheetId']
        if timesheet_id is None:
            return jsonify({'error': 'No timesheet ID provided'}), 400
        result = self.timesheet_service.sign_timesheet(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR])
    def approve_timesheet(self):
        """
        Allows a supervisor to approve a timesheet.

        :return: JSON response containing the status message and status code.
        """
        if not request.is_json:
            return jsonify({'error': 'Request data must be in JSON format'}), 400
        request_data = request.get_json()
        timesheet_id = request_data['timesheetId']
        result = self.timesheet_service.approve_timesheet(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR])
    def request_change(self):
        """
        Allows a supervisor to request changes to a timesheet.

        :return: JSON response containing the status message and status code.
        """
        if not request.is_json:
            return jsonify({'error': 'Request data must be in JSON format'}), 400
        request_data = request.get_json()
        timesheet_id = request_data['timesheetId']
        result = self.timesheet_service.request_change(timesheet_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def get_timesheets(self):
        """
        Retrieves timesheets for the current user.

        :return: JSON response containing a list of timesheets or an error message.
        """

        request_data = request.args
        username = request_data.get('username')
        if username is None:
            return jsonify({'error': 'No username provided'}), 400
        result = self.timesheet_service.get_timesheets_by_username(username)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify([timesheet.to_dict() for timesheet in result.data]), result.status_code

    @jwt_required()
    def get_timesheets_by_month_year(self):
        """
        Retrieves timesheets for the current user by month and year.

        :return: JSON response containing the timesheet data or an error message.
        """

        request_data = request.args
        username = request_data.get('username')
        month = int(request_data.get('month'))
        year = int(request_data.get('year'))
        print(username, month, year)
        if username is None or month is None or year is None:
            return jsonify({'error': 'Missing required fields'}), 400
        result = self.timesheet_service.get_timesheet(username, month, year)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify(result.data.to_dict()), result.status_code

    @jwt_required()
    def get_current_timesheet(self):
        """
        Retrieves the current timesheet for a user.

        :return: JSON response containing the current timesheet data or an error message.
        """
        username = request.args.get('username')
        if username is None:
            return jsonify({'error': 'No username provided'}), 400
        result = self.timesheet_service.get_current_timesheet(username)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify(result.data.to_dict()), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.SUPERVISOR, UserRole.SECRETARY])
    def get_timesheets_by_username_status(self):
        """
        Retrieves timesheets for a specific user and status.

        :return: JSON response containing a list of timesheets or an error message.
        """

        request_data = request.args
        username = request_data.get('username')
        status = request_data.get('status')
        if username is None or status is None:
            return jsonify({'error': 'Missing required fields'}), 400
        timesheets = self.timesheet_service.get_timesheets_by_username_status(username, status)
        if timesheets is None or len(timesheets) == 0:
            return jsonify({'error': 'No timesheets found'}), 404
        return jsonify([timesheet.to_dict() for timesheet in timesheets]), 200

    def _dispatch_request(self, endpoint_mapping):
        """
        Dispatches the request to the appropriate handler based on the request path.

        :param endpoint_mapping: Dictionary mapping endpoints to function handlers.
        :return: The response from the handler or an error message if the endpoint is not found.
        """
        request_path = request.path.replace('/timesheet', '', 1)
        for path, func in endpoint_mapping.items():
            if request_path.endswith(path):
                return func()
        return jsonify({'error': 'Endpoint not found'}), 404
