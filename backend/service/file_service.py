import os

from model.repository.FileRepository import FileRepository
from model.request_result import RequestResult
from model.file.FileType import FileType


class FileService:

    MAX_FILE_SIZE = 20 * 1024 * 1024  # max file size is 20 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def __init__(self):
        """
        Initializes a new instance of the FileService class, which is responsible for
        managing file operations, interfacing with the FileRepository for data storage
        and retrieval.
        """
        self.file_repository = FileRepository.get_instance()

    def _allowed_file(self, filename: str) -> bool:
        """
        Check if the file's extension is in the allowed list.
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def upload_image(self, file, username: str, file_type: FileType) -> RequestResult:
        """
        Uploads or updates an image file in the system after performing checks on file size and type.
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
            return self.file_repository.update_image(file, existing_metadata['gridfs_id'], username, file_type)

        return self.file_repository.upload_image(file, username, file_type)

    def delete_image(self, username: str, file_type: FileType) -> RequestResult:
        """
        Deletes an image from the system based on the username and file type.

        :param username: Username associated with the image.
        :param file_type: FileType of the image to delete.
        :return: A RequestResult object containing the result of the operation.
        """
        image_metadata = self.file_repository.get_image_metadata(username, file_type)
        if not image_metadata:
            return RequestResult(False, "Image not found", 404)

        image_id = image_metadata.get('gridfs_id')
        if not image_id:
            return RequestResult(False, "Image ID not found", 404)

        return self.file_repository.delete_image(image_id)

    def get_image(self, username: str, file_type: FileType):
        """
        Retrieves an image based on the username and file type.

        :param username: Username associated with the image.
        :param file_type: Type of the file.
        :return: Image object if found, otherwise None.
        """
        return self.file_repository.get_image(username, file_type)

    def does_file_exist(self, username: str, file_type: FileType) -> bool:
        """
        Checks if a file exists in the system for a given username and file type.

        :param username: Username to check for the file.
        :param file_type: Type of file to check.
        :return: True if the file exists, False otherwise.
        """
        return self.file_repository.does_file_exist(username, file_type)
