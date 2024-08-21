import datetime
import unittest

from bson import ObjectId

from db import initialize_db
from model.repository.user_repository import UserRepository
from model.user.hiwi import Hiwi
from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User
from utils.security_utils import SecurityUtils


class TestUserRepository(unittest.TestCase):
    """
    Test the UserRepository class.
    """

    @classmethod  # This decorator is used to define a
    # class method that is called before
    # tests in an individual class are run.
    def setUpClass(cls):
        cls.user_repository = UserRepository.get_instance()
        cls.db = initialize_db()
        cls.test_user_data = {
            "username": "testAdminUserRepo",
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
            "lastLogin": None,
            "isArchived": False,
            "slackId": None
        }
        cls.db.users.insert_one(cls.test_user_data)
        cls.test_user_data.pop("_id")

    @classmethod
    def tearDownClass(cls):
        cls.db.users.delete_one({"username": "testAdminUserRepo"})
        cls.db.users.delete_one({"username": "testAdminUserRepo2"})
        cls.db.users.delete_one({"username": "testHiwiUserRepo"})
        cls.db.users.delete_one({"username": "testDeleteUser"})

    def test_create_user_none(self):
        """
        Test the create_user method of the UserRepository class for None user.
        """
        response = self.user_repository.create_user(None)
        self.assertEqual("User object is None", response.message)
        self.assertEqual(False, response.is_successful)
        self.assertEqual(400, response.status_code)

    def test_create_user_already_exists(self):
        """
        Test the create_user method of the UserRepository class for an already existing user.
        """
        test_admin_data = self.user_repository.find_by_username("testAdminUserRepo")
        response_existing_user = self.user_repository.create_user(User.from_dict(test_admin_data))
        self.assertEqual("User already exists", response_existing_user.message)
        self.assertEqual(False, response_existing_user.is_successful)
        self.assertEqual(409, response_existing_user.status_code)

    def test_create_user(self):
        """
        Test the create_user method of the UserRepository class.
        """
        test_user_data = self.test_user_data
        test_user_data["username"] = "testAdminUserRepo2"
        test_user = User.from_dict(test_user_data)
        result = self.user_repository.create_user(test_user)
        self.assertEqual(True, result.is_successful)
        self.assertEqual(201, result.status_code)
        created_user_data = self.user_repository.find_by_username("testAdminUserRepo2")
        created_user_data.pop("_id")
        self.assertEqual(test_user_data, created_user_data)
        self.user_repository.delete_user("testAdminUserRepo2")

    def test_create_user_hiwi(self):
        """
        Test the create_user method of the UserRepository class for a Hiwi user.
        """
        test_user_data = {
            "username": "testHiwiUserRepo",
            "passwordHash": SecurityUtils.hash_password("test_password"),
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
            "isArchived": False,
            "slackId": None
        }

        test_user = Hiwi.from_dict(test_user_data)
        self.user_repository.create_user(test_user)
        created_user_data = self.user_repository.find_by_username("testHiwiUserRepo")
        created_user_data.pop("_id")
        created_user_data.pop("accountCreation")
        self.assertEqual(test_user_data, created_user_data)
        self.user_repository.delete_user("testHiwiUserRepo")

    def test_set_last_login_invalid_username(self):
        """
        Test the set_last_login method of the UserRepository class for an invalid username.
        """

        response = self.user_repository.set_last_login("", datetime.datetime.now())
        self.assertEqual("User not found", response.message)
        self.assertEqual(False, response.is_successful)
        self.assertEqual(404, response.status_code)

    def test_set_last_login_no_change(self):
        """
        Test the set_last_login method of the UserRepository class for no change.
        """
        received_user_data = self.user_repository.find_by_username("testAdminUserRepo")
        previous_last_login = received_user_data["lastLogin"]

        # Test for no change
        response_no_change = self.user_repository.set_last_login("testAdminUserRepo", previous_last_login)
        self.assertEqual("Last login update failed", response_no_change.message)
        self.assertEqual(False, response_no_change.is_successful)
        self.assertEqual(500, response_no_change.status_code)

    def test_set_last_login_new(self):
        received_user_data = self.user_repository.find_by_username("testAdminUserRepo")
        new_last_login = datetime.datetime(2024, 8, 1, 18, 45, 29, 170000)

        # Set new lastLogin
        response = self.user_repository.set_last_login("testAdminUserRepo", new_last_login)
        self.assertEqual("Last login updated successfully", response.message)
        self.assertEqual(True, response.is_successful)
        self.assertEqual(200, response.status_code)
        received_user_data = self.user_repository.find_by_username("testAdminUserRepo")
        self.assertEqual(received_user_data["lastLogin"], new_last_login)


    def test_find_by_username_no_username(self):
        """
        Test the find_by_username method of the UserRepository class for no username.
        """
        response = self.user_repository.find_by_username(None)
        self.assertEqual(None, response)

    def test_find_by_username_new(self):
        """
        Test the find_by_username method of the UserRepository class for a new user.
        """
        response = self.user_repository.find_by_username("testAdminUserRepo")
        self.test_user_data["username"] = "testAdminUserRepo"
        self.assertIsNotNone(response)
        response.pop("_id")
        self.assertEqual(self.test_user_data, response)


    def test_update_user_invalid_username(self):
        """
        Test the update_user method of the UserRepository class for an invalid username.
        """
        invalid_username_data = self.user_repository.find_by_username("testAdminUserRepo")
        invalid_username_data["username"] = ""
        invalid_username_user = User.from_dict(invalid_username_data)
        response_invalid_username = self.user_repository.update_user(invalid_username_user)
        self.assertEqual("User not found", response_invalid_username.message)
        self.assertEqual(False, response_invalid_username.is_successful)
        self.assertEqual(404, response_invalid_username.status_code)

    def test_update_user(self):
        """
        Test the update_user method of the UserRepository class.
        """
        test_user_data = self.user_repository.find_by_username("testAdminUserRepo")
        test_user_data["personalInfo"]["email"] = "testUpdateMethodDict@gmail.com"
        user = User.from_dict(test_user_data)
        self.user_repository.update_user(user)
        updated_user_data = self.user_repository.find_by_username("testAdminUserRepo")
        updated_user_data.pop("lastLogin")
        test_user_data.pop("lastLogin")
        self.assertEqual(test_user_data, updated_user_data)
        test_user_data["personalInfo"]["email"] = "test@gmail1.com"
        user = User.from_dict(test_user_data)
        self.user_repository.update_user(user)

    def test_delete_user_no_username(self):
        """
        Test the delete_user method of the UserRepository class for no username.
        """
        response = self.user_repository.delete_user(None)
        self.assertEqual("Please provide a username to delete the user.", response.message)
        self.assertEqual(False, response.is_successful)
        self.assertEqual(400, response.status_code)

    def test_delete_user_invalid_username(self):
        """
        Test the delete_user method of the UserRepository class for an invalid username.
        """
        response_invalid_username = self.user_repository.delete_user("invalid_username")
        self.assertEqual("User not found", response_invalid_username.message)
        self.assertEqual(False, response_invalid_username.is_successful)
        self.assertEqual(404, response_invalid_username.status_code)
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

    def test_get_users(self):
        users = self.user_repository.get_users()
        self.assertIsNotNone(users)

    def test_get_users_by_role(self):
        users_by_role = self.user_repository.get_users_by_role(UserRole.ADMIN)
        self.assertIsNotNone(users_by_role)

    if __name__ == '__main__':
        unittest.main()
