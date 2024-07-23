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

        responseNoUsername = self.client.get('/document/generateDocument?month=6&year=2024',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(responseNoUsername.status_code, 400)

        responseNoMonth = self.client.get('/document/generateDocument?year=2024&username=testHiwi2',
                                             headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(responseNoMonth.status_code, 400)

        responseNoYear = self.client.get('/document/generateDocument?month=6&username=testHiwi2',
                                             headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(responseNoYear.status_code, 400)

        response = self.client.get('/document/generateDocument?month=6&year=2024&username=testHiwi2',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(response.data)
    def test_generate_multiple_documents(self):
        """
        Test the generate_multiple_documents method of the DocumentController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")

        responseUsername = self.client.get('/document/generateMultipleDocuments?usernames=testHiwi1&usernames=testHiwi2&month=5&year=2024',
                                   headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(responseUsername.data)
        responseIds = self.client.get(
            '/document/generateMultipleDocuments?timesheetIds=667bd050cf0aa6181e9c8dd9&timesheetIds=667bd14ecf0aa6181e9c8dda',
            headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(responseIds.data)


        responseDates = self.client.get(
            '/document/generateMultipleDocuments?username=testHiwi1&startDate=01-03-24&endDate=01-04-24',
            headers={'Authorization': f'Bearer {access_token}'})
        self.assertIsNotNone(responseDates.data)

        responseError = self.client.get(
            '/document/generateMultipleDocuments?username=testHiwi1',
            headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(responseError.status_code, 400)
