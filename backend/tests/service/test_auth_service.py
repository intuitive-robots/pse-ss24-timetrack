import unittest

from flask_jwt_extended.exceptions import NoAuthorizationError

from app import app
from model.user.role import UserRole
from model.user.user import User
from service.auth_service import AuthenticationService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.auth_service = AuthenticationService()

    def test_create_token(self):
        """
        Test the create_token method of the AuthenticationService class.
        """
        with app.app_context():
            token = self.auth_service.create_token("testAdmin1", "Admin")
            self.assertIsNotNone(token)

    def test_get_user_from_token(self):
        with self.app.app_context():
            # Create a token
            token = self.auth_service.create_token("testAdmin1", "Admin")
            # Manually push a request context with the JWT token in the headers
            with self.app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
                # Call the method within the request context
                user = self.auth_service.get_user_from_token()

                # Perform your assertions here
                self.assertIsNotNone(user)
                self.assertIsInstance(user, User)

    def test_logout(self):
        with self.app.app_context():
            token = self.auth_service.create_token("testAdmin1", "Admin")
            with self.app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
                response = self.auth_service.logout()
                self.assertIsNotNone(response)
                self.assertEqual(response.status_code, 200)

    def test_login(self):
        with self.app.app_context():
            # Test for invalid username
            response_invalid_username = self.auth_service.login("xyz", "test_password")
            self.assertEqual("Invalid username", response_invalid_username.message)
            self.assertEqual(401, response_invalid_username.status_code)
            self.assertEqual(False, response_invalid_username.is_successful)

            # Test for invalid password
            response_invalid_password = self.auth_service.login("testAdmin1", "xyz")
            self.assertEqual("Invalid username or password", response_invalid_password.message)
            self.assertEqual(401, response_invalid_password.status_code)
            self.assertEqual(False, response_invalid_password.is_successful)

            response = self.auth_service.login("testAdmin1", "test_password")
            self.assertIsNotNone(response)
            self.assertIsNotNone(response.data)

    def test_reset_password(self):
        with self.app.app_context():
            # Test for missing new password
            response_missing_password = self.auth_service.reset_password("testAdmin1", "testAdmin1", "")
            self.assertEqual("New password must be provided", response_missing_password.message)
            self.assertEqual(400, response_missing_password.status_code)
            self.assertEqual(False, response_missing_password.is_successful)

            # Test for invalid current username
            response_invalid_username = self.auth_service.reset_password("", "testAdmin1", "test_password")
            self.assertEqual("User not found", response_invalid_username.message)
            self.assertEqual(404, response_invalid_username.status_code)
            self.assertEqual(False, response_invalid_username.is_successful)

            # Test for user role != admin and current user != user
            response_authorization_denied = self.auth_service.reset_password("testHiwi1", "testAdmin1", "test_password")
            self.assertEqual("Password reset authorization denied", response_authorization_denied.message)
            self.assertEqual(401, response_authorization_denied.status_code)
            self.assertEqual(False, response_authorization_denied.is_successful)

            response = self.auth_service.reset_password("testAdmin1", "testAdmin1", "test_password")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)




if __name__ == '__main__':
    unittest.main()