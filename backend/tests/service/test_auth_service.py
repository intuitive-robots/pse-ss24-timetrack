import unittest

from app import app
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
            response = self.auth_service.login("testAdmin1", "test_password")
            self.assertIsNotNone(response)
            self.assertIsNotNone(response.data)

    def test_reset_password(self):
        with self.app.app_context():
            response = self.auth_service.reset_password("testAdmin1", "testAdmin1", "test_password")
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()
