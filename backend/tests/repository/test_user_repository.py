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
            "lastLogin": None,
            "isArchived": False,
            "slackId": None
        }

        # Test for no user
        response_no_user = self.user_repository.create_user(None)
        self.assertEqual("User object is None", response_no_user.message)
        self.assertEqual(False, response_no_user.is_successful)
        self.assertEqual(400, response_no_user.status_code)

        # Test for user already existing
        test_hiwi_one = self.user_repository.find_by_username("testHiwi1")
        response_no_user = self.user_repository.create_user(User.from_dict(test_hiwi_one))
        self.assertEqual("User already exists", response_no_user.message)
        self.assertEqual(False, response_no_user.is_successful)
        self.assertEqual(409, response_no_user.status_code)

        # Test create_user method
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
                "vacationMinutes": 19,
                "overtimeMinutes": 0
            },
            "supervisor": "testSupervisor1",
            "lastLogin": None,
            "timesheets": [],
            "isArchived": False,
            "slackId": None
        }

        test_user = Hiwi.from_dict(test_user_data)
        self.user_repository.create_user(test_user)
        created_user_data = self.user_repository.find_by_username("testHiwi10")
        created_user_data.pop("_id")
        created_user_data.pop("accountCreation")
        self.assertEqual(test_user_data, created_user_data)
        self.user_repository.delete_user("testHiwi10")

    def test_set_last_login(self):
        """
        Test the set_last_login method of the UserRepository class.
        """
        received_user_data = self.user_repository.find_by_username("testAdmin1")
        previous_last_login = received_user_data["lastLogin"]
        new_last_login = datetime.datetime(2024, 8, 1, 18, 45, 29, 170000)

        # Test for invalid username
        response_invalid_username = self.user_repository.set_last_login("", previous_last_login)
        self.assertEqual("User not found", response_invalid_username.message)
        self.assertEqual(False, response_invalid_username.is_successful)
        self.assertEqual(404, response_invalid_username.status_code)

        # Test for no change
        response_no_change = self.user_repository.set_last_login("testAdmin1", previous_last_login)
        self.assertEqual("Last login update failed", response_no_change.message)
        self.assertEqual(False, response_no_change.is_successful)
        self.assertEqual(500, response_no_change.status_code)

        # Set new lastLogin
        response = self.user_repository.set_last_login("testAdmin1", new_last_login)
        self.assertEqual("Last login updated successfully", response.message)
        self.assertEqual(True, response.is_successful)
        self.assertEqual(200, response.status_code)
        received_user_data = self.user_repository.find_by_username("testAdmin1")
        self.assertEqual(received_user_data["lastLogin"], new_last_login)

        # Reset lastLogin
        response_reset = self.user_repository.set_last_login("testAdmin1", previous_last_login)
        self.assertEqual("Last login updated successfully", response_reset.message)
        self.assertEqual(True, response_reset.is_successful)
        self.assertEqual(200, response_reset.status_code)
        received_user_data = self.user_repository.find_by_username("testAdmin1")
        self.assertEqual(received_user_data["lastLogin"], previous_last_login)

    def test_find_by_username(self):
        """
        Test the find_by_username method of the UserRepository class.
        """
        test_user_data = {'_id': ObjectId('667c433eba00f12151afe642'),
                          'isArchived': False,
                          'username': 'testAdmin1',
                          'slackId': 'U07BENARPHB',
                          'personalInfo': {'firstName': 'Nico', 'lastName': 'Admin',
                                           'email': 'test@gmail1.com', 'personalNumber': '6981211',
                                           'instituteName': 'Info Institute'}, 'role': 'Admin'}

        # Test for no username
        response_no_username = self.user_repository.find_by_username(None)
        self.assertEqual(None, response_no_username)

        # Test find_by_username method
        received_user_data = self.user_repository.find_by_username("testAdmin1")
        received_user_data.pop("lastLogin")
        received_user_data.pop("accountCreation")
        received_user_data.pop("passwordHash")

        self.assertEqual(test_user_data, received_user_data)

    def test_update_user(self):
        """
        Test the update_user method of the UserRepository class.
        """
        # Test for invalid username
        invalid_username_data = self.user_repository.find_by_username("testAdmin1")
        invalid_username_data["username"] = ""
        invalid_username_user = User.from_dict(invalid_username_data)
        response_invalid_username = self.user_repository.update_user(invalid_username_user)
        self.assertEqual("User not found", response_invalid_username.message)
        self.assertEqual(False, response_invalid_username.is_successful)
        self.assertEqual(404, response_invalid_username.status_code)

        # Test update_user method
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

        # Test for no username
        response_no_username = self.user_repository.delete_user(None)
        self.assertEqual("Please provide a username to delete the user.", response_no_username.message)
        self.assertEqual(False, response_no_username.is_successful)
        self.assertEqual(400, response_no_username.status_code)

        # Test for invalid username
        response_invalid_username = self.user_repository.delete_user("")
        self.assertEqual("User not found", response_invalid_username.message)
        self.assertEqual(False, response_invalid_username.is_successful)
        self.assertEqual(404, response_invalid_username.status_code)

        # Test delete_user method
        deletionResult = self.user_repository.delete_user("Test129387")
        self.assertEqual(404, deletionResult.status_code)
        self.user_repository.delete_user("testDeleteUser")
        self.assertIsNone(self.user_repository.find_by_username("testDeleteUser"))

    def test_get_users(self):
        users = self.user_repository.get_users()
        self.assertIsNotNone(users)

    def test_get_users_by_role(self):
        users_by_role = self.user_repository.get_users_by_role(UserRole.ADMIN)
        self.assertIsNotNone(users_by_role)

    if __name__ == '__main__':
        unittest.main()
