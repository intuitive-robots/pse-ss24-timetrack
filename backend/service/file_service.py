import os

from model.repository.FileRepository import FileRepository
from model.request_result import RequestResult
from model.file.FileType import FileType


class FileService:
    """
    Provides service-layer functionality to handle file-related operations, such as uploading,
    updating, retrieving, and deleting files. This service works with the FileRepository to
    interact with the model-data layer, ensuring files are managed according to defined business rules.
    """

    MAX_FILE_SIZE = 20 * 1024 * 1024  # max file size is 20 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def __init__(self):
        """
        Initializes a new instance of FileService by setting up a connection to the FileRepository.
        """
        self.file_repository = FileRepository.get_instance()

    def _allowed_file(self, filename: str) -> bool:
        """
        Private method to check if the file's extension is among the allowed types.

        Args:
            filename (str): The name of the file to check.

        Returns:
            bool: True if the file's extension is allowed, False otherwise.
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def upload_image(self, file, username: str, file_type: FileType) -> RequestResult:
        """
        Handles the uploading or updating of an image file after validating its size and type.

        Args:
            file: The file object to be uploaded, typically a Flask `request.files` object.
            username (str): The username associated with the file.
            file_type (FileType): The type of file, determined by an enumeration.

        Returns:
            RequestResult: Indicates the success or failure of the upload operation.
        """
        if not file or not self._allowed_file(file.filename):
            return RequestResult(False, "Invalid file type or file does not exist.", 400)

        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > self.MAX_FILE_SIZE:
            return RequestResult(False, "File size exceeds the allowed limit of 20 MB.", 400)

        existing_metadata = self.file_repository.get_image_metadata(username, file_type)
        if existing_metadata:
            return self.file_repository.update_image(file, existing_metadata['gridfsId'], username, file_type)

        return self.file_repository.upload_image(file, username, file_type)

    def delete_image(self, username: str, file_type: FileType) -> RequestResult:
        """
        Deletes an image associated with a specific username and file type.

        Args:
            username (str): The username linked to the image.
            file_type (FileType): The type of the file to delete.

        Returns:
            RequestResult: Indicates the success or failure of the delete operation.
        """
        image_metadata = self.file_repository.get_image_metadata(username, file_type)
        if not image_metadata:
            return RequestResult(False, "Image not found", 404)

        image_id = image_metadata.get('gridfsId')
        if not image_id:
            return RequestResult(False, "Image ID not found", 404)

        return self.file_repository.delete_image(image_id)

    def get_image(self, username: str, file_type: FileType):
        """
        Retrieves an image based on the specified username and file type.

        Args:
            username (str): The username associated with the image.
            file_type (FileType): The type of file being requested.

        Returns:
            Image object if found, otherwise None.
        """
        return self.file_repository.get_image(username, file_type)

    def does_file_exist(self, username: str, file_type: FileType) -> bool:
        """
        Verifies if a particular file exists for a given username and specified file type.

        Args:
            username (str): The username to check.
            file_type (FileType): The type of file to verify.

        Returns:
            bool: True if the file exists, otherwise False.
        """
        return self.file_repository.does_file_exist(username, file_type)
