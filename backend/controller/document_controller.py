import os.path
from datetime import datetime

from flask import request, jsonify, Blueprint, send_file, after_this_request
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from service.document.document_service import DocumentService

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
        if not month or not year or not username:
            return jsonify({'error': 'Missing required fields'}), 400

        result = self.document_service.generate_document(month, year, username)
        if result.status_code != 200:
            return jsonify({'error': result.message}), result.status_code
        file_path = result.data
        if not file_path:
            return jsonify({'error': 'Failed to generate document'}), 500
        if os.path.isfile(file_path):
            @after_this_request
            def delete_file(response):
                os.remove(file_path)
                return response


            return send_file(file_path, as_attachment=True)
        return jsonify({'error': 'Failed to generate document'}), 500

    @jwt_required()
    def generate_multiple_documents(self):
        """
        Generates multiple documents

        """

        request_data = request.args
        usernames = request_data.getlist('usernames')
        month = int(request_data.get('month'))
        year = int(request_data.get('year'))
        timesheet_ids = request_data.getlist('timesheetIds')
        start_date_str = request_data.get('startDate')
        end_date_str = request_data.get('endDate')
        username = request_data.get('username')
        if usernames and month and year:
            result = self.document_service.generate_multiple_documents(usernames, month, year)
        elif timesheet_ids:
            result = self.document_service.generate_multiple_documents_by_id(timesheet_ids)
        elif start_date_str and end_date_str and username:
            start_date = datetime.strptime(start_date_str, '%d-%m-%y')
            end_date = datetime.strptime(end_date_str, '%d-%m-%y')

            result = self.document_service.generate_document_in_date_range(start_date, end_date, username)
        else:
            return jsonify({'error': 'Missing required fields'}), 400

        if result.status_code != 200:
            return jsonify({'error': result.message}), result.status_code

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
        return jsonify({'error': 'Endpoint not found'}), 404
