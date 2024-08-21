import unittest

from app import app
from model.repository.user_repository import UserRepository
from model.user.hiwi import Hiwi
from model.user.role import UserRole
from model.user.supervisor import Supervisor
from model.user.user import User
from service.user_service import UserService
from utils.security_utils import SecurityUtils


class TestUserService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.client = app.test_client()
        cls.user_service = UserService()
        cls.user_repository = UserRepository.get_instance()

        cls.test_admin_user_data = {
            "username": "AdminUserService",
            "role": "Admin",
            "passwordHash": SecurityUtils.hash_password("test_password"),
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
        admin_user = User.from_dict(cls.test_admin_user_data)
        cls.user_repository.create_user(admin_user)
        cls.supervisor_user_data = {
            "username": "SupervisorUserService",
            "role": "Supervisor",
            "passwordHash": SecurityUtils.hash_password("test_password"),
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Supervisor",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "hiwis": [],
            "accountCreation": None,
            "lastLogin": None,
            "slackId": None
        }
        supervisor_user = Supervisor.from_dict(cls.supervisor_user_data)
        cls.user_repository.create_user(supervisor_user)


    @classmethod
    def tearDownClass(cls):
        cls.user_repository.delete_user("AdminUserService")
        cls.user_repository.delete_user("testAdminUserService")
        cls.user_repository.delete_user("testSupervisorUserService")
        cls.user_repository.delete_user("testHiwiUserService")
        cls.user_repository.delete_user("SupervisorUserService")

    def tearDown(self):
        self.user_repository.delete_user("testSupervisorUserService")
        self.user_repository.delete_user("testHiwiUserService")

    def setUp(self):
        self.test_admin_user_data = {
            "username": "testAdminUserService",
            "password": "test_password",
            "role": "Admin",
            "personalInfo": {
                "firstName": "Paul",
                "lastName": "Admin",
                "email": "test@gmail.com",
                "personalNumber": "6981211",
                "instituteName": "Info Institute"
            },
            "lastLogin": None,
            "accountCreation": None,
            "slackId": None
        }
        self.supervisor_user_data = {
            "username": "testSupervisorUserService",
            "role": "Supervisor",
            "password": "test_password",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Supervisor",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None,
            "slackId": None
        }
        self.hiwi_user_data = {
            "username": "testHiwiUserService",
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
                "workingHours": 80
            },
            "supervisor": "testSupervisorUserService",
            "slackId": None,
            "accountCreation": None,
            "lastLogin": None
        }

    def _authenticate(self, username, password):
        """
        Authenticate the user.
        """
        user = {
            "username": username,
            "password": password
        }
        response = self.client.post('/user/login', json=user)
        return response.json['accessToken']

    def test_create_user_admin(self):
        """
        Test the create_user method of the UserService class for an admin user.
        """

        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                result = self.user_service.create_user(self.test_admin_user_data)
                self.assertEqual(result.status_code, 201)
                self.assertTrue(result.is_successful)
                created_user_data = self.user_repository.find_by_username(self.test_admin_user_data["username"])
                created_user_data.pop('_id')
                self.assertIsNotNone(created_user_data['accountCreation'])
                created_user_data.pop('accountCreation')
                self.test_admin_user_data.pop('accountCreation')
                self.assertEqual(self.test_admin_user_data, created_user_data)
                self.user_service.delete_user(self.test_admin_user_data["username"])

    def test_create_user_supervisor_without_pwd(self):
        """
        Test the create_user method of the UserService class for a Supervisor user without password.
        """
        self.supervisor_user_data.pop('password')
        result_no_password = self.user_service.create_user(self.supervisor_user_data)
        self.assertEqual(result_no_password.status_code, 400)
        self.assertFalse(result_no_password.is_successful)

    def test_create_user_supervisor(self):
        """
        Test the create_user method of the UserService class for a Supervisor user.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                supervisor_result = self.user_service.create_user(self.supervisor_user_data)
                self.assertEqual(supervisor_result.status_code, 201)
                self.assertTrue(supervisor_result.is_successful)
                created_user_data = self.user_repository.find_by_username(self.supervisor_user_data["username"])
                created_user_data.pop('_id')
                self.assertIsNotNone(created_user_data['accountCreation'])
                created_user_data.pop('accountCreation')
                created_user_data.pop('hiwis')
                self.supervisor_user_data.pop('accountCreation')
                self.assertEqual(self.supervisor_user_data, created_user_data)
                self.user_service.delete_user(self.supervisor_user_data["username"])

    def test_create_user_hiwi_missing_field(self):
        """
        Test the create_user method of the UserService class for a Hiwi user with missing field.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data.pop('contractInfo')
                result_missing_field = self.user_service.create_user(self.hiwi_user_data)
                self.assertEqual(result_missing_field.status_code, 400)
                self.assertFalse(result_missing_field.is_successful)

    def test_create_user_hiwi_invalid_supervisor(self):
        """
        Test the create_user method of the UserService class for a Hiwi user with invalid supervisor.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = ''
                result_invalid_supervisor = self.user_service.create_user(self.hiwi_user_data)
                self.assertEqual(result_invalid_supervisor.status_code, 404)
                self.assertFalse(result_invalid_supervisor.is_successful)
                self.assertEqual("Supervisor not found", result_invalid_supervisor.message)

    def test_create_user_hiwi_missing_supervisor(self):
        """
        Test the create_user method of the UserService class for a Hiwi user with missing supervisor.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data.pop('supervisor')
                result_missing_supervisor = self.user_service.create_user(self.hiwi_user_data)
                self.assertEqual(result_missing_supervisor.status_code, 400)
                self.assertFalse(result_missing_supervisor.is_successful)
                self.assertEqual("Supervisor is required for Hiwi creation", result_missing_supervisor.message)

    def test_create_user_hiwi_invalid_supervisor_role(self):
        """
        Test the create_user method of the UserService class for a Hiwi user with invalid supervisor role.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'AdminUserService'
                result_invalid_supervisor_role = self.user_service.create_user(self.hiwi_user_data)
                self.assertEqual(result_invalid_supervisor_role.status_code, 400)
                self.assertFalse(result_invalid_supervisor_role.is_successful)
                self.assertEqual("Supervisor must be of role 'Supervisor'", result_invalid_supervisor_role.message)

    def test_create_user_hiwi_invalid_data(self):
        """
        Test the create_user method of the UserService class for a Hiwi user with invalid data.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['contractInfo']['hourlyWage'] = -15
                result_invalid_data = self.user_service.create_user(self.hiwi_user_data)
                self.assertEqual(result_invalid_data.status_code, 400)
                self.assertFalse(result_invalid_data.is_successful)
                self.assertEqual("Invalid hourlyWage in contractInfo. Must be a positive number.",
                                 result_invalid_data.message)

    def test_create_user_hiwi_without_pwd(self):
        """
        Test the create_user method of the UserService class for a Hiwi user without password.
        """
        self.hiwi_user_data.pop('password')
        result_no_password = self.user_service.create_user(self.hiwi_user_data)
        self.assertEqual(result_no_password.status_code, 400)
        self.assertFalse(result_no_password.is_successful)
        self.assertEqual("Password is required", result_no_password.message)

    def test_create_user_hiwi_already_exists(self):
        """
        Test the create_user method of the UserService class for a Hiwi user that already exists.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):

                supervisor_creation_result = self.user_service.create_user(self.supervisor_user_data)
                self.hiwi_user_data['passwordHash'] = SecurityUtils.hash_password(self.hiwi_user_data['password'])
                result = self.user_repository.create_user(User.from_dict(self.hiwi_user_data))
                self.assertEqual(result.status_code, 201)
                self.assertTrue(result.is_successful)
                self.hiwi_user_data.pop('passwordHash')
                result_already_exists = self.user_service.create_user(self.hiwi_user_data)
                self.assertEqual(result_already_exists.status_code, 409)
                self.assertFalse(result_already_exists.is_successful)
                self.assertEqual("User already exists", result_already_exists.message)


    def test_create_user_hiwi(self):
        """
        Test the create_user method of the UserService class for a Hiwi user.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                supervisor_creation_result = self.user_service.create_user(self.supervisor_user_data)
                self.assertEqual(supervisor_creation_result.status_code, 201)
                self.assertTrue(supervisor_creation_result.is_successful)
                hiwi_result = self.user_service.create_user(self.hiwi_user_data)
                self.assertEqual('Hiwi created successfully', hiwi_result.message)
                self.assertEqual(201, hiwi_result.status_code)
                self.assertTrue(hiwi_result.is_successful)
                created_user_data = self.user_repository.find_by_username(self.hiwi_user_data["username"])
                created_user_data.pop('_id')
                self.assertIsNotNone(created_user_data['accountCreation'])
                created_user_data.pop('accountCreation')
                self.hiwi_user_data['contractInfo']['overtimeMinutes'] = 0
                self.hiwi_user_data['contractInfo']['vacationMinutes'] = 0
                self.hiwi_user_data.pop('accountCreation')
                self.assertEqual(self.hiwi_user_data, created_user_data)

    def test_add_overtime_minutes_invalid_username(self):
        """
        Test the add_overtime_minutes method of the UserService class.
        """
        # Test for invalid username
        result_add_invalid_user = self.user_service.add_overtime_minutes("", 10)
        self.assertEqual(False, result_add_invalid_user.is_successful)
        self.assertEqual(404, result_add_invalid_user.status_code)
        self.assertEqual("User not found", result_add_invalid_user.message)

    def test_add_overtime_minutes(self):
        """
        Test the add_overtime_minutes method of the UserService class.
        """

        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                result_add = self.user_service.add_overtime_minutes("testHiwiUserService", 10)
                self.assertEqual(True, result_add.is_successful)
                self.assertEqual(200, result_add.status_code)
                self.assertEqual("User updated successfully", result_add.message)

    def test_remove_overtime_minutes_invalid_username(self):
        """
        Test the remove_overtime_minutes method of the UserService class.
        """
        # Test for invalid username
        result_remove_invalid_user = self.user_service.remove_overtime_minutes("", 10)
        self.assertEqual(False, result_remove_invalid_user.is_successful)
        self.assertEqual(404, result_remove_invalid_user.status_code)
        self.assertEqual("User not found", result_remove_invalid_user.message)

    def test_remove_overtime_minutes(self):
        """
        Test the remove_overtime_minutes method of the UserService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                result_remove = self.user_service.remove_overtime_minutes("testHiwiUserService", 10)
                self.assertEqual(True, result_remove.is_successful)
                self.assertEqual(200, result_remove.status_code)
                self.assertEqual("User updated successfully", result_remove.message)

    def test_add_vacation_minutes_invalid_username(self):
        """
        Test the add_vacation_minutes method of the UserService class with invalid username.
        """
        # Test for invalid username
        result_add_invalid_user = self.user_service.add_vacation_minutes("", 10)
        self.assertEqual(False, result_add_invalid_user.is_successful)
        self.assertEqual(404, result_add_invalid_user.status_code)
        self.assertEqual("User not found", result_add_invalid_user.message)

    def test_add_vacation_minutes(self):
        """
        Test the add_vacation_minutes method of the UserService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                result_add = self.user_service.add_vacation_minutes("testHiwiUserService", 10)
                self.assertEqual(True, result_add.is_successful)
                self.assertEqual(200, result_add.status_code)
                self.assertEqual("User updated successfully", result_add.message)

    def test_remove_vacation_minutes_invalid_username(self):
        """
        Test the remove_vacation_minutes method of the UserService class with invalid username.
        """
        result_remove_invalid_user = self.user_service.remove_vacation_minutes("", 10)
        self.assertEqual(False, result_remove_invalid_user.is_successful)
        self.assertEqual(404, result_remove_invalid_user.status_code)
        self.assertEqual("User not found", result_remove_invalid_user.message)

    def test_remove_vacation_minutes(self):
        """
        Test the remove_vacation_minutes method of the UserService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                result_remove = self.user_service.remove_vacation_minutes("testHiwiUserService", 10)
                self.assertEqual(True, result_remove.is_successful)
                self.assertEqual(200, result_remove.status_code)
                self.assertEqual("User updated successfully", result_remove.message)


    def test_add_none_vacation_minutes(self):
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                result_add = self.user_service.add_vacation_minutes("testHiwiUserService")
                self.assertEqual(True, result_add.is_successful)
                self.assertEqual(200, result_add.status_code)
                self.assertEqual("User updated successfully", result_add.message)

    def test_remove_none_vacation_minutes(self):
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                result_remove = self.user_service.remove_vacation_minutes("testHiwiUserService")
                self.assertEqual(True, result_remove.is_successful)
                self.assertEqual(200, result_remove.status_code)
                self.assertEqual("User updated successfully", result_remove.message)



    def test_update_user_no_username(self):
        """
        Test the update_user method of the UserService class with invalid username.
        """
        self.hiwi_user_data.pop('username')
        result_invalid_username = self.user_service.update_user(self.hiwi_user_data)
        self.assertEqual(False, result_invalid_username.is_successful)
        self.assertEqual(400, result_invalid_username.status_code)
        self.assertEqual("Username must be provided for user update", result_invalid_username.message)

    def test_update_user_invalid_username(self):
        """
        Test the update_user method of the UserService class with invalid username.
        """
        self.hiwi_user_data['username'] = ''
        result_invalid_username = self.user_service.update_user(self.hiwi_user_data)
        self.assertEqual(False, result_invalid_username.is_successful)
        self.assertEqual(404, result_invalid_username.status_code)
        self.assertEqual("User not found", result_invalid_username.message)

    def test_update_user_invalid_data(self):
        """
        Test the update_user method of the UserService class with invalid data.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                self.hiwi_user_data['firstName'] = ''
                result_invalid_data = self.user_service.update_user(self.hiwi_user_data)
                self.assertEqual(False, result_invalid_data.is_successful)
                self.assertEqual(400, result_invalid_data.status_code)
                self.assertEqual("firstName cannot be empty.", result_invalid_data.message)



    def test_update_user(self):
        """
        Test the update_user method of the UserService class.
        """

        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                self.hiwi_user_data['personalInfo']['lastName'] = 'TestLastName'
                result = self.user_service.update_user(self.hiwi_user_data)
                self.assertTrue(result.is_successful)
                self.assertEqual(result.status_code, 200)
                updated_user_data = self.user_repository.find_by_username(self.hiwi_user_data["username"])
                self.assertEqual(updated_user_data["personalInfo"]["lastName"], "TestLastName")

    def test_delete_user_invalid_username(self):
        """
        Test the delete_user method of the UserService class with invalid username.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                result_invalid_username = self.user_service.delete_user("")
                self.assertEqual(False, result_invalid_username.is_successful)
                self.assertEqual(404, result_invalid_username.status_code)
                self.assertEqual("User not found", result_invalid_username.message)
    def test_delete_user(self):
        """
        Test the delete_user method of the UserService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)

                result = self.user_service.delete_user(self.hiwi_user_data["username"])
                self.assertTrue(result.is_successful)
                self.assertEqual(result.status_code, 200)
                self.assertIsNone(self.user_repository.find_by_username(self.hiwi_user_data["username"]))


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
        # Test for incorrect role name
        result_incorrect_role = self.user_service.get_users_by_role("")
        self.assertEqual(False, result_incorrect_role.is_successful)
        self.assertEqual(404, result_incorrect_role.status_code)
        self.assertEqual("Role not found", result_incorrect_role.message)

        user_list = self.user_service.get_users_by_role("Hiwi").data
        self.assertIsNotNone(user_list)
        self.assertIsInstance(user_list, list)
        for user in user_list:
            self.assertIsInstance(user, User)
            self.assertEqual(user.role, UserRole.HIWI)

    def test_get_profile(self):
        """
        Test the get_profile method of the UserService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                user_data = self.user_service.get_profile(self.hiwi_user_data['username']).to_dict()
                user_data.pop('accountCreation')
                user_data['contractInfo'].pop('overtimeMinutes')
                user_data['contractInfo'].pop('vacationMinutes')
                self.hiwi_user_data.pop('passwordHash')
                user_data.pop('passwordHash')
                self.hiwi_user_data.pop('accountCreation')
                self.assertEqual(self.hiwi_user_data, user_data)

    def test_get_hiwis_invalid_username(self):
        """
        Test the get_hiwis method of the UserService class with invalid username.
        """
        result_incorrect_username = self.user_service.get_hiwis("")
        self.assertEqual(False, result_incorrect_username.is_successful)
        self.assertEqual(404, result_incorrect_username.status_code)
        self.assertEqual("Supervisor not found", result_incorrect_username.message)

    def test_get_hiwis_role_not_supervisor(self):
        """
        Test the get_hiwis method of the UserService class with role != supervisor.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                result_no_supervisor = self.user_service.get_hiwis(self.hiwi_user_data['username'])
                self.assertEqual(False, result_no_supervisor.is_successful)
                self.assertEqual(400, result_no_supervisor.status_code)
                self.assertEqual("User is not a Supervisor", result_no_supervisor.message)

    def test_get_hiwis(self):
        """
        Test the get_hiwis method of the UserService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)

                result = self.user_service.get_hiwis("SupervisorUserService")
                hiwi_data = result.data
                self.assertIsNotNone(hiwi_data)
                self.assertIsInstance(hiwi_data, list)
                for hiwi in hiwi_data:
                    self.assertIsInstance(hiwi, Hiwi)
                    self.assertEqual(hiwi.supervisor, "SupervisorUserService")

    def test_get_supervisor_invalid_username(self):
        """
        Test the get_supervisor method of the UserService class with invalid username.
        """
        result_incorrect_username = self.user_service.get_supervisor("")
        self.assertEqual(False, result_incorrect_username.is_successful)
        self.assertEqual(404, result_incorrect_username.status_code)
        self.assertEqual("Hiwi not found", result_incorrect_username.message)

    def test_get_supervisor_role_not_hiwi(self):
        """
        Test the get_supervisor method of the UserService class with role != hiwi.
        """
        result_no_hiwi = self.user_service.get_supervisor("SupervisorUserService")
        self.assertEqual(False, result_no_hiwi.is_successful)
        self.assertEqual(400, result_no_hiwi.status_code)
        self.assertEqual("User is not a Hiwi", result_no_hiwi.message)

    def test_get_supervisor_read_only(self):
        """
        Test the get_supervisor method of the UserService class with only_name = True.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)

                result_only_name = self.user_service.get_supervisor("testHiwiUserService", True)
                self.assertEqual(True, result_only_name.is_successful)
                self.assertEqual(200, result_only_name.status_code)
                supervisor_data = result_only_name.data
                self.assertIsNotNone(supervisor_data)
                self.assertEqual(self.supervisor_user_data['personalInfo']['firstName'], supervisor_data['firstName'])
                self.assertEqual(self.supervisor_user_data['personalInfo']['lastName'], supervisor_data['lastName'])
                self.assertIsNone(supervisor_data.get('email'))

    def test_get_supervisor(self):
        """
        Test the get_supervisor method of the UserService class.
        """
        with self.app.app_context():
            access_token = self._authenticate('AdminUserService', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
                self.hiwi_user_data['supervisor'] = 'SupervisorUserService'
                hiwi_creation_result = self.user_service.create_user(self.hiwi_user_data)
                result = self.user_service.get_supervisor("testHiwiUserService")
                self.assertEqual(True, result.is_successful)
                self.assertEqual(200, result.status_code)
                supervisor_data = result.data
                self.assertIsNotNone(supervisor_data)
                self.assertEqual(self.supervisor_user_data['personalInfo']['firstName'], supervisor_data['firstName'])
                self.assertEqual(self.supervisor_user_data['personalInfo']['lastName'], supervisor_data['lastName'])
                self.assertEqual(self.supervisor_user_data['personalInfo']['email'], supervisor_data['email'])



    def test_get_supervisors(self):
        """
        Test the get_supervisors method of the UserService class.
        """
        expected_supervisors = [
            {'username': 'SupervisorUserService', 'firstName': 'Test', 'lastName': 'Supervisor'},
        ]
        result = self.user_service.get_supervisors()
        self.assertEqual(True, result.is_successful)
        self.assertEqual(200, result.status_code)

        supervisors = result.data
        self.assertIsNotNone(supervisors)
        actual_supervisors = [supervisor.to_name_dict() for supervisor in supervisors]
        for expected in expected_supervisors:
            self.assertIn(expected, actual_supervisors)
