from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from service.time_entry_service import TimeEntryService
from service.timesheet_service import TimesheetService

time_entry_blueprint = Blueprint('time_entry', __name__)


class TimeEntryController(MethodView):
    def __init__(self):
        """
        Initialize the TimeEntryController with an instance of TimeEntryService.
        """
        self.time_entry_service = TimeEntryService()
        self.timesheet_service = TimesheetService()

    def post(self):
        """
        Handles POST requests to manage time entry-related actions such as creating time entries,
        vacation time, updating entries, and deleting entries based on the specific endpoint.
        """
        endpoint_mapping = {
            '/createWorkEntry': self.create_work_entry,
            '/createVacationEntry': self.create_vacation_entry,
            '/updateTimeEntry': self.update_time_entry,
            '/deleteTimeEntry': self.delete_time_entry
        }
        return self._dispatch_request(endpoint_mapping)

    def get(self):
        """
        Handles GET requests for retrieving time entries by their timesheet ID.
        """
        endpoint_mapping = {
            '/getEntriesByTimesheetId': self.get_entries_by_timesheet_id,
        }
        return self._dispatch_request(endpoint_mapping)

    def _dispatch_request(self, endpoint_mapping):
        """
        Dispatches the request to the appropriate handler based on the request path.

        :param endpoint_mapping: Dictionary mapping endpoints to function handlers.
        :return: The response from the handler or an error message if endpoint not found.
        """
        request_path = request.path.replace('/time_entry', '', 1)
        for path, func in endpoint_mapping.items():
            if request_path.endswith(path):
                return func()
        return jsonify({'error': 'Endpoint not found'}), 404

    @jwt_required()
    def create_work_entry(self):
        """
        Creates a new time entry with the provided JSON data.
        """
        time_entry_data = request.get_json()
        result = self.time_entry_service.create_work_entry(time_entry_data)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def create_vacation_entry(self):
        """
        Creates a new vacation time entry with the provided JSON data.
        """
        vacation_data = request.get_json()
        result = self.time_entry_service.add_vacation_entry(vacation_data)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def update_time_entry(self):
        """
        Updates an existing time entry with the provided JSON data.
        """
        time_entry_data = request.get_json()
        time_entry_id = time_entry_data.get('timeEntryId')
        time_entry_data.pop('timeEntryId')
        result = self.time_entry_service.update_time_entry(time_entry_id, time_entry_data)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def delete_time_entry(self):
        """
        Deletes a time entry identified by its ID provided in JSON data.
        """
        time_entry_id = request.get_json().get('timeEntryId')
        result = self.time_entry_service.delete_time_entry(time_entry_id)
        return jsonify(result.message), result.status_code

    @jwt_required()
    def get_entries_by_timesheet_id(self):
        """
        Retrieves all time entries associated with a specific timesheet ID.
        """
        timesheet_id = request.get_json().get('timesheetId')
        time_entries = self.time_entry_service.get_entries_of_timesheet(timesheet_id)
        time_entries_data = [entry.to_dict() for entry in time_entries]
        return jsonify(time_entries_data), 200