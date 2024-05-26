from enum import Enum


class UserRole(Enum):
    """
    describes the role of a user within the system.
    There are 4 different user roles: assistant scientist (HiWi), supervisor, secretary and admin.
    """

    HIWI = "HIWI"
    SUPERVISOR = "SUPERVISOR"
    SECRETARY = "SECRETARY"
    ADMIN = "ADMIN"

    def __str__(self):
        return self.value
