import os.path
import unittest

from app import app
from model.repository.user_repository import UserRepository
from model.user.user import User
from service.file_service import FileService
from service.user_service import UserService
from utils.security_utils import SecurityUtils


class TestUserController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.user_repository = UserRepository.get_instance()
        cls.user_service = UserService()
        cls.user_repository = UserRepository.get_instance()
        file_path = "../resources/testProfilePic.jpg"
        if not os.path.exists(file_path):
            file_path = "tests/resources/testProfilePic.jpg"
        cls.file = open(file_path, "rb")
        cls.admin_user_data = {
            "username": "AdminUserController",
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
        admin_user = User.from_dict(cls.admin_user_data)
        cls.user_repository.create_user(admin_user)

    def setUp(self):
        file_path = "../resources/testProfilePic.jpg"
        if not os.path.exists(file_path):
            file_path = "tests/resources/testProfilePic.jpg"
        self.file = open(file_path, "rb")
        self.test_admin_user_data = {
            "username": "testAdminUserController",
            "role": "Admin",
            "password": "test_password",
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
        self.supervisor_user_data = {
            "username": "testSupervisorUserController",
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
            "username": "testHiwiUserController",
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
            "supervisor": "testSupervisorUserController",
            "slackId": None,
            "accountCreation": None,
            "lastLogin": None
        }

    def tearDown(self):
        self.user_repository.delete_user("testAdminUserController")
        self.user_repository.delete_user("testSupervisorUserController")
        self.user_repository.delete_user("testHiwiUserController")
        self.file.close()

    @classmethod
    def tearDownClass(cls):
        cls.user_repository.delete_user("AdminUserController")
        cls.file.close()
        file_service = FileService()
        file_service.delete_files_by_username("testHiwiUserController")
        file_service.delete_files_by_username("AdminUserController")

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

    def test_login_invalid_user(self):
        """
        Test the login method of the UserController class with invalid user.
        """
        user = {
            "username": "invalid_user",
            "password": "invalid_password"
        }
        response = self.client.post('/user/login', json=user)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, "Invalid username")

    def test_login_invalid_password(self):
        """
        Test the login method of the UserController class with invalid password.
        """
        user = {
            "username": "AdminUserController",
            "password": "invalid_password"
        }
        response = self.client.post('/user/login', json=user)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, "Invalid username or password")

    def test_login_without_data(self):
        """
        Test the login method of the UserController class without data.
        """
        response = self.client.post('/user/login')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, "Request data must be in JSON format")

    def test_login(self):
        """
        Test the login method of the UserController class.
        """
        user = {
            "username": "AdminUserController",
            "password": "test_password"
        }
        response = self.client.post('/user/login', json=user)
        self.assertEqual(response.status_code, 200)

    def test_create_user_no_json(self):
        """
        Test the create_user method of the UserController class without json.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/createUser', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data must be in JSON format', response.json)

    def test_create_user(self):
        """
        Test the create_user method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/createUser', json=self.test_admin_user_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(201, response.status_code)
        user_data = self.user_repository.find_by_username("testAdminUserController")
        self.assertIsNotNone(user_data)

    def test_update_user_no_json(self):
        """
        Test the update_user method of the UserController class without json.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/updateUser', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data must be in JSON format', response.json)

    def test_update_user(self):
        """
        Test the update_user method of the UserController class.
        """

        access_token = self._authenticate("AdminUserController", "test_password")
        user_creation = self.user_service.create_user(self.test_admin_user_data)
        self.test_admin_user_data['personalInfo']['email'] = "usedInTest@gmail.com"
        response = self.client.post('/user/updateUser', json=self.test_admin_user_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        user_data = self.user_repository.find_by_username(self.test_admin_user_data['username'])
        self.assertEqual(user_data['personalInfo']['email'], "usedInTest@gmail.com")

    def test_delete_user_no_json(self):
        """
        Test the delete_user method of the UserController class without json.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.delete('/user/deleteUser', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data must be in JSON format', response.json)

    def test_delete_user(self):
        """
        Test the delete_user method of the UserController class.
        """
        self.user_service.create_user(self.test_admin_user_data)
        access_token = self._authenticate("AdminUserController", "test_password")

        response = self.client.delete('/user/deleteUser', json={"username": self.test_admin_user_data['username']},
                                      headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        user_data = self.user_repository.find_by_username(self.test_admin_user_data['username'])
        self.assertIsNone(user_data)

    def test_archive_user_no_json(self):
        """
        Test the archive_user method of the UserController class without json.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/archiveUser', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data must be in JSON format', response.json)

    def test_archive_user(self):
        """
        Test the archive_user method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        self.user_service.create_user(self.test_admin_user_data)
        response = self.client.post('/user/archiveUser', json={"username": self.test_admin_user_data['username']},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.user_service.is_archived(self.test_admin_user_data['username']))

    def test_unarchive_user_no_json(self):
        """
        Test the unarchive_user method of the UserController class without json.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/unarchiveUser', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data must be in JSON format', response.json)

    def test_unarchive_user_already_unarchived(self):
        """
        Test the unarchive_user method of the UserController class for already unarchived user.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        self.user_service.create_user(self.test_admin_user_data)
        response = self.client.post('/user/unarchiveUser', json={"username": self.test_admin_user_data['username']},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('User is not archived', response.json)

    def test_unarchive_user(self):
        """
        Test the unarchive_user method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        self.test_admin_user_data['isArchived'] = True
        self.test_admin_user_data['passwordHash'] = SecurityUtils.hash_password(self.test_admin_user_data['password'])
        self.test_admin_user_data.pop('password', None)
        self.user_repository.create_user(User.from_dict(self.test_admin_user_data))

        response = self.client.post('/user/unarchiveUser', json={"username": self.test_admin_user_data['username']},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertFalse(self.user_service.is_archived(self.test_admin_user_data['username']))

    def test_logout(self):
        """
        Test the logout method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/logout', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)

    def test_reset_password_no_json(self):
        """
        Test the reset_password method of the UserController class without json.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/resetPassword', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Request data must be in JSON format', response.json)

    def test_reset_password_archived_user(self):
        """
        Test the reset_password method of the UserController class for archived user.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        self.test_admin_user_data['isArchived'] = True
        self.test_admin_user_data['passwordHash'] = SecurityUtils.hash_password(self.test_admin_user_data['password'])
        self.test_admin_user_data.pop('password', None)
        self.user_repository.create_user(User.from_dict(self.test_admin_user_data))
        response = self.client.post('/user/resetPassword', json={"username": self.test_admin_user_data['username'],
                                                                 "password": "updated_password"},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Password of archived user cannot be reset', response.json)

    def test_reset_password(self):
        """
        Test the reset_password method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        self.user_service.create_user(self.test_admin_user_data)
        user_data = self.user_repository.find_by_username(self.test_admin_user_data['username'])
        password_hash = user_data['passwordHash']

        response = self.client.post('/user/resetPassword', json={"username": self.test_admin_user_data['username'],
                                                                 "password": "updated_password"},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        user_data = self.user_repository.find_by_username(self.test_admin_user_data['username'])
        new_password_hash = user_data['passwordHash']
        self.assertNotEqual(password_hash, new_password_hash)

    def test_get_profile(self):
        """
        Test the get_profile method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.get('/user/getProfile', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], "AdminUserController")

    def test_get_contract_info_no_json(self):
        """
        Test the get_contract_info method of the UserController class without json.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.get('/user/getContractInfo', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Username parameter is required', response.json)

    def test_get_contract_info(self):
        """
        Test the get_contract_info method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        supervisor_creation = self.user_service.create_user(self.supervisor_user_data)
        hiwi_creation = self.user_service.create_user(self.hiwi_user_data)

        response = self.client.get('/user/getContractInfo?username=' + self.hiwi_user_data['username'],
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(12.4, response.json['hourlyWage'])

    def test_get_users(self):
        """
        Test the get_users method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.get('/user/getUsers', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_archived_users(self):
        """
        Test the get_archived_users method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        self.user_service.create_user(self.test_admin_user_data)
        self.user_service.archive_user("testAdminUserController")

        response = self.client.get('/user/getArchivedUsers', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        archived_users = [user['username'] for user in response.json]
        self.assertTrue("testAdminUserController" in archived_users)

    def test_get_users_by_role_no_json(self):
        """
        Test the get_users_by_role method of the UserController class without json.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.get('/user/getUsersByRole', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual('Role parameter is required', response.json)

    def test_get_users_by_role_admin(self):
        """
        Test the get_users_by_role method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.get('/user/getUsersByRole?role=Admin',
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
        for admin in response.json:
            self.assertEqual(admin['role'], "Admin")

    def test_get_users_by_role_hiwi(self):
        """
        Test the get_users_by_role method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        supervisor_creation = self.user_service.create_user(self.supervisor_user_data)
        hiwi_creation = self.user_service.create_user(self.hiwi_user_data)
        response = self.client.get('/user/getUsersByRole?role=Hiwi',
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
        for hiwi in response.json:
            self.assertEqual(hiwi['role'], "Hiwi")

    def test_get_users_by_role_supervisor(self):
        """
        Test the get_users_by_role method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        supervisor_creation = self.user_service.create_user(self.supervisor_user_data)
        response = self.client.get('/user/getUsersByRole?role=Supervisor',
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
        for supervisor in response.json:
            self.assertEqual(supervisor['role'], "Supervisor")

    def test_upload_user_file_no_file(self):
        """
        Test the upload_user_file method of the UserController class without file.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/uploadFile?username=testHiwi1&fileType=Signature',
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing file or file type", response.json)

    def test_upload_user_file(self):
        """
        Test the upload_user_file method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")

        response = self.client.post(f'/user/uploadFile?username={self.hiwi_user_data['username']}&fileType=Signature',
                                    data={"file": self.file},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        self.client.delete(f'/user/deleteFile?username={self.hiwi_user_data['username']}&fileType=Signature',
                           headers={"Authorization": f"Bearer {access_token}"})

    def test_get_user_file_unauthorized(self):
        """
        Test the get_user_file method of the UserController class for archived user.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        hiwi_creation = self.user_service.create_user(self.hiwi_user_data)

        unauthorized_response = self.client.get(f'/user/getFile?username={self.hiwi_user_data['username']}&fileType'
                                                f'=Signature',
                                                headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(403, unauthorized_response.status_code)

    def test_get_user_file(self):
        """
        Test the get_user_file method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/uploadFile?username=AdminUserController&fileType=Signature',
                                    data={"file": self.file},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        user_file = self.client.get('/user/getFile?username=AdminUserController&fileType=Signature',
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertIsNotNone(user_file)

    def test_get_hiwis(self):
        """
        Test the get_hiwis method of the UserController class.
        """
        supervisor_creation = self.user_service.create_user(self.supervisor_user_data)
        hiwi_creation = self.user_service.create_user(self.hiwi_user_data)
        access_token = self._authenticate(self.supervisor_user_data['username'], "test_password")
        response = self.client.get('/user/getHiwis', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
        for hiwi in response.json:
            self.assertEqual(hiwi['role'], "Hiwi")

    def test_delete_user_file_archived_user(self):
        """
        Test the delete_user_file method of the UserController class for archived user.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        supervisor_creation = self.user_service.create_user(self.supervisor_user_data)
        hiwi_creation = self.user_service.create_user(self.hiwi_user_data)
        upload_response = self.client.post(f'/user/uploadFile?username={self.hiwi_user_data['username']}'
                                           f'&fileType=Signature', data={"file": self.file},
                                           headers={"Authorization": f"Bearer {access_token}"})
        self.user_service.archive_user(self.hiwi_user_data['username'])

        archived_response = self.client.delete(
            f'/user/deleteFile?username={self.hiwi_user_data['username']}&fileType'
            f'=Signature',
            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, archived_response.status_code)
        self.assertEqual("Cannot delete file of an archived user", archived_response.json)

    def test_delete_user_file(self):
        """
        Test the delete_user_file method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        response = self.client.post('/user/uploadFile?username=AdminUserController&fileType=Signature',
                                    data={"file": self.file},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        response = self.client.delete('/user/deleteFile?username=AdminUserController&fileType=Signature',
                                      headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        received_file = self.client.get('/user/getFile?username=AdminUserController&fileType=Signature',
                                        headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(received_file.status_code, 404)

    def test_get_supervisor_hiwi(self):
        """
        Test the get_supervisors method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        supervisor_creation = self.user_service.create_user(self.supervisor_user_data)
        hiwi_creation = self.user_service.create_user(self.hiwi_user_data)
        access_token = self._authenticate(self.hiwi_user_data['username'], "test_password")
        response = self.client.get('/user/getSupervisor', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['firstName'], self.supervisor_user_data['personalInfo']['firstName'])
        self.assertEqual(response.json['lastName'], self.supervisor_user_data['personalInfo']['lastName'])

        self.assertIsNotNone(response.json)

    def test_get_supervisors(self):
        """
        Test the get_supervisors method of the UserController class.
        """
        access_token = self._authenticate("AdminUserController", "test_password")
        supervisor_creation = self.user_service.create_user(self.supervisor_user_data)
        response = self.client.get('/user/getSupervisors', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
