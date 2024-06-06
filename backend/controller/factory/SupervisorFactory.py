from controller.factory.UserFactory import UserFactory
from model.user.personal_information import PersonalInfo
from model.user.supervisor import Supervisor
from model.user.user import User


class SupervisorFactory(UserFactory):
    def create_user(self, user_data: dict) -> Supervisor:
        """
        Creates and returns a Supervisor object based on the provided data.
        """
        personal_info = PersonalInfo.from_dict(user_data['personalInfo'])
        hiwis = user_data.get('hiwis', [])
        return Supervisor(
            username=user_data['username'],
            password_hash=user_data['passwordHash'],
            personal_info=personal_info,
            hiwis=hiwis
        )