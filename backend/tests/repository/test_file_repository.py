import os
import unittest

from model.file.FileType import FileType
from model.repository.file_repository import FileRepository


class TestFileRepository(unittest.TestCase):
    """
    Test the FileRepository class.
    """

    @classmethod
    def setUpClass(cls):
        cls.file_repository = FileRepository.get_instance()
        file_path = "../resources/testProfilePic.jpg"
        if not os.path.exists(file_path):
            file_path = "tests/resources/testProfilePic.jpg"
        cls.test_file = open(file_path, "rb")
        cls.test_file_type = FileType.PROFILE_PICTURE
        updated_file_path = "../resources/testProfilePic.jpg"
        if not os.path.exists(updated_file_path):
            updated_file_path = "tests/resources/testProfilePic.jpg"
        cls.updated_file = open(updated_file_path, "rb")
        cls.created_files = []

    @classmethod
    def tearDownClass(cls):
        cls.test_file.close()
        cls.updated_file.close()
        for file_id in cls.created_files:
            cls.file_repository.delete_image(file_id)



    def test_upload_image(self):
        """
        Test the upload_image method of the FileRepository class.
        """
        test_username = "testAdmin"
        result = self.file_repository.upload_image(self.test_file, test_username, self.test_file_type)
        self.created_files.append(result.data["gridfsId"])
        self.assertTrue(result.is_successful)
        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.file_repository.delete_image(metadata["gridfsId"])

    def test_update_image(self):
        """
        Test the update_image method of the FileRepository class.
        """
        test_username = "testAdmin"
        upload_result= self.file_repository.upload_image(self.test_file, test_username, self.test_file_type)
        self.created_files.append(upload_result.data["gridfsId"])

        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        result = self.file_repository.update_image(self.updated_file, metadata["gridfsId"], test_username, self.test_file_type)
        self.assertTrue(result.is_successful)
        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.file_repository.delete_image(metadata["gridfsId"])

    def test_get_image_none(self):
        """
        Test the get_image method of the FileRepository class for no image.
        """
        test_username = "testAdmin"
        upload_result = self.file_repository.upload_image(self.test_file, test_username, self.test_file_type)
        self.created_files.append(upload_result.data["gridfsId"])
        # Test for no username
        response_no_username = self.file_repository.get_image(None, FileType.PROFILE_PICTURE)
        self.assertIsNone(response_no_username)
    def test_get_image(self):
        """
        Test the get_image method of the FileRepository class.
        """
        test_username = "testAdmin"
        upload_result = self.file_repository.upload_image(self.test_file, test_username, self.test_file_type)
        self.created_files.append(upload_result.data["gridfsId"])

        image = self.file_repository.get_image(test_username, FileType.PROFILE_PICTURE)
        self.assertIsNotNone(image)
        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.file_repository.delete_image(metadata["gridfsId"])

    def test_delete_image_none(self):
        """
        Test the delete_image method of the FileRepository class for no image.
        """
        response_no_gridfs_id = self.file_repository.delete_image(None)
        self.assertEqual("Failed to delete image: no file could be deleted because none matched None", response_no_gridfs_id.message)
        self.assertEqual(False, response_no_gridfs_id.is_successful)
        self.assertEqual(500, response_no_gridfs_id.status_code)
    def test_delete_image(self):
        """
        Test the delete_image method of the FileRepository class.
        """

        test_username = "testAdmin"
        upload_result = self.file_repository.upload_image(self.test_file, test_username, self.test_file_type)
        self.created_files.append(upload_result.data["gridfsId"])

        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        result = self.file_repository.delete_image(metadata["gridfsId"])
        self.assertTrue(result.is_successful)

    def test_does_file_exist(self):
        """
        Test the does_file_exist method of the FileRepository class.
        """

        test_username = "testAdmin"
        upload_result = self.file_repository.upload_image(self.test_file, test_username, self.test_file_type)
        self.created_files.append(upload_result.data["gridfsId"])

        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.assertTrue(self.file_repository.does_file_exist(test_username, self.test_file_type))
        self.file_repository.delete_image(metadata["gridfsId"])

    def test_get_image_metadata(self):
        """
        Test the get_image_metadata method of the FileRepository class.
        """
        test_username = "testAdmin"
        upload_result = self.file_repository.upload_image(self.test_file, test_username, self.test_file_type)
        self.created_files.append(upload_result.data["gridfsId"])

        metadata = self.file_repository.get_image_metadata(test_username, FileType.PROFILE_PICTURE)
        self.assertIsNotNone(metadata)
        self.file_repository.delete_image(metadata["gridfsId"])

    if __name__ == '__main__':
        unittest.main()
