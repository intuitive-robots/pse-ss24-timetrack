import datetime
import unittest

from model.repository.user_repository import UserRepository
from model.user.hiwi import Hiwi
from model.user.role import UserRole
from model.user.user import User
from service.user_service import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()
        self.user_repository = UserRepository.get_instance()

    def test_create_user_admin(self):
        """
        Test the create_user method of the UserService class for an admin user.
        """
        test_user_data = {
            "username": "testAdmin10",
            "password": "test_password",
            "role": "Admin",
            "personalInfo": {
                "firstName": "Paul",
                "lastName": "Admin10",
                "email": "test@gmail.com",
                "personalNumber": "6981211",
                "instituteName": "Info Institute"
            },
            "lastLogin": None,
            "accountCreation": None
        }
        data_to_compare = {'username': 'testAdmin10',
                           'personalInfo': {'firstName': 'Paul',
                                            'lastName': 'Admin10',
                                            'email': 'test@gmail.com',
                                            'personalNumber': '6981211',
                                            'instituteName': 'Info Institute'},
                           'role': 'Admin',
                           'lastLogin': None}

        result = self.user_service.create_user(test_user_data)
        self.assertEqual(result.status_code, 201)
        self.assertTrue(result.is_successful)
        created_user_data = self.user_repository.find_by_username(test_user_data["username"])
        created_user_data.pop('_id')
        self.assertIsNotNone(created_user_data['passwordHash'])
        created_user_data.pop('passwordHash')
        self.assertIsNotNone(created_user_data['accountCreation'])
        created_user_data.pop('accountCreation')
        self.assertEqual(data_to_compare, created_user_data)
        self.user_repository.delete_user(test_user_data["username"])

    def test_create_user_hiwi(self):
        """
        Test the create_user method of the UserService class for a Hiwi user.
        """
        test_user_data = {
            "username": "testHiWi5",
            "password": "test_password",
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
                "vacationMinutes": 19
            },
            "supervisor": "testSupervisor1",
            "accountCreation": None,
            "lastLogin": None
        }
        data_to_compare = {'username': 'testHiWi5',
                           'personalInfo': {'firstName': 'Test',
                                            'lastName': 'LastName',
                                            'email': 'test@gmail.com',
                                            'personalNumber': '6381212',
                                            'instituteName': 'Info Institute'},
                           'role': 'Hiwi',
                           'lastLogin': None,
                           'supervisor': 'testSupervisor1',
                           'timesheets': [],
                           'contractInfo': {'hourlyWage': 12.4,
                                            'workingHours': 18,
                                            'vacationMinutes': 19}}

        result = self.user_service.create_user(test_user_data)
        self.assertEqual(result.status_code, 201)
        self.assertTrue(result.is_successful)
        created_user_data = self.user_repository.find_by_username(test_user_data["username"])
        created_user_data.pop('_id')
        self.assertIsNotNone(created_user_data['passwordHash'])
        created_user_data.pop('passwordHash')
        self.assertIsNotNone(created_user_data['accountCreation'])
        created_user_data.pop('accountCreation')
        self.assertEqual(data_to_compare, created_user_data)
        self.user_service.delete_user(test_user_data["username"])

    def test_create_user_supervisor(self):
        """
        Test the create_user method of the UserService class for a Supervisor user.
        """
        test_user_data = {
            "username": "testSupervisor10",
            "role": "Supervisor",
            "password": "test_password",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Supervisor10",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }

        data_to_compare = {'hiwis': [],
             'lastLogin': None,
             'personalInfo': {'email': 'test@gmail.com',
                              'firstName': 'Test',
                              'instituteName': 'Info Institute',
                              'lastName': 'Supervisor10',
                              'personalNumber': '6381212'},
             'role': 'Supervisor',
             'username': 'testSupervisor10'}

        result = self.user_service.create_user(test_user_data)
        self.assertEqual(result.status_code, 201)
        self.assertTrue(result.is_successful)
        created_user_data = self.user_repository.find_by_username(test_user_data["username"])
        created_user_data.pop('_id')
        self.assertIsNotNone(created_user_data['passwordHash'])
        created_user_data.pop('passwordHash')
        self.assertIsNotNone(created_user_data['accountCreation'])
        created_user_data.pop('accountCreation')
        self.assertEqual(data_to_compare, created_user_data)
        self.user_repository.delete_user(test_user_data["username"])

    def test_update_user(self):
        """
        Test the update_user method of the UserService class.
        """
        test_user_data = {
            "username": "testHiwi1",
            "role": "Hiwi",
            "personalInfo": {
                "firstName": "Martin",
                "lastName": "HiwiOne",
                "email": "updatedInTest@gmail.com",
                "personalNumber": "6381211",
                "instituteName": "Info Institute"
            }
        }
        untouched_user_data = self.user_repository.find_by_username(test_user_data["username"])
        result = self.user_service.update_user(test_user_data)
        self.assertTrue(result.is_successful)
        self.assertEqual(result.status_code, 200)
        updated_user_data = self.user_repository.find_by_username(test_user_data["username"])
        self.assertNotEqual(untouched_user_data, updated_user_data)
        self.assertEqual(updated_user_data["personalInfo"]["email"], "updatedInTest@gmail.com")
        self.user_service.update_user(untouched_user_data)

    def test_delete_user(self):
        """
        Test the delete_user method of the UserService class.
        """
        test_user_data = {
            "username": "testAdmin10",
            "password": "test_password",
            "role": "Admin",
            "personalInfo": {
                "firstName": "Paul",
                "lastName": "Admin10",
                "email": "test@gmail.com",
                "personalNumber": "6981211",
                "instituteName": "Info Institute"
            },
            "lastLogin": None,
            "accountCreation": None
        }
        self.user_service.create_user(test_user_data)
        result = self.user_service.delete_user(test_user_data["username"])
        self.assertTrue(result.is_successful)
        self.assertEqual(result.status_code, 200)
        self.assertIsNone(self.user_repository.find_by_username(test_user_data["username"]))

    def test_get_users(self):
        """
        Test the get_users method of the UserService class.
        """
        user_list = self.user_service.get_users()
        self.assertIsNotNone(user_list)
        self.assertIsInstance(user_list, list)
        for user in user_list:
            self.assertIsInstance(user, User)

    def test_get_users_by_role(self):
        """
        Test the get_users_by_role method of the UserService class.
        """
        user_list = self.user_service.get_users_by_role("Hiwi")
        self.assertIsNotNone(user_list)
        self.assertIsInstance(user_list, list)
        for user in user_list:
            self.assertIsInstance(user, User)
            self.assertEqual(user.role, UserRole.HIWI)

    def test_get_profile(self):
        """
        Test the get_profile method of the UserService class.
        """
        data_to_compare = {
            "username": "testAdmin1",
            "role": "Admin",
            "personalInfo": {
                "firstName": "Nico",
                "lastName": "Admin",
                "email": "test@gmail1.com",
                "personalNumber": "6981211",
                "instituteName": "Info Institute"
            },
            "lastLogin": None
        }
        user_data = self.user_service.get_profile("testAdmin1").to_dict()
        user_data.pop('passwordHash')
        user_data.pop('accountCreation')
        self.assertEqual(data_to_compare, user_data)

    def test_get_hiwis(self):
        """
        Test the get_hiwis method of the UserService class.
        """
        result = self.user_service.get_hiwis("testSupervisor1")
        hiwi_data = result.data
        self.assertIsNotNone(hiwi_data)
        self.assertIsInstance(hiwi_data, list)
        for hiwi in hiwi_data:
            self.assertIsInstance(hiwi, Hiwi)
            self.assertEqual(hiwi.supervisor, "testSupervisor1")





