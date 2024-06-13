from gridfs import GridFS, GridFSBucket

from db import initialize_db
from model.file.FileType import FileType
from model.request_result import RequestResult


class FileRepository:
    """
    Manages files stored in MongoDB using GridFS. This class handles the uploading, updating,
    retrieving, and deleting of files along with their metadata.
    """

    _instance = None

    @staticmethod
    def get_instance():
        """
        Provides a singleton instance of FileRepository.

        Returns:
            FileRepository: The singleton instance of the FileRepository.
        """
        if FileRepository._instance is None:
            FileRepository._instance = FileRepository()
        return FileRepository._instance

    def __init__(self):
        """
        Initializes the FileRepository, setting up GridFS to interact with the MongoDB database.
        """
        self.db = initialize_db()
        self.grid_fs = GridFS(self.db)
        self.grid_fs_bucket = GridFSBucket(self.db)

    def upload_image(self, file, username: str, file_type: FileType):
        """
        Uploads an image to MongoDB using GridFS, storing associated metadata.

        Args:
            file (FileStorage): The file object to be uploaded.
            username (str): The username associated with the file upload.
            file_type (FileType): The enum representing the type of the file.

        Returns:
            RequestResult: Indicates success or failure of the file upload.
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
        except Exception as e:
            return RequestResult(False, f"Failed to upload image: {str(e)}", 500)

    def update_image(self, file_content, gridfs_id: str, username: str, file_type: FileType):
        """
        Updates an existing image in GridFS and its metadata in the MongoDB database.

        Args:
            file_content (bytes): The content of the file to replace the existing file.
            gridfs_id (str): The GridFS ID of the existing file to update.
            username (str): The username associated with the file.
            file_type (FileType): The enum representing the type of the file.

        Returns:
            RequestResult: Indicates success or failure of the file update.
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
        except Exception as e:
            return RequestResult(False, f"Failed to update image: {str(e)}", 500)

    def get_image(self, username: str, file_type: FileType):
        """
        Retrieves an image file from GridFS based on username and file type.

        Args:
            username (str): The username associated with the file.
            file_type (FileType): The type of file to retrieve.

        Returns:
            A file-like object containing the image data if found; otherwise, None.
        """
        metadata = self.db.file_metadata.find_one({"username": username, "fileType": file_type.value})
        if not metadata:
            return None

        gridfs_id = metadata['gridfsId']
        file_stream = self.grid_fs_bucket.open_download_stream(gridfs_id)
        return file_stream

    def delete_image(self, gridfs_id: str):
        """
        Deletes an image and its metadata from GridFS and MongoDB.

        Args:
            gridfs_id (str): The GridFS ID of the image to delete.

        Returns:
            RequestResult: Indicates success or failure of the deletion.
        """
        self.grid_fs_bucket.delete(gridfs_id)

        metadata_delete_result = self.db.file_metadata.delete_one({"gridfsId": gridfs_id})
        if metadata_delete_result.deleted_count == 0:
            return RequestResult(False, "No metadata found for the image, or failed to delete metadata", 404)

        return RequestResult(True, "Image and metadata deleted successfully", 200)

    def does_file_exist(self, username, file_type: FileType):
        """
        Checks whether a file exists in the database based on the username and file type.

        Args:
            username (str): The username to check for the file.
            file_type (FileType): The type of file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return self.db.file_metadata.count_documents({"username": username, "fileType": file_type.value}) > 0

    def get_image_metadata(self, username: str, file_type: FileType):
        """
        Retrieves the metadata of an image based on the username and file type.

        Args:
            username (str): The username associated with the image.
            file_type (FileType): The type of the image.

        Returns:
            dict: Metadata of the image if found, otherwise None.
        """
        return self.db.file_metadata.find_one({"username": username, "fileType": file_type.value})
