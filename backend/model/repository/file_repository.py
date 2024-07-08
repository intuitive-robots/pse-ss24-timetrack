from gridfs import GridFS, GridFSBucket

from db import initialize_db
from model.file.FileType import FileType
from model.request_result import RequestResult
from pymongo.errors import PyMongoError


class FileRepository:
    """
    Manages files stored in MongoDB using GridFS. This class handles the uploading, updating,
    retrieving, and deleting of files along with their metadata, providing a high-level abstraction
    over the direct GridFS interactions.
    """

    _instance = None

    @staticmethod
    def get_instance():
        """
        Provides a singleton instance of FileRepository, ensuring that only one instance
        of the repository exists throughout the application lifecycle.

        :return: The singleton instance of the FileRepository.
        """
        if FileRepository._instance is None:
            FileRepository._instance = FileRepository()
        return FileRepository._instance

    def __init__(self):
        """
        Initializes the FileRepository, setting up GridFS to interact with the MongoDB database.
        This setup involves establishing a connection to the database and preparing GridFS
        and GridFSBucket instances for file operations.
        """
        self.db = initialize_db()
        self.grid_fs = GridFS(self.db)
        self.grid_fs_bucket = GridFSBucket(self.db)

    def upload_image(self, file, username: str, file_type: FileType) -> RequestResult:
        """
        Uploads an image to MongoDB using GridFS, storing associated metadata.

        
        :param file (FileStorage): The file object to be uploaded.
        :param username (str): The username associated with the file upload.
        :param file_type (FileType): The enum representing the type of the file.

        :return: A RequestResult object indicating success or failure of the file upload,
                 including a message and a status code.
        """
        try:
            file_content = file.read()
            file_id = self.grid_fs.put(file_content, filename=f"{username}_{file_type}")

            metadata = {
                "username": username,
                "gridfsId": file_id,
                "fileType": file_type.value
            }
            self.db.file_metadata.insert_one(metadata)

            return RequestResult(True, f"Image uploaded successfully with GridFS ID: {file_id}", 201)
        except PyMongoError as e:
            return RequestResult(False, f"Failed to upload image: {str(e)}", 500)

    def update_image(self, file_content, gridfs_id: str, username: str, file_type: FileType) -> RequestResult:
        """
        Updates an existing image in GridFS and its metadata in the MongoDB database.

        
        :param file_content: The new content for the file.
        :param gridfs_id: The GridFS ID of the file to update.
        :param username: The username associated with the file.
        :param file_type: The enum representing the type of the file.

        :return: A RequestResult object indicating success or failure of the file update.
        """
        try:
            self.grid_fs_bucket.delete(gridfs_id)  # Remove the old file
            new_gridfs_id = self.grid_fs.put(file_content, filename=f"{username}_{file_type.value}")

            # Update the metadata with the new GridFS ID
            self.db.file_metadata.update_one(
                {"gridfsId": gridfs_id},
                {"$set": {"gridfsId": new_gridfs_id}}
            )

            return RequestResult(True, f"Image updated successfully with new GridFS ID: {new_gridfs_id}", 201)
        except PyMongoError as e:
            return RequestResult(False, f"Failed to update image: {str(e)}", 500)

    def get_image(self, username: str, file_type: FileType):
        """
        Retrieves an image file from GridFS based on the username and file type specified,
        ensuring files are retrieved securely according to user and type.

        :param username: The username associated with the file.
        :param file_type: The type of file to retrieve.

        :return: A file-like object containing the image data if found, otherwise None.
        """
        try:
            metadata = self.db.file_metadata.find_one({"username": username, "fileType": file_type.value})
            if not metadata:
                return None
            gridfs_id = metadata['gridfsId']
            file_stream = self.grid_fs_bucket.open_download_stream(gridfs_id)
            return file_stream
        except PyMongoError as e:
            return None

    def delete_image(self, gridfs_id: str) -> RequestResult:
        """
        Deletes an image and its associated metadata from GridFS and MongoDB based on the
        GridFS ID provided.

        :param gridfs_id: The GridFS ID of the image to delete.

        :return: A RequestResult indicating success or failure of the deletion, including
                 a message and a status code.
        """
        try:
            self.grid_fs_bucket.delete(gridfs_id)
            metadata_delete_result = self.db.file_metadata.delete_one({"gridfsId": gridfs_id})
            if metadata_delete_result.deleted_count == 0:
                return RequestResult(False, "No metadata found for the image, or failed to delete metadata", 404)
            return RequestResult(True, "Image and metadata deleted successfully", 200)
        except PyMongoError as e:
            return RequestResult(False, f"Failed to delete image: {str(e)}", 500)

    def does_file_exist(self, username, file_type: FileType):
        """
        Checks whether a file exists in the database based on the username and file type specified,
        useful for validation before file operations.

        :param username: The username to check for the file.
        :param file_type: The type of file to check.

        :return: True if the file exists in the database, False otherwise.
        """
        try:
            does_file_exist = self.db.file_metadata.count_documents({"username": username, "fileType": file_type.value}) > 0
        except PyMongoError as e:
            return False
        return does_file_exist

    def get_image_metadata(self, username: str, file_type: FileType):
        """
        Retrieves metadata of an image based on the username and file type specified,
        providing detailed information about the file stored in the database.

        :param username: The username associated with the image.
        :param file_type: The type of the image.

        :return: A dictionary containing the metadata of the image if found, otherwise None.
        """
        try:
            metadata = self.db.file_metadata.find_one({"username": username, "fileType": file_type.value})
            return metadata
        except PyMongoError as e:
            return None

