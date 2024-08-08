import datetime
import unittest

from app import app
from model.repository.user_repository import UserRepository
from model.user.hiwi import Hiwi
from model.user.role import UserRole
from model.user.user import User
from model.user.supervisor import Supervisor
from service.user_service import UserService


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.user_service = UserService()
        self.user_repository = UserRepository.get_instance()

    def authenticate(self, username, password):
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
        test_user_data = {
            "username": "testAdmin10",
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
            "accountCreation": None

        }
        data_to_compare = {'username': 'testAdmin10',  'slackId': None,
                           'personalInfo': {'firstName': 'Paul',
                                            'lastName': 'Admin',
                                            'email': 'test@gmail.com',
                                            'personalNumber': '6981211',
                                            'instituteName': 'Info Institute'},
                           'role': 'Admin',
                           'lastLogin': None}
        with self.app.app_context():
            access_token = self.authenticate('testAdmin1', 'test_password')
            with self.app.test_request_context(headers={"Authorization": f"Bearer {access_token}"}):
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

        # Test no password
        no_password_user_data = {
            "username": "testSupervisor20",
            "role": "Supervisor",
            "password": "",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Supervisor",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }
        result_no_password = self.user_service.create_user(no_password_user_data)
        self.assertEqual(result_no_password.status_code, 400)
        self.assertFalse(result_no_password.is_successful)

        # Create supervisor
        supervisor_user_data = {
            "username": "testSupervisor10",
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
            "lastLogin": None
        }

        supervisor_data_to_compare = {'hiwis': [],
                                      'lastLogin': None,
                                      'personalInfo': {'email': 'test@gmail.com',
                                                       'firstName': 'Test',
                                                       'instituteName': 'Info Institute',
                                                       'lastName': 'Supervisor',
                                                       'personalNumber': '6381212'},
                                      'role': 'Supervisor',
                                      'slackId': None,
                                      'username': 'testSupervisor10'}

        supervisorResult = self.user_service.create_user(supervisor_user_data)
        self.assertEqual(supervisorResult.status_code, 201)
        self.assertTrue(supervisorResult.is_successful)
        created_user_data = self.user_repository.find_by_username(supervisor_user_data["username"])
        created_user_data.pop('_id')
        self.assertIsNotNone(created_user_data['passwordHash'])
        created_user_data.pop('passwordHash')
        self.assertIsNotNone(created_user_data['accountCreation'])
        created_user_data.pop('accountCreation')
        self.assertEqual(supervisor_data_to_compare, created_user_data)
        self.user_service.delete_user(supervisor_user_data["username"])

    def test_create_user_hiwi(self):
        # Test for missing field
        missing_field_data = {
            "contractInfo": {"hourlyWage": 15,
                             "workingHours": 80,
                             "vacationMinutes": 0,
                             "overtimeMinutes": 0},
            "username": "testHiwi10",
            "role": "Hiwi",
            "password": "test_password",
            'slackId': None,
            "supervisor": "testSupervisor1",
            "accountCreation": None,
            "lastLogin": None
        }
        result_missing_field = self.user_service.create_user(missing_field_data)
        self.assertEqual(False, result_missing_field.is_successful)
        self.assertEqual(400, result_missing_field.status_code)
        self.assertEqual("Missing required field: personalInfo", result_missing_field.message)

        # Test for missing supervisor
        missing_supervisor_data = {
            "contractInfo": {"hourlyWage": 15,
                             "workingHours": 80,
                             "vacationMinutes": 0,
                             "overtimeMinutes": 0},
            "username": "testHiwi10",
            "role": "Hiwi",
            "password": "test_password",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Hiwi",
                "email": "testHiwi@gmail.com",
                "personalNumber": "6381215",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            'slackId': None,
            "lastLogin": None
        }
        result_missing_supervisor = self.user_service.create_user(missing_supervisor_data)
        self.assertEqual(False, result_missing_supervisor.is_successful)
        self.assertEqual(400, result_missing_supervisor.status_code)
        self.assertEqual("Supervisor is required for Hiwi creation", result_missing_supervisor.message)

        # Test for invalid supervisor
        invalid_supervisor_data = {
            "contractInfo": {"hourlyWage": 15,
                             "workingHours": 80,
                             "vacationMinutes": 0,
                             "overtimeMinutes": 0},
            "username": "testHiwi10",
            'slackId': None,
            "supervisor": "",
            "role": "Hiwi",
            "password": "test_password",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Hiwi",
                "email": "testHiwi@gmail.com",
                "personalNumber": "6381215",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }
        result_invalid_supervisor = self.user_service.create_user(invalid_supervisor_data)
        self.assertEqual(False, result_invalid_supervisor.is_successful)
        self.assertEqual(404, result_invalid_supervisor.status_code)
        self.assertEqual("Supervisor not found", result_invalid_supervisor.message)

        # Test for invalid supervisor role
        invalid_supervisor_role_data = {
            "contractInfo": {"hourlyWage": 15,
                             "workingHours": 80,
                             "vacationMinutes": 0,
                             "overtimeMinutes": 0},
            "username": "testHiwi10",
            "supervisor": "testHiwi2",
            "role": "Hiwi",
            'slackId': None,
            "password": "test_password",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Hiwi",
                "email": "testHiwi@gmail.com",
                "personalNumber": "6381215",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }
        result_invalid_supervisor_role = self.user_service.create_user(invalid_supervisor_role_data)
        self.assertEqual(False, result_invalid_supervisor_role.is_successful)
        self.assertEqual(400, result_invalid_supervisor_role.status_code)
        self.assertEqual("Supervisor must be of role 'Supervisor'", result_invalid_supervisor_role.message)


        # Test for invalid data
        invalid_data = {
            "contractInfo": {"hourlyWage": "15",
                             "workingHours": 80,
                             "vacationMinutes": 0,
                             "overtimeMinutes": 0},
            "username": "testHiwi10",
            "role": "Hiwi",
            'slackId': None,
            "supervisor": "testSupervisor1",
            "password": "test_password",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Hiwi",
                "email": "testHiwi@gmail.com",
                "personalNumber": "6381215",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }
        result_invalid_data = self.user_service.create_user(invalid_data)
        self.assertEqual(False, result_invalid_data.is_successful)
        self.assertEqual(400, result_invalid_data.status_code)
        self.assertEqual("Invalid hourlyWage in contractInfo. Must be a positive number.", result_invalid_data.message)

        # Test for no password
        no_password_data = {
            "contractInfo": {"hourlyWage": 15,
                             "workingHours": 80,
                             "vacationMinutes": 0,
                             "overtimeMinutes": 0},
            "username": "testHiwi10",
            "role": "Hiwi",
            'slackId': None,
            "supervisor": "testSupervisor1",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Hiwi",
                "email": "testHiwi@gmail.com",
                "personalNumber": "6381215",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }
        result_no_password = self.user_service.create_user(no_password_data)
        self.assertEqual(False, result_no_password.is_successful)
        self.assertEqual(400, result_no_password.status_code)
        self.assertEqual("Password is required", result_no_password.message)

        # Test for user already exists
        user_already_exists_data = {
            "contractInfo": {"hourlyWage": 15,
                             "workingHours": 80,
                             "vacationMinutes": 0,
                             "overtimeMinutes": 0},
            "username": "testHiwi1",
            "password": "test_password",
            "role": "Hiwi",
            'slackId': None,
            "supervisor": "testSupervisor1",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Hiwi",
                "email": "testHiwi@gmail.com",
                "personalNumber": "6381215",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }
        result_user_already_exists = self.user_service.create_user(user_already_exists_data)
        self.assertEqual(False, result_user_already_exists.is_successful)
        self.assertEqual("User already exists", result_user_already_exists.message)
        self.assertEqual(409, result_user_already_exists.status_code)

        # Create hiwi
        hiwi_user_data = {
            "contractInfo": {"hourlyWage": 15,
                             "workingHours": 80,
                             "vacationMinutes": 0,
                             "overtimeMinutes": 0},
            "username": "testHiwi10",
            "role": "Hiwi",
            'slackId': None,
            "supervisor": "testSupervisor1",
            "password": "test_password",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Hiwi",
                "email": "testHiwi@gmail.com",
                "personalNumber": "6381215",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None
        }

        hiwi_data_to_compare = {'contractInfo': {'hourlyWage': 15,
                                                 'workingHours': 80,
                                                 'vacationMinutes': 0,
                                                 'overtimeMinutes': 0},
                                'lastLogin': None,
                                'personalInfo': {'email': 'testHiwi@gmail.com',
                                                 'firstName': 'Test',
                                                 'instituteName': 'Info Institute',
                                                 'lastName': 'Hiwi',
                                                 'personalNumber': '6381215'},
                                'role': 'Hiwi',
                                'slackId': None,
                                'supervisor': 'testSupervisor1',
                                'timesheets': [],
                                'username': 'testHiwi10'}

        hiwiResult = self.user_service.create_user(hiwi_user_data)
        self.assertEqual('HiWi created successfully', hiwiResult.message)
        self.assertEqual(201, hiwiResult.status_code)
        self.assertTrue(hiwiResult.is_successful)
        created_user_data = self.user_repository.find_by_username(hiwi_user_data["username"])
        created_user_data.pop('_id')
        self.assertIsNotNone(created_user_data['passwordHash'])
        created_user_data.pop('passwordHash')
        self.assertIsNotNone(created_user_data['accountCreation'])
        created_user_data.pop('accountCreation')
        self.assertEqual(hiwi_data_to_compare, created_user_data)
        deletion_result = self.user_service.delete_user("testHiwi10")


    def test_add_remove_overtime_minutes(self):
        # Test for invalid username
        result_add_invalid_user = self.user_service.add_overtime_minutes("", 10)
        self.assertEqual(False, result_add_invalid_user.is_successful)
        self.assertEqual(404, result_add_invalid_user.status_code)
        self.assertEqual("User not found", result_add_invalid_user.message)
        #print("1" + str(hiwi['contractInfo']['overtimeMinutes']))
        result_add = self.user_service.add_overtime_minutes("testHiwi1", 10)
        #hiwi = self.user_repository.find_by_username("testHiwi1")
        #print("2" + str(hiwi['contractInfo']['overtimeMinutes']))
        self.assertEqual(True, result_add.is_successful)
        self.assertEqual(200, result_add.status_code)
        self.assertEqual("User updated successfully", result_add.message)


        # Test for invalid username
        result_remove_invalid_user = self.user_service.remove_overtime_minutes("", 10)
        self.assertEqual(False, result_remove_invalid_user.is_successful)
        self.assertEqual(404, result_remove_invalid_user.status_code)
        self.assertEqual("User not found", result_remove_invalid_user.message)

        result_remove = self.user_service.remove_overtime_minutes("testHiwi1", 10)
        #hiwi = self.user_repository.find_by_username("testHiwi1")
        #print("3" + str(hiwi['contractInfo']['overtimeMinutes']))
        self.assertEqual(True, result_remove.is_successful)
        self.assertEqual(200, result_remove.status_code)
        self.assertEqual("User updated successfully", result_remove.message)


    def test_add_remove_vacation_minutes(self):
        # Test for invalid username
        result_add_invalid_user = self.user_service.add_vacation_minutes("", 10)
        self.assertEqual(False, result_add_invalid_user.is_successful)
        self.assertEqual(404, result_add_invalid_user.status_code)
        self.assertEqual("User not found", result_add_invalid_user.message)

        #hiwi = self.user_repository.find_by_username("testHiwi1")
        #print("1" + str(hiwi['contractInfo']['vacationMinutes']))
        result_add = self.user_service.add_vacation_minutes("testHiwi1", 10)
        #hiwi = self.user_repository.find_by_username("testHiwi1")
        #print("2" + str(hiwi['contractInfo']['vacationMinutes']))
        self.assertEqual(True, result_add.is_successful)
        self.assertEqual(200, result_add.status_code)
        self.assertEqual("User updated successfully", result_add.message)

        # Test for invalid username
        result_remove_invalid_user = self.user_service.remove_vacation_minutes("", 10)
        self.assertEqual(False, result_remove_invalid_user.is_successful)
        self.assertEqual(404, result_remove_invalid_user.status_code)
        self.assertEqual("User not found", result_remove_invalid_user.message)

        result_remove = self.user_service.remove_vacation_minutes("testHiwi1", 10)
        #hiwi = self.user_repository.find_by_username("testHiwi1")
        #print("3" + str(hiwi['contractInfo']['vacationMinutes']))
        self.assertEqual(True, result_remove.is_successful)
        self.assertEqual(200, result_remove.status_code)
        self.assertEqual("User updated successfully", result_remove.message)

    def test_add_remove_none_vacation_minutes(self):
        #hiwi = self.user_repository.find_by_username("testHiwi1")
        #print("1" + str(hiwi['contractInfo']['vacationMinutes']))
        result_add = self.user_service.add_vacation_minutes("testHiwi1")
        #hiwi = self.user_repository.find_by_username("testHiwi1")
        #print("2" + str(hiwi['contractInfo']['vacationMinutes']))
        self.assertEqual(True, result_add.is_successful)
        self.assertEqual(200, result_add.status_code)
        self.assertEqual("User updated successfully", result_add.message)
        result_remove = self.user_service.remove_vacation_minutes("testHiwi1")
        #hiwi = self.user_repository.find_by_username("testHiwi1")
        #print("3" + str(hiwi['contractInfo']['vacationMinutes']))
        self.assertEqual(True, result_remove.is_successful)
        self.assertEqual(200, result_remove.status_code)
        self.assertEqual("User updated successfully", result_remove.message)

    def test_update_user(self):
        """
        Test the update_user method of the UserService class.
        """
        # Test for no username
        no_username_data = {
            "role": "Hiwi",
            "personalInfo": {
                "firstName": "Martin",
                "lastName": "HiwiOne",
                "email": "updatedInTest@gmail.com",
                "personalNumber": "6381211",
                "instituteName": "Info Institute"
            }
        }
        result_no_username = self.user_service.update_user(no_username_data)
        self.assertEqual(False, result_no_username.is_successful)
        self.assertEqual(400, result_no_username.status_code)
        self.assertEqual("Username must be provided for user update", result_no_username.message)

        # Test for incorrect username
        incorrect_username_data = {
            "username": "",
            "role": "Hiwi",
            "personalInfo": {
                "firstName": "Martin",
                "lastName": "HiwiOne",
                "email": "updatedInTest@gmail.com",
                "personalNumber": "6381211",
                "instituteName": "Info Institute"
            }
        }
        result_incorrect_username = self.user_service.update_user(incorrect_username_data)
        self.assertEqual(False, result_incorrect_username.is_successful)
        self.assertEqual(404, result_incorrect_username.status_code)
        self.assertEqual("User not found", result_incorrect_username.message)

        # Test for invalid user data
        invalid_user_data = {
            "username": "testHiwi1",
            "role": "Hiwi",
            "personalInfo": {
                "firstName": "",
                "lastName": "HiwiOne",
                "email": "updatedInTest@gmail.com",
                "personalNumber": "6381211",
                "instituteName": "Info Institute"
            },
        }
        result_invalid_user_data = self.user_service.update_user(invalid_user_data)
        self.assertEqual(False, result_invalid_user_data.is_successful)
        self.assertEqual(400, result_invalid_user_data.status_code)
        self.assertEqual("Invalid or missing personal info field: firstName.", result_invalid_user_data.message)

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
        self.assertEqual(updated_user_data["personalInfo"]["email"], "updatedInTest@gmail.com")
        result = self.user_service.update_user(untouched_user_data)

    def test_delete_user(self):
        """
        Test the delete_user method of the UserService class.
        """
        # Test for incorrect username
        result_incorrect_username = self.user_service.delete_user("")
        self.assertEqual(False, result_incorrect_username.is_successful)
        self.assertEqual(404, result_incorrect_username.status_code)
        self.assertEqual("User not found", result_incorrect_username.message)

        test_user_data = {
            "username": "testAdmin10",
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
        data_to_compare = {
            "username": "testAdmin1",
            'slackId': 'U07BENARPHB',
            "role": "Admin",
            "personalInfo": {
                "firstName": "Nico",
                "lastName": "Admin",
                "email": "test@gmail.com",
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
        # Test for incorrect username
        result_incorrect_username = self.user_service.get_hiwis("")
        self.assertEqual(False, result_incorrect_username.is_successful)
        self.assertEqual(404, result_incorrect_username.status_code)
        self.assertEqual("Supervisor not found", result_incorrect_username.message)

        # Test for role != supervisor
        result_no_supervisor = self.user_service.get_hiwis("testHiwi1")
        self.assertEqual(False, result_no_supervisor.is_successful)
        self.assertEqual(400, result_no_supervisor.status_code)
        self.assertEqual("User is not a Supervisor", result_no_supervisor.message)

        result = self.user_service.get_hiwis("testSupervisor1")
        hiwi_data = result.data
        self.assertIsNotNone(hiwi_data)
        self.assertIsInstance(hiwi_data, list)
        for hiwi in hiwi_data:
            self.assertIsInstance(hiwi, Hiwi)
            self.assertEqual(hiwi.supervisor, "testSupervisor1")

    def test_get_supervisor(self):
        """
        Test the get_supervisor method of the UserService class.
        """
        # Test for incorrect hiwi username
        result_incorrect_username = self.user_service.get_supervisor("")
        self.assertEqual(False, result_incorrect_username.is_successful)
        self.assertEqual(404, result_incorrect_username.status_code)
        self.assertEqual("Hiwi not found", result_incorrect_username.message)

        # Test for role != hiwi
        result_no_hiwi = self.user_service.get_supervisor("testSupervisor1")
        self.assertEqual(False, result_no_hiwi.is_successful)
        self.assertEqual(400, result_no_hiwi.status_code)
        self.assertEqual("User is not a Hiwi", result_no_hiwi.message)

        result = self.user_service.get_supervisor("testHiwi1")
        self.assertEqual(True, result.is_successful)
        self.assertEqual(200, result.status_code)

        supervisor_data = result.data
        self.assertIsNotNone(supervisor_data)
        self.assertEqual('Marie', supervisor_data['firstName'])
        self.assertEqual('Supervisor', supervisor_data['lastName'])
        self.assertEqual('Supervisor', supervisor_data['role'])

        # Test for flag only_name = True
        result_only_name = self.user_service.get_supervisor("testHiwi1", True)
        self.assertEqual(True, result_only_name.is_successful)
        self.assertEqual(200, result_only_name.status_code)
        supervisor_data_only_name = result_only_name.data
        self.assertIsNotNone(supervisor_data_only_name)
        self.assertEqual('Marie', supervisor_data_only_name['firstName'])
        self.assertEqual('Supervisor', supervisor_data_only_name['lastName'])
    def test_get_supervisors(self):
        """
        Test the get_supervisors method of the UserService class.
        """
        expected_supervisors = [
            {'username': 'PaulKlein', 'firstName': 'Paul', 'lastName': 'Klein'},
            {'username': 'FrontendSupervisor', 'firstName': 'Maximilian', 'lastName': 'Li'},
            {'username': 'PaulMattes', 'firstName': 'Paul', 'lastName': 'Mattes'},
            {'username': 'FrontendSupervisor2', 'firstName': 'Moritz', 'lastName': 'Reuss'},
            {'username': 'testSupervisor1', 'firstName': 'Marie', 'lastName': 'Supervisor'},
            {'username': 'testSupervisor2', 'firstName': 'Elena', 'lastName': 'Supervisor2'}
        ]
        result = self.user_service.get_supervisors()
        self.assertEqual(True, result.is_successful)
        self.assertEqual(200, result.status_code)

        supervisors = result.data
        self.assertIsNotNone(supervisors)
        actual_supervisors = [supervisor.to_name_dict() for supervisor in supervisors]
        self.assertEqual(len(expected_supervisors), len(actual_supervisors))
        for expected in expected_supervisors:
            self.assertIn(expected, actual_supervisors)
