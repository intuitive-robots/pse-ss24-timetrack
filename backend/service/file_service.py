import os

from model.repository.file_repository import FileRepository
from model.request_result import RequestResult
from model.file.FileType import FileType


class FileService:
    """
    Provides service-layer functionality to handle file-related operations, such as uploading,
    updating, retrieving, and deleting files. This service works with the FileRepository to
    interact with the model-data layer, ensuring files are managed according to defined business rules.

    Attributes:
        MAX_FILE_SIZE (int): The maximum allowed file size for uploads (20 MB).
        ALLOWED_EXTENSIONS (set): A set of allowed file extensions for uploads.
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
        Checks if the file's extension is among the allowed types.

        :param filename: The name of the file to check.
        :type filename: str
        :return: True if the file's extension is allowed, False otherwise.
        :rtype: bool
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def upload_image(self, file, username: str, file_type: FileType) -> RequestResult:
        """
        Handles the uploading or updating of an image file after validating its size and type.

        :param file: The file object to be uploaded, typically a Flask `request.files` object.
        :param username: The username associated with the file.
        :param file_type: The type of file, determined by an enumeration.
        :type username: str
        :type file_type: FileType
        :return: Indicates the success or failure of the upload operation.
        :rtype: RequestResult
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

        :param username: The username linked to the image.
        :param file_type: The type of the file to delete.
        :type username: str
        :type file_type: FileType
        :return: Indicates the success or failure of the delete operation.
        :rtype: RequestResult
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

        :param username: The username associated with the image.
        :param file_type: The type of file being requested.
        :type username: str
        :type file_type: FileType
        :return: The image object if found, otherwise None.
        :rtype: file-like object or None
        """
        return self.file_repository.get_image(username, file_type)

    def does_file_exist(self, username: str, file_type: FileType) -> bool:
        """
        Verifies if a particular file exists for a given username and specified file type.

        :param username: The username to check.
        :param file_type: The type of file to verify.
        :type username: str
        :type file_type: FileType
        :return: True if the file exists, otherwise False.
        :rtype: bool
        """
        return self.file_repository.does_file_exist(username, file_type)

    def delete_files_by_username(self, username: str) -> RequestResult:
        """
        Deletes all files associated with a specific username.

        :param username: The username linked to the files.
        :type username: str
        :return: Indicates the success or failure of the delete operation.
        :rtype: RequestResult
        """
        for filetype in FileType:
            if self.does_file_exist(username, filetype):
                result = self.delete_image(username, filetype)
                if not result.is_successful:
                    return result
        return RequestResult(True, "All files deleted successfully", 200)
