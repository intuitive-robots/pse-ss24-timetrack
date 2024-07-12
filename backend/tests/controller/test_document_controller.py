import unittest

from app import app


class TestDocumentController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.app = app


    def authenticate(self, username, password):
        """
        Authenticate the user.
        """
        user = {
            "username": username,
            "password": password
        }
        response = self.client.post('/user/login', json=user)
        return response.json['accessToken']

    def test_generate_document(self):
        """
        Test the generate_document method of the DocumentController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")

        response = self.client.get('/document/generateDocument?month=5&year=2024&username=testHiwi1', headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(response.data)

    def test_generate_multiple_documents(self):
        """
        Test the generate_multiple_documents method of the DocumentController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")

        response = self.client.get('/document/generateMultipleDocuments?usernames=testHiwi1&usernames=testHiwi2&month=5&year=2024',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(response.data)


