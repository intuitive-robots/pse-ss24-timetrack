import os
import tempfile
from datetime import datetime

from flask import request, jsonify, Blueprint, send_file, after_this_request, Response
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from service.document.document_service import DocumentService
from service.user_service import UserService

document_blueprint = Blueprint('document', __name__)


class DocumentController(MethodView):
    """
    controller class for handling document-related requests.

    """

    def __init__(self):
        """
        Initializes the DocumentController instance

        """
        self.document_service = DocumentService()
        self.user_service = UserService()


    def get(self):
        """
        Handles GET requests for retrieving document data

        """
        endpoint_mapping = {
            '/generateDocument': self.generate_document,
            '/generateMultipleDocuments': self.generate_multiple_documents
        }
        return self._dispatch_request(endpoint_mapping)

    @jwt_required()
    def generate_document(self):
        """
        Generates a new document

        """
        request_data = request.args
        month = int(request_data.get('month'))
        year = int(request_data.get('year'))
        username = request_data.get('username')
        if not username:
            return jsonify('No username provided'), 400
        if not year:
            return jsonify('No year provided'), 400
        if not month:
            return jsonify('No month provided'), 400

        result = self.document_service.generate_document(month, year, username, get_jwt_identity())
        if result.status_code != 200:
            return jsonify(result.message), result.status_code
        file_path = result.data
        if not file_path:
            return jsonify('Failed to generate document'), 500
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_content = file.read()
            # Step 2 & 3: Create a response object and set headers for download
            response = Response(file_content)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            # Step 4: Delete the file
            os.remove(file_path)

            # Step 5: Return the response object
            return response
        return jsonify('Failed to generate document'), 500

    @jwt_required()
    def generate_multiple_documents(self):
        """
        Generates multiple documents

        """

        request_data = request.args
        usernames = request_data.getlist('usernames')
        timesheet_ids = request_data.getlist('timesheetIds')
        start_date_str = request_data.get('startDate')
        end_date_str = request_data.get('endDate')
        username = request_data.get('username')

        month_str = request_data.get('month')
        year_str = request_data.get('year')
        month = int(month_str) if month_str and month_str is not None and month_str.isdigit() else None
        year = int(year_str) if year_str and year_str is not None and year_str.isdigit() else None

        if usernames and month is not None and year is not None:
            result = self.document_service.generate_multiple_documents(usernames, month, year, get_jwt_identity())
        elif timesheet_ids:
            result = self.document_service.generate_multiple_documents_by_id(timesheet_ids, get_jwt_identity())
        elif start_date_str and end_date_str and username:
            start_date = datetime.strptime(start_date_str, '%d-%m-%y')
            end_date = datetime.strptime(end_date_str, '%d-%m-%y')

            result = self.document_service.generate_document_in_date_range(start_date, end_date, username,
                                                                           get_jwt_identity())
        else:
            return jsonify('Missing required fields'), 400

        if result.status_code != 200:
            return jsonify(result.message), result.status_code

        return send_file(result.data, as_attachment=True, download_name='documents.zip')

    def _dispatch_request(self, endpoint_mapping):
        """
        Dispatches the request to the appropriate handler based on the request path.

        :param endpoint_mapping: Dictionary mapping endpoints to function handlers.

        :return: The response from the handler or an error message if endpoint not found.
        """
        request_path = request.path.replace('/document', '', 1)
        for path, func in endpoint_mapping.items():
            if request_path.endswith(path):
                return func()
        return jsonify('Endpoint not found'), 404

