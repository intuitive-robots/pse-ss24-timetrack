from flask import request, jsonify, Blueprint
from flask.views import MethodView

document_blueprint = Blueprint('document', __name__)


class DocumentController(MethodView):

    def __init__(self):
        """
        Initializes the DocumentController instance
        """
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
        #TODO: Implement this method
        if not request.is_json:
            return jsonify({'error': 'Request must be in JSON format'}), 400

        print("Generating document")

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
