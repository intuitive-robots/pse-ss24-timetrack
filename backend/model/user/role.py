from enum import Enum


class UserRole(Enum):
    """
    describes the role of a user within the system.
    There are 4 different user roles: assistant scientist (HiWi), supervisor, secretary and admin.
    """

    HIWI = "HiWi"
    SUPERVISOR = "Supervisor"
    SECRETARY = "Secretary"
    ADMIN = "Admin"

    @staticmethod
    def get_role_by_value(value: str):
        for role in UserRole:
            if role.value == value:
                return role
        return None

    def __str__(self):
        return self.value
