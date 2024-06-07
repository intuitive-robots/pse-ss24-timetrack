from controller.factory.UserFactory import UserFactory
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User


class AdminFactory(UserFactory):
    def create_user(self, user_data: dict) -> User:
        """
        Creates and returns a Supervisor object based on the provided data.
        """
        personal_info = PersonalInfo.from_dict(user_data['personalInfo'])
        return User(
            username=user_data['username'],
            password_hash=user_data['passwordHash'],
            personal_info=personal_info,
            role=UserRole.get_role_by_value(user_data['role'])
        )