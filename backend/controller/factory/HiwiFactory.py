from controller.factory.UserFactory import UserFactory
from model.user.contract_information import ContractInfo
from model.user.hiwi import Hiwi
from model.user.personal_information import PersonalInfo
from model.user.user import User


class HiWiFactory(UserFactory):
    def create_user(self, user_data: dict) -> Hiwi:
        """
        Creates and returns a Hiwi object based on the provided data.
        """
        personal_info = PersonalInfo.from_dict(user_data['personalInfo'])
        contract_info = ContractInfo.from_dict(user_data['contractInfo'])
        return Hiwi(
            username=user_data['username'],
            password_hash=user_data['passwordHash'],
            personal_info=personal_info,
            supervisor=user_data['supervisor'],
            contract_info=contract_info
        )
