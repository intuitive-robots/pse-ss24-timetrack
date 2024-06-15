from controller.factory.user_factory import UserFactory
from model.user.personal_information import PersonalInfo
from model.user.supervisor import Supervisor


class SupervisorFactory(UserFactory):
    """
    A factory class for creating Supervisor user objects.
    Extends the UserFactory class.
    """

    def create_user(self, user_data: dict) -> Supervisor:
        """
        Creates and returns a Supervisor object based on the provided data.

        :param user_data: A dictionary containing user details including username, password hash, personal information, and a list of hiwis.
        :return: A Supervisor object initialized with the provided data.
        """
        personal_info = None
        if 'personalInfo' in user_data:
            personal_info = PersonalInfo.from_dict(user_data['personalInfo'])
        hiwis = user_data.get('hiwis', [])
        return Supervisor(
            username=user_data['username'],
            password_hash=user_data['passwordHash'],
            personal_info=personal_info,
            hiwis=hiwis
        )