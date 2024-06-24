import datetime
import unittest

from bson import ObjectId

from model.repository.user_repository import UserRepository
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User


class TestUserRepository(unittest.TestCase):
    """
    Test the UserRepository class.
    """

    def setUp(self):
        self.user_repository = UserRepository.get_instance()

    def test_create_user(self):
        """
        Test the create_user method of the UserRepository class.
        """
        test_user_data = {
            "username": "testAdmin1",
            "role": "Admin",
            "passwordHash": "test_password_hash",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Admin",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }

        test_user = User.from_dict(test_user_data)
        self.user_repository.create_user(test_user)
        created_user_data = self.user_repository.find_by_username("testAdmin1")
        created_user_data.pop("_id")
        created_user_data.pop("accountCreation")
        test_user_data.pop("accountCreation")

        self.assertEqual(test_user_data, created_user_data)
        self.user_repository.delete_user("testAdmin1")

    def test_find_by_username(self):
        """
        Test the find_by_username method of the UserRepository class.
        """
        test_user_data = {
            "accountCreation": datetime.datetime(2024, 6, 24, 21, 23, 11, 302000),
            "passwordHash": "$2b$12$gUFnPv9enUu8/w8XPnv.oexAZqG3f9c3vXEkYb5h/w6lQNiK.E/9O",
            "personalInfo": {
                "email": "test@gmail.com",
                "firstName": "Test",
                "instituteName": "Info Institute",
                "lastName": "Admin",
                "personalNumber": "6381212"
            },
            "role": "Admin",
            "username": "testAdmin"
        }
        received_user_data = self.user_repository.find_by_username("testAdmin")
        received_user_data.pop("_id")
        received_user_data.pop("lastLogin")
        self.assertEqual(test_user_data, received_user_data)

    def test_update_user(self):
        """
        Test the update_user method of the UserRepository class.
        """
        test_user_data = self.user_repository.find_by_username("testAdmin")
        test_user_data["personalInfo"]["email"] = "testUpdateMethod@gmail.com"
        test_user = User.from_dict(test_user_data)
        self.user_repository.update_user(test_user)
        updated_user_data = self.user_repository.find_by_username("testAdmin")
        updated_user_data.pop("lastLogin")
        test_user_data.pop("lastLogin")
        self.assertEqual(test_user_data, updated_user_data)
        test_user_data["personalInfo"]["email"] = "usedInTests@gmail.com"
        test_user = User.from_dict(test_user_data)
        self.user_repository.update_user(test_user)

    def test_update_user_by_dict(self):
        """
        Test the update_user_by_dict method of the UserRepository class.
        """
        test_user_data = self.user_repository.find_by_username("testAdmin")
        test_user_data["personalInfo"]["email"] = "testUpdateMethodDict@gmail.com"
        self.user_repository.update_user_by_dict(test_user_data)
        updated_user_data = self.user_repository.find_by_username("testAdmin")
        updated_user_data.pop("lastLogin")
        test_user_data.pop("lastLogin")
        self.assertEqual(test_user_data, updated_user_data)
        test_user_data["personalInfo"]["email"] = "usedInTests@gmail.com"
        self.user_repository.update_user_by_dict(test_user_data)

    def test_delete_user(self):
        """
        Test the delete_user method of the UserRepository class.
        """
        self.user_repository.create_user(User("testDeleteUser", "test_password_hash",
                                              PersonalInfo("Test", "TestUser",
                                                           "testmail", "231232",
                                                           "Test Institute"), UserRole.ADMIN))
        self.user_repository.delete_user("testDeleteUser")
        self.assertIsNone(self.user_repository.find_by_username("testDeleteUser"))

