import unittest
from io import BytesIO

from model.file.FileType import FileType
from service.file_service import FileService


class TestFileService(unittest.TestCase):
    def setUp(self):
        self.file_service = FileService()

    def test_upload_image(self):
        """
        Test the upload_image method of the FileService class.
        """
        username = 'testUser'
        file_type = FileType.PROFILE_PICTURE

        # Create a dummy file for testing
        file = BytesIO(b"test file content")
        file.filename = '../resources/testProfilePic.jpg'


        # Test for no file
        result_no_file = self.file_service.upload_image(None, username, file_type)
        self.assertEqual("Invalid file type or file does not exist.", result_no_file.message)
        self.assertEqual(400, result_no_file.status_code)
        self.assertEqual(False, result_no_file.is_successful)

        result = self.file_service.upload_image(file, username, file_type)

        # Assert that the upload was successful
        self.assertTrue(result.is_successful)

        # Assert that the status code is 201 (Created)
        self.assertEqual(result.status_code, 201)

        # Clean up after test
        self.file_service.delete_image(username, file_type)

    def test_delete_image(self):
        """
        Test the delete_image method of the FileService class.
        """
        username = 'testUser'
        file_type = FileType.PROFILE_PICTURE

        # Create a dummy file for testing
        file = BytesIO(b"test file content")
        file.filename = '../resources/testProfilePic.jpg'

        # Upload the file
        self.file_service.upload_image(file, username, file_type)

        # Delete the uploaded file

        # Test for invalid username
        result_invalid_username = self.file_service.delete_image("", file_type)
        self.assertEqual("Image not found", result_invalid_username.message)
        self.assertEqual(404, result_invalid_username.status_code)
        self.assertEqual(False, result_invalid_username.is_successful)

        result = self.file_service.delete_image(username, file_type)

        # Assert that the delete operation was successful
        self.assertTrue(result.is_successful)

        # Assert that the status code is 200 (OK)
        self.assertEqual(result.status_code, 200)
        result = self.file_service.get_image(username, file_type)
        self.assertIsNone(result)

    def test_get_image(self):
        """
        Test the get_image method of the FileService class.
        """
        username = 'testUser'
        file_type = FileType.PROFILE_PICTURE

        # Create a dummy file for testing
        file = BytesIO(b"test file content")
        file.filename = '../resources/testProfilePic.jpg'

        # Upload the file
        self.file_service.upload_image(file, username, file_type)

        # Get the uploaded file
        result = self.file_service.get_image(username, file_type)

        # Assert that the file was retrieved successfully
        self.assertIsNotNone(result)

        # Clean up after test
        self.file_service.delete_image(username, file_type)

    def test_does_file_exist(self):
        """
        Test the does_file_exist method of the FileService class.
        """
        username = 'testUser'
        file_type = FileType.PROFILE_PICTURE

        # Create a dummy file for testing
        file = BytesIO(b"test file content")
        file.filename = '../resources/testProfilePic.jpg'

        # Upload the file
        self.file_service.upload_image(file, username, file_type)

        # Check if the file exists
        result = self.file_service.does_file_exist(username, file_type)

        # Assert that the file exists
        self.assertTrue(result)

        # Clean up after test
        self.file_service.delete_image(username, file_type)

        result = self.file_service.does_file_exist(username, file_type)
        self.assertFalse(result)