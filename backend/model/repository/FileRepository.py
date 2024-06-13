from gridfs import GridFS, GridFSBucket

from db import initialize_db
from model.file.FileType import FileType
from model.request_result import RequestResult


class FileRepository:
    """
    Repository class for managing files in the database using GridFS
    """
    _instance = None

    @staticmethod
    def get_instance():
        """
        Singleton instance of the FileRepository class
        :return: FileRepository instance
        """
        if FileRepository._instance is None:
            FileRepository._instance = FileRepository()
        return FileRepository._instance

    def __init__(self):
        """
        Initializes the FileRepository instance, setting up GridFS
        """
        self.db = initialize_db()
        self.grid_fs = GridFS(self.db)
        self.grid_fs_bucket = GridFSBucket(self.db)

    def upload_image(self, file, username: str, file_type: FileType):
        """
        Uploads an image file to the database using GridFS and stores metadata
        :param file: image file object to upload
        :param username: Username associated with the image
        :param file_type: Type of the file (e.g., 'profile_pic', 'signature')
        :return: RequestResult indicating the success of the operation
        """
        try:
            file_content = file.read()
            file_id = self.grid_fs.put(file_content, filename=f"{username}_{file_type}")

            metadata = {
                "username": username,
                "gridfs_id": file_id.value,
                "file_type": file_type
            }
            self.db.file_metadata.insert_one(metadata)

            return RequestResult(True, f"Image uploaded successfully with GridFS ID: {file_id}", 201)
        except Exception as e:
            return RequestResult(False, f"Failed to upload image: {str(e)}", 500)

    def get_image(self, username, file_type: FileType):
        """
        Retrieves an image from the database by username and file type
        :param username: Username associated with the image
        :param file_type: Type of the file
        :return: Image data if found, otherwise None
        """
        metadata = self.db.file_metadata.find_one({"username": username, "file_type": file_type.value})
        if metadata:
            return self.grid_fs_bucket.open_download_stream(metadata["gridfs_id"]).read()
        return None

    def delete_image(self, gridfs_id: str):
        """
        Deletes an image from the database using its GridFS ID
        :param gridfs_id: The GridFS ID of the image to delete
        :return: RequestResult indicating the success of the operation
        """
        try:
            self.grid_fs_bucket.delete(gridfs_id)
            self.db.file_metadata.delete_one({"gridfs_id": gridfs_id})
            return RequestResult(True, "Image deleted successfully", 200)
        except Exception as e:
            return RequestResult(False, f"Failed to delete image: {str(e)}", 500)

    def does_file_exist(self, username, file_type: FileType):
        """
        Checks if a file exists in the database for a given username and file type
        :param username: Username to check for the file
        :param file_type: Type of file to check
        :return: bool indicating whether the file exists
        """
        return self.db.file_metadata.count_documents({"username": username, "file_type": file_type.value}) > 0
