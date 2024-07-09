import datetime
import unittest

from bson import ObjectId

from model.repository.user_repository import UserRepository
from model.user.hiwi import Hiwi
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User
from service.user_service import UserService


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
            "username": "testAdmin10",
            "role": "Admin",
            "passwordHash": "test_password_hash",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Admin",
                "email": "test@gmail1.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }

        test_user = User.from_dict(test_user_data)
        self.user_repository.create_user(test_user)
        created_user_data = self.user_repository.find_by_username("testAdmin10")
        created_user_data.pop("_id")
        created_user_data.pop("accountCreation")
        test_user_data.pop("accountCreation")

        self.assertEqual(test_user_data, created_user_data)
        self.user_repository.delete_user("testAdmin10")

    def test_create_user_hiwi(self):
        """
        Test the create_user method of the UserRepository class for a Hiwi user.
        """
        test_user_data = {
            "username": "testHiwi10",
            "passwordHash": "test_password",
            "role": "Hiwi",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "LastName",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "contractInfo": {
                "hourlyWage": 12.40,
                "workingHours": 18,
                "vacationHours": 19
            },
            "supervisor": "testSupervisor1",
            "lastLogin": None,
            "timesheets": []
        }

        test_user = Hiwi.from_dict(test_user_data)
        self.user_repository.create_user(test_user)
        created_user_data = self.user_repository.find_by_username("testHiwi10")
        created_user_data.pop("_id")
        created_user_data.pop("accountCreation")
        self.assertEqual(test_user_data, created_user_data)
        self.user_repository.delete_user("testHiwi10")

    def test_find_by_username(self):
        """
        Test the find_by_username method of the UserRepository class.
        """
        test_user_data = {'_id': ObjectId('667c433eba00f12151afe642'),
                          'username': 'testAdmin1',
                          'personalInfo': {'firstName': 'Nico', 'lastName': 'Admin',
                                           'email': 'test@gmail1.com', 'personalNumber': '6981211',
                                           'instituteName': 'Info Institute'}, 'role': 'Admin'}
        received_user_data = self.user_repository.find_by_username("testAdmin1")
        received_user_data.pop("lastLogin")
        received_user_data.pop("passwordHash")
        received_user_data.pop("accountCreation")
        self.assertEqual(test_user_data, received_user_data)

    def test_update_user(self):
        """
        Test the update_user method of the UserRepository class.
        """
        test_user_data = self.user_repository.find_by_username("testAdmin1")
        test_user_data["personalInfo"]["email"] = "testUpdateMethodDict@gmail.com"
        user = User.from_dict(test_user_data)
        self.user_repository.update_user(user)
        updated_user_data = self.user_repository.find_by_username("testAdmin1")
        updated_user_data.pop("lastLogin")
        test_user_data.pop("lastLogin")
        self.assertEqual(test_user_data, updated_user_data)
        test_user_data["personalInfo"]["email"] = "test@gmail1.com"
        user = User.from_dict(test_user_data)
        self.user_repository.update_user(user)



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

    if __name__ == '__main__':
        unittest.main()
