import os.path

from flask import request, jsonify, Blueprint, send_file, after_this_request
from flask.views import MethodView

from service.document_service import DocumentService

document_blueprint = Blueprint('document', __name__)


class DocumentController(MethodView):

    def __init__(self):
        """
        Initializes the DocumentController instance
        """
        self.document_service = DocumentService()
        pass

    def get(self):
        """
        Handles GET requests for retrieving document data
        """
        endpoint_mapping = {
            '/generateDocument': self.generate_document,
            '/generateMultipleDocuments': self.generate_multiple_documents
        }
        return self._dispatch_request(endpoint_mapping)

    def generate_document(self):
        """
        Generates a new document
        """

        if not request.is_json:
            return jsonify({'error': 'Request must be in JSON format'}), 400
        request_data = request.get_json()
        month = request_data['month']
        year = request_data['year']
        username = request_data['username']
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


    def generate_multiple_documents(self):
        """
        Generates multiple documents
        """
        if not request.is_json:
            return jsonify({'error': 'Request must be in JSON format'}), 400
        #TODO: Implement this method
        print("Generating multiple documents")

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
