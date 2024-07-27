from flask import request, jsonify, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from service.notification_service import NotificationService

notification_blueprint = Blueprint('notification', __name__)


class NotificationController(MethodView):

    def __init__(self):
        self.notification_service = NotificationService()

    def post(self):
        endpoint_mapping = {
            "/send": self.create_notification
        }
        return self._dispatch_request(endpoint_mapping)

    @jwt_required()
    def create_notification(self):
        notification_data = request.json
        result = self.notification_service.send_notification(notification_data)
        return jsonify(result.message), result.status_code

    def _dispatch_request(self, endpoint_mapping):
        """
        Dispatches the request to the appropriate handler based on the request path.

        :param endpoint_mapping: Dictionary mapping endpoints to function handlers.
        :return: The response from the handler or an error message if endpoint not found.
        """
        request_path = request.path.replace('/notification', '', 1)
        for path, func in endpoint_mapping.items():
            if request_path.endswith(path):
                return func()
        return jsonify('Endpoint not found'), 404
