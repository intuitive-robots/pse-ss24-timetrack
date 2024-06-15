from enum import Enum


class FileType(Enum):
    """
    Enum to represent different types of file classifications within the system.

    This enum defines specific categories of files that can be managed within the application,
    such as profile pictures and signatures. This classification helps in handling file operations
    more securely and contextually.

    Attributes:
        PROFILE_PICTURE (FileType): Represents an image used as a profile picture.
        SIGNATURE (FileType): Represents an image used as a user's signature.
    """

    PROFILE_PICTURE = "Profile Picture"
    SIGNATURE = "Signature"

    @staticmethod
    def get_type_by_value(value: str):
        """
        Searches for and returns the FileType enum member that matches the provided string value.

        :param value: The string value to match against FileType values.
        :return: The matching FileType enum member if found, otherwise None.
        """
        for file_type in FileType:
            if file_type.value == value:
                return file_type
        return None

    def __str__(self):
        """
        Returns the string representation of the enum member.

        :return: The value of the enum member as a string.
        """
        return self.value
