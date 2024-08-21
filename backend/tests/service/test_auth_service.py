import unittest

from flask_jwt_extended.exceptions import NoAuthorizationError

from app import app
from model.repository.user_repository import UserRepository
from model.user.role import UserRole
from model.user.supervisor import Supervisor
from model.user.user import User
from service.auth_service import AuthenticationService
from utils.security_utils import SecurityUtils


class TestAuthService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = cls.app.test_client()
        cls.auth_service = AuthenticationService()
        cls.user_repository = UserRepository.get_instance()

        cls.test_admin_user_data = {
            "username": "AdminAuthService",
            "role": "Admin",
            "passwordHash": SecurityUtils.hash_password("test_password"),
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Admin",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None,
            "isArchived": False,
            "slackId": None
        }
        admin_user = User.from_dict(cls.test_admin_user_data)
        cls.user_repository.create_user(admin_user)
        cls.supervisor_user_data = {
            "username": "SupervisorAuthService",
            "role": "Supervisor",
            "passwordHash": SecurityUtils.hash_password("test_password"),
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Supervisor",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "hiwis": [],
            "accountCreation": None,
            "lastLogin": None,
            "slackId": None
        }
        supervisor_user = Supervisor.from_dict(cls.supervisor_user_data)
        cls.user_repository.create_user(supervisor_user)

    @classmethod
    def tearDownClass(cls):
        cls.user_repository.delete_user("AdminAuthService")

    def test_create_token(self):
        """
        Test the create_token method of the AuthenticationService class.
        """
        with app.app_context():
            token = self.auth_service.create_token("AdminAuthService", "Admin")
            self.assertIsNotNone(token)

    def test_get_user_from_token(self):
        with self.app.app_context():
            # Create a token
            token = self.auth_service.create_token("AdminAuthService", "Admin")
            # Manually push a request context with the JWT token in the headers
            with self.app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
                # Call the method within the request context
                user = self.auth_service.get_user_from_token()
                # Perform your assertions here
                self.assertIsNotNone(user)
                self.assertIsInstance(user, User)

    def test_logout(self):
        with self.app.app_context():
            token = self.auth_service.create_token("AdminAuthService", "Admin")
            with self.app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
                response = self.auth_service.logout()
                self.assertIsNotNone(response)
                self.assertEqual(response.status_code, 200)

    def test_login_invalid_username(self):
        with self.app.app_context():
            response = self.auth_service.login("xyz", "test_password")
            self.assertEqual("Invalid username", response.message)
            self.assertEqual(401, response.status_code)
            self.assertEqual(False, response.is_successful)

    def test_login_invalid_password(self):
        with self.app.app_context():
            response = self.auth_service.login("AdminAuthService", "xyz")
            self.assertEqual("Invalid username or password", response.message)
            self.assertEqual(401, response.status_code)
            self.assertEqual(False, response.is_successful)

    def test_login(self):
        with self.app.app_context():
            response = self.auth_service.login("AdminAuthService", "test_password")
            self.assertIsNotNone(response)
            self.assertIsNotNone(response.data)


    def test_reset_password_missing_new_password(self):
        with self.app.app_context():
            response = self.auth_service.reset_password("AdminAuthService", "AdminAuthService", "")
            self.assertEqual("New password must be provided", response.message)
            self.assertEqual(400, response.status_code)
            self.assertEqual(False, response.is_successful)

    def test_reset_password_invalid_current_username(self):
        with self.app.app_context():
            response = self.auth_service.reset_password("", "AdminAuthService", "test_password")
            self.assertEqual("User not found", response.message)
            self.assertEqual(404, response.status_code)
            self.assertEqual(False, response.is_successful)

    def test_reset_password_unauthorized(self):
        with self.app.app_context():
            response = self.auth_service.reset_password("SupervisorAuthService", "AdminAuthService", "test_password")
            self.assertEqual("Password reset authorization denied", response.message)
            self.assertEqual(401, response.status_code)
            self.assertEqual(False, response.is_successful)
    def test_reset_password(self):
        with self.app.app_context():
            response = self.auth_service.reset_password("AdminAuthService", "AdminAuthService", "test_password")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()