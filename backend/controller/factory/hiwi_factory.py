from controller.factory.user_factory import UserFactory
from model.user.contract_information import ContractInfo
from model.user.hiwi import Hiwi
from model.user.personal_information import PersonalInfo


class HiwiFactory(UserFactory):
    """
    A factory_and_validation class for creating HiWi user objects.
    Extends the UserFactory class.
    """

    def create_user(self, user_data: dict) -> Hiwi:
        """
        Creates and returns a Hiwi object based on the provided data.

        :param user_data: A dictionary containing user details including username, password hash, personal information, supervisor, and contract information.
        :return: A Hiwi object initialized with the provided data.
        """
        personal_info = None
        contract_info = None
        supervisor = None
        is_archived = False
        account_creation = None

        if 'personalInfo' in user_data:
            personal_info = PersonalInfo.from_dict(user_data['personalInfo'])
        if 'contractInfo' in user_data:
            contract_info = ContractInfo.from_dict(user_data['contractInfo'])
        if 'supervisor' in user_data:
            supervisor = user_data['supervisor']
        if 'isArchived' in user_data:
            is_archived = user_data['isArchived']
        if 'accountCreation' in user_data:
            account_creation = user_data['accountCreation']

        return Hiwi(
            username=user_data['username'],
            password_hash=user_data['passwordHash'],
            personal_info=personal_info,
            supervisor=supervisor,
            contract_info=contract_info,
            is_archived=is_archived,
            slack_id=user_data.get('slackId'),
            account_creation=account_creation
        )
