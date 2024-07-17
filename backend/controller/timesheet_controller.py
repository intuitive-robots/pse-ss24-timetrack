from flask import jsonify, request, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.file.FileType import FileType
from model.user.role import UserRole
from service.auth_service import check_access
from service.file_service import FileService
from service.timesheet_service import TimesheetService

timesheet_blueprint = Blueprint('timesheet', __name__)


class TimesheetController(MethodView):
    """
    controller for managing timesheet-related operations such as retrieval, creation, modification,
    and deletion of timesheet entries.
    """

    def __init__(self):
        """
        Initializes TimesheetController with an instance of TimesheetService.
        """
        self.timesheet_service = TimesheetService()
        self.file_service = FileService()

    def get(self):
        """
        Handles GET requests for retrieving timesheet data based on the endpoint.

        :return: JSON response with the timesheet data or an error message.
        """
        endpoint_mapping = {
            '/get': self.get_timesheets,
            '/getByUsernameStatus': self.get_timesheets_by_username_status,
            '/getCurrentTimesheet': self.get_current_timesheet,
            '/getHighestPriorityTimesheet': self.get_highest_priority_timesheet,
            '/getByMonthYear': self.get_timesheet_by_month_year
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
            return jsonify('Request must be in JSON format'), 400
        request_data = request.get_json()
        if request_data is None:
            return jsonify('Request data is missing'), 400
        username = request_data.get('username')
        month = request_data['month']
        year = request_data.get('year')
        if not username:
            return jsonify('No username provided'), 400
        if not month:
            return jsonify('No month provided'), 400
        if not year:
            return jsonify('No year provided'), 400
        result = self.timesheet_service.ensure_timesheet_exists(username, month, year)
        return jsonify(result.message), result.status_code

    @jwt_required()
    @check_access(roles=[UserRole.HIWI])
    def sign_timesheet(self):
        """
        Allows a HiWi to sign his timesheet.

        :return: JSON response containing the status message and status code.
        """
        if not request.is_json:
            return jsonify('Request data must be in JSON format'), 400
        request_data = request.get_json()
        timesheet_id = request_data['_id']
        if timesheet_id is None:
            return jsonify( 'No timesheet ID provided'), 400
        if not self.file_service.does_file_exist(get_jwt_identity(), FileType.SIGNATURE):
            return jsonify('No signature has been uploaded.'), 400
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
            return jsonify( 'Request data must be in JSON format'), 400
        request_data = request.get_json()
        timesheet_id = request_data['_id']
        if timesheet_id is None:
            return jsonify('No timesheet ID provided'), 400
        if not self.file_service.does_file_exist(get_jwt_identity(), FileType.SIGNATURE):
            return jsonify('No signature has been uploaded.'), 400
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
            return jsonify('Request data must be in JSON format'), 400
        request_data = request.get_json()
        timesheet_id = request_data['_id']
        if timesheet_id is None:
            return jsonify('No timesheet ID provided'), 400
        if not self.file_service.does_file_exist(get_jwt_identity(), FileType.SIGNATURE):
            return jsonify('No signature has been uploaded.'), 400
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
            return jsonify('No username provided'), 400
        result = self.timesheet_service.get_timesheets_by_username(username)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify([timesheet.to_str_dict() for timesheet in result.data]), result.status_code

    @jwt_required()
    def get_timesheet_by_month_year(self):
        """
        Retrieves timesheets for the current user by month and year.

        :return: JSON response containing the timesheet data or an error message.
        """

        request_data = request.args
        username = request_data.get('username')
        month = int(request_data.get('month'))
        year = int(request_data.get('year'))
        print(username, month, year)
        if username is None:
            return jsonify('No username provided'), 400
        if month is None:
            return jsonify('No month provided'), 400
        if year is None:
            return jsonify('No year provided'), 400
        result = self.timesheet_service.get_timesheet(username, month, year)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify(result.data.to_str_dict()), result.status_code

    @jwt_required()
    def get_current_timesheet(self):
        """
        Retrieves the current timesheet for a user.

        :return: JSON response containing the current timesheet data or an error message.
        """
        username = request.args.get('username')
        if username is None:
            return jsonify('No username provided'), 400
        result = self.timesheet_service.get_current_timesheet(username)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify(result.data.to_str_dict()), result.status_code

    @jwt_required()
    def get_highest_priority_timesheet(self):
        """
        Retrieves the highest priority timesheet for a user. I. e. the oldest timesheet that isn't complete.

        :return: JSON response containing the highest priority timesheet data or an error message.
        """
        username = request.args.get('username')
        if username is None:
            return jsonify('No username provided'), 400
        result = self.timesheet_service.get_highest_priority_timesheet(username)
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        return jsonify(result.data.to_str_dict()), result.status_code

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
        if username is None:
            return jsonify('No username provided'), 400
        if status is None:
            return jsonify('No status provided'), 400
        #TODO: changes status in timesheet service to string and convert there
        timesheets = self.timesheet_service.get_timesheets_by_username_status(username, status).data
        if timesheets is None or len(timesheets) == 0:
            return jsonify('No timesheets found'), 404
        return jsonify([timesheet.to_str_dict() for timesheet in timesheets]), 200

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
        return jsonify('Endpoint not found'), 404
