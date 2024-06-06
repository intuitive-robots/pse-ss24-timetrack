from abc import ABC, abstractmethod

from model.user.role import UserRole
from model.user.user import User


class UserFactory(ABC):

    # ROLE_FACTORY_MAPPING = {
    #     UserRole.HIWI.value: HiwiFactory,
    #     UserRole.SUPERVISOR.value: SupervisorFactory,
    #     UserRole.SECRETARY.value: SecretaryFactory
    # }

    @staticmethod
    def _role_factory_mapping():
        from controller.factory.SupervisorFactory import SupervisorFactory
        from controller.factory.HiwiFactory import HiwiFactory
        from controller.factory.SecretaryFactory import SecretaryFactory
        return {
            UserRole.HIWI.value: HiwiFactory,
            UserRole.SUPERVISOR.value: SupervisorFactory,
            UserRole.SECRETARY.value: SecretaryFactory
        }

    # @staticmethod
    # def get_factory(user_role: str):
    #     from controller.factory.HiwiFactory import HiwiFactory
    #
    #     ROLE_FACTORY_MAPPING = {
    #         UserRole.HIWI.value: HiwiFactory,
    #         UserRole.SUPERVISOR.value: SupervisorFactory,
    #         UserRole.SECRETARY.value: SecretaryFactory
    #     }
    #
    #     if user_role == UserRole.HIWI.value:
    #         from HiwiFactory import HiwiFactory
    #         return HiwiFactory()
    #     elif user_role == UserRole.SUPERVISOR.value:
    #         from SupervisorFactory import SupervisorFactory
    #         return SupervisorFactory()
    #     elif user_role == UserRole.SECRETARY.value:
    #         from SecretaryFactory import SecretaryFactory
    #         return SecretaryFactory()
    #     return None

    @staticmethod
    def get_factory(user_role: str):
        """
        Returns the factory instance associated with the given user role.

        :param user_role: The role of the user for which the factory is requested.
        :return: An instance of the appropriate factory if found, otherwise None.
        """
        # factory_class = UserFactory.ROLE_FACTORY_MAPPING.get(user_role)
        factory_class = UserFactory._role_factory_mapping().get(user_role)
        if factory_class:
            return factory_class()
        return None

    @abstractmethod
    def create_user(self, user_data: dict) -> User:
        """
        Abstract method to create a user instance based on the provided user data.

        :param user_data: A dictionary containing data needed to create a user instance.
        :return: An instance of a subclass of User.
        """
        pass

    @staticmethod
    def create_user_if_factory_exists(user_data):
        """
        create a user if the corresponding factory exists.
        :param user_data: A dictionary containing data needed to create a user instance.
        :return: An instance of a subclass of UserFactory or None.
        """
        factory = UserFactory.get_factory(user_data['role'])
        if factory:
            return factory.create_user(user_data)
        return None
