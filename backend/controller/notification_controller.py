from flask import request, jsonify, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from service.notification_service import NotificationService

notification_blueprint = Blueprint('notification', __name__)


class NotificationController(MethodView):

    def __init__(self):
        self.notification_service = NotificationService()

    def delete(self):
        endpoint_mapping = {
            "/delete": self.delete_notification
        }
        return self._dispatch_request(endpoint_mapping)

    def get(self):
        endpoint_mapping = {
            "/readAll": self.read_all_notifications,
            "/doesUnreadMessageExist": self.does_unread_messages_exist
        }
        return self._dispatch_request(endpoint_mapping)

    @jwt_required()
    def does_unread_messages_exist(self):
        result = self.notification_service.does_unread_message_exist()
        return jsonify(result.data), result.status_code


    @jwt_required()
    def read_all_notifications(self):
        result = self.notification_service.read_all_notifications()
        if result.is_successful:
            data_dict = [notification.to_dict() for notification in result.data]
            return jsonify(data_dict), result.status_code
        return jsonify(result.message), result.status_code

    @jwt_required()
    def delete_notification(self):
        notification_id = request.args.get("id")
        result = self.notification_service.delete_notification(notification_id)
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
