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

    def get_role_by_value(value):
        for role in UserRole:
            if role.value == value:
                return role
        raise ValueError("Role not found")

    def __str__(self):
        return self.value
