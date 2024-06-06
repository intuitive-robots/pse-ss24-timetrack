from controller.factory.UserFactory import UserFactory
from model.user.user import User


class SecretaryFactory(UserFactory):
    def create_user(self, user_data: dict) -> User:
        return User(user_data['username'], 'Secretary')