from enum import Enum


class FileType(Enum):
    """
    Enum to represent different types of file classifications within the system.
    """

    PROFILE_PICTURE = "Profile Picture"
    SIGNATURE = "Signature"

    @staticmethod
    def get_type_by_value(value: str):
        """
        Returns the FileType enum member matching the given value.

        :param value: The string value to match.
        :return: The matching FileType enum member, or None if no match is found.
        """
        for file_type in FileType:
            if file_type.value == value:
                return file_type
        return None

    def __str__(self):
        """
        Returns the string representation of the enum member.
        """
        return self.value
