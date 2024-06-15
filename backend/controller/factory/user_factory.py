from abc import ABC, abstractmethod

from model.user.role import UserRole
from model.user.user import User


class UserFactory(ABC):
    """
    Abstract base class for creating User objects based on user roles, including the factory method pattern.
    """

    @staticmethod
    def _role_factory_mapping():
        """
        Returns a mapping of user roles to their corresponding factory classes.

        This method imports the necessary factory classes and creates a dictionary
        that maps user role values to their respective factory classes. This mapping
        allows for dynamic creation of user instances based on their roles.

        :return: A dictionary where the keys are user role values and the values are the corresponding factory classes.
        :rtype: dict
        """
        from controller.factory.supervisor_factory import SupervisorFactory
        from controller.factory.hiwi_factory import HiwiFactory
        from controller.factory.secretary_factory import SecretaryFactory
        from controller.factory.admin_factory import AdminFactory
        return {
            UserRole.HIWI.value: HiwiFactory,
            UserRole.SUPERVISOR.value: SupervisorFactory,
            UserRole.SECRETARY.value: SecretaryFactory,
            UserRole.ADMIN.value: AdminFactory,
        }

    @staticmethod
    def get_factory(user_role: str):
        """
        Returns the factory instance associated with the given user role.

        :param user_role: The role of the user for which the factory is requested.
        :return: An instance of the appropriate factory if found, otherwise None.
        """
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
    def create_user_if_factory_exists(user_data) -> User or None:
        """
        Create a user if the corresponding factory exists based on the user role specified in user_data.

        :param user_data: A dictionary containing data needed to create a user instance.
        :return: An instance of a subclass of UserFactory or None.
        """
        factory = UserFactory.get_factory(user_data['role'])
        if not factory:
            return None
        return factory.create_user(user_data)
