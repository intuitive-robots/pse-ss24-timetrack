import unittest

from model.request_result import RequestResult


class TestRequestResult(unittest.TestCase):

    def test_to_dict(self):
        """
        Test that the to_dict method returns the correct dictionary representation of the RequestResult object
        """
        result = RequestResult(is_successful=True, message="Operation completed", status_code=200)
        self.assertEqual(result.to_dict(), {'isSuccessful': True, 'message': 'Operation completed', 'statusCode': 200})