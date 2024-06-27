import unittest

from model.file.FileType import FileType
from model.repository.file_repository import FileRepository


class TestFileRepository(unittest.TestCase):
    """
    Test the FileRepository class.
    """

    def setUp(self):
        self.file_repository = FileRepository.get_instance()

    def test_upload_image(self):
        """
        Test the upload_image method of the FileRepository class.
        """
        test_file = open("../resources/testProfilePic.jpg", "rb")
        test_file_type = FileType.PROFILE_PICTURE
        test_username = "testAdmin"
        result = self.file_repository.upload_image(test_file, test_username, test_file_type)
        self.assertTrue(result.is_successful)
        test_file.close()
        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.file_repository.delete_image(metadata["gridfsId"])

    def test_update_image(self):
        """
        Test the update_image method of the FileRepository class.
        """
        test_file = open("../resources/testProfilePic.jpg", "rb")
        test_file_type = FileType.PROFILE_PICTURE
        test_username = "testAdmin"
        self.file_repository.upload_image(test_file, test_username, test_file_type)
        test_file.close()

        updated_file = open("../resources/updateTest.jpg", "rb")
        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        result = self.file_repository.update_image(updated_file, metadata["gridfsId"], test_username, test_file_type)
        self.assertTrue(result.is_successful)
        updated_file.close()
        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.file_repository.delete_image(metadata["gridfsId"])

    def test_get_image(self):
        """
        Test the get_image method of the FileRepository class.
        """
        test_file = open("../resources/testProfilePic.jpg", "rb")
        test_file_type = FileType.PROFILE_PICTURE
        test_username = "testAdmin"
        self.file_repository.upload_image(test_file, test_username, test_file_type)
        test_file.close()

        image = self.file_repository.get_image(test_username, FileType.PROFILE_PICTURE)
        self.assertIsNotNone(image)
        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.file_repository.delete_image(metadata["gridfsId"])

    def test_delete_image(self):
        """
        Test the delete_image method of the FileRepository class.
        """
        test_file = open("../resources/testProfilePic.jpg", "rb")
        test_file_type = FileType.PROFILE_PICTURE
        test_username = "testAdmin"
        self.file_repository.upload_image(test_file, test_username, test_file_type)
        test_file.close()

        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        result = self.file_repository.delete_image(metadata["gridfsId"])
        self.assertTrue(result.is_successful)

    def test_does_file_exist(self):
        """
        Test the does_file_exist method of the FileRepository class.
        """
        test_file = open("../resources/testProfilePic.jpg", "rb")
        test_file_type = FileType.PROFILE_PICTURE
        test_username = "testAdmin"
        self.file_repository.upload_image(test_file, test_username, test_file_type)
        test_file.close()

        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.assertTrue(self.file_repository.does_file_exist(test_username, test_file_type))
        self.file_repository.delete_image(metadata["gridfsId"])

    def test_get_image_metadata(self):
        """
        Test the get_image_metadata method of the FileRepository class.
        """
        test_file = open("../resources/testProfilePic.jpg", "rb")
        test_file_type = FileType.PROFILE_PICTURE
        test_username = "testAdmin"
        self.file_repository.upload_image(test_file, test_username, test_file_type)
        test_file.close()

        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.assertIsNotNone(metadata)
        self.file_repository.delete_image(metadata["gridfsId"])