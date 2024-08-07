from controller.factory.user_factory import UserFactory
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User


class AdminFactory(UserFactory):
    """
    A factory class for creating Admin user objects.
    Extends the UserFactory class.
    """

    def create_user(self, user_data: dict) -> User:
        """
        Creates and returns an Admin object based on the provided data.

        :param user_data: A dictionary containing user details including username, password hash, personal information and role.
        :return: A User object initialized as an Admin with the provided data.
        """
        personal_info = None
        if 'personalInfo' in user_data:
            personal_info = PersonalInfo.from_dict(user_data['personalInfo'])
        return User(
            username=user_data['username'],
            password_hash=user_data['passwordHash'],
            personal_info=personal_info,
            role=UserRole.get_role_by_value(user_data['role']),
            is_archived=user_data['isArchived']
        )
