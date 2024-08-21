import unittest
from io import BytesIO

from model.file.FileType import FileType
from model.repository.file_repository import FileRepository
from service.file_service import FileService


class TestFileService(unittest.TestCase):
    """
    Test suite for the FileService class.
    """

    @classmethod
    def setUpClass(cls):
        cls.file_service = FileService()
        cls.username = 'testUser'
        cls.file_repository = FileRepository.get_instance()
        cls.file_type = FileType.PROFILE_PICTURE
        cls.file = BytesIO(b"test file content")
        cls.file.filename = '../resources/testProfilePic.jpg'

    @classmethod
    def tearDownClass(cls):
        cls.file_service.delete_image(cls.username, cls.file_type)

    def test_upload_image_no_file(self):
        """
        Test the upload_image method of the FileService class with no file.
        """
        result = self.file_service.upload_image(None, self.username, self.file_type)
        self.assertFalse(result.is_successful)
        self.assertEqual(result.status_code, 400)
        self.assertEqual("Invalid file type or file does not exist.", result.message)

    def test_upload_image(self):
        """
        Test the upload_image method of the FileService class.
        """
        result = self.file_service.upload_image(self.file, self.username, self.file_type)
        self.assertTrue(result.is_successful)
        self.assertEqual(result.status_code, 201)

    def test_delete_image_invalid_username(self):
        """
        Test the delete_image method of the FileService class with an invalid username.
        """
        result = self.file_service.delete_image("", self.file_type)
        self.assertFalse(result.is_successful)
        self.assertEqual(result.status_code, 404)
        self.assertEqual("Image not found", result.message)

    def test_delete_image(self):
        """
        Test the delete_image method of the FileService class.
        """
        self.file_repository.upload_image(self.file, self.username, self.file_type)
        result = self.file_service.delete_image(self.username, self.file_type)
        self.assertTrue(result.is_successful)
        self.assertEqual(result.status_code, 200)
        result = self.file_service.get_image(self.username, self.file_type)
        self.assertIsNone(result)

    def test_get_image(self):
        """
        Test the get_image method of the FileService class.
        """
        self.file_repository.upload_image(self.file, self.username, self.file_type)
        result = self.file_service.get_image(self.username, self.file_type)
        self.assertIsNotNone(result)
        self.file_service.delete_image(self.username, self.file_type)

    def test_does_file_exist(self):
        """
        Test the does_file_exist method of the FileService class.
        """
        self.file_repository.upload_image(self.file, self.username, self.file_type)
        result = self.file_service.does_file_exist(self.username, self.file_type)
        self.assertTrue(result)
        self.file_service.delete_image(self.username, self.file_type)

        result = self.file_service.does_file_exist(self.username, self.file_type)
        self.assertFalse(result)