import unittest

from app import app
from model.repository.user_repository import UserRepository
from model.user.user import User
from service.user_service import UserService


class TestUserController(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user_repository = UserRepository.get_instance()
        self.user_service = UserService()

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

    def test_login(self):
        """
        Test the login method of the UserController class.
        """
        user = {
            "username": "testAdmin1",
            "password": "test_password"
        }
        fake_user = {
            "username": "wroaif",
            "password": "test_password"
        }

        # Test for no json
        no_json_response = self.client.post('/user/login')
        self.assertEqual(400, no_json_response.status_code)
        self.assertEqual('Request data must be in JSON format', no_json_response.json)

        # Test for wrong username
        wrong_username_response = self.client.post('/user/login', json=fake_user)
        self.assertEqual(401, wrong_username_response.status_code)

        response = self.client.post('/user/login', json=user)

        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        """
        Test the create_user method of the UserController class.
        """
        user = {
            "username": "testAdmin10",
            "password": "test_password",
            "role": "Admin",
            "personalInfo": {
                "firstName": "Nico",
                "lastName": "Admin",
                "email": "test@gmail.com",
                "personalNumber": "6981211",
                "instituteName": "Info Institute"
            }
        }
        access_token = self.authenticate("testAdmin1", "test_password")



        response = self.client.post('/user/createUser', json=user, headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(201, response.status_code)
        user_data = self.user_repository.find_by_username("testAdmin10")
        self.assertIsNotNone(user_data)
        self.user_repository.delete_user("testAdmin10")

        # Test for no json
        no_json_response = self.client.post('/user/createUser',
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_response.status_code)
        self.assertEqual('Request data must be in JSON format', no_json_response.json)
    def test_update_user(self):
        """
        Test the update_user method of the UserController class.
        """
        update_data = {
            "username": "testAdmin1",
            "personalInfo": {
                "firstName": "Nico",
                "lastName": "Admin",
                "email": "usedInTest@gmail.com",
                "personalNumber": "6981211",
                "instituteName": "Info Institute"
            }
        }
        access_token = self.authenticate("testAdmin1", "test_password")

        # Test for no json
        no_json_response = self.client.post('/user/updateUser',
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_response.status_code)
        self.assertEqual('Request data must be in JSON format', no_json_response.json)

        response = self.client.post('/user/updateUser', json=update_data,
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        user_data = self.user_repository.find_by_username("testAdmin1")
        self.assertEqual(user_data['personalInfo']['email'], "usedInTest@gmail.com")
        user_data['personalInfo']['email'] = "test@gmail.com"
        self.user_repository.update_user(User.from_dict(user_data))

    def test_delete_user(self):
        """
        Test the delete_user method of the UserController class.
        """
        user_data = {
            "username": "testAdmin10",
            "password": "test_password",
            "role": "Admin",
            "personalInfo": {
                "firstName": "Nico",
                "lastName": "Admin",
                "email": "test@gmail.com",
                "personalNumber": "6981211",
                "instituteName": "Info Institute"
            }
        }

        self.user_service.create_user(user_data)
        access_token = self.authenticate("testAdmin1", "test_password")

        # Test for no json
        no_json_response = self.client.delete('/user/deleteUser',
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_response.status_code)
        self.assertEqual('Request data must be in JSON format', no_json_response.json)

        response = self.client.delete('/user/deleteUser', json={"username": "testAdmin10"},
                                      headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        user_data = self.user_repository.find_by_username("testAdmin10")
        self.assertIsNone(user_data)

    def test_archive_user(self):
        """
        Test the archive_user method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")

        # Test for no json
        no_json_response = self.client.post('/user/archiveUser',
                                              headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_response.status_code)
        self.assertEqual('Request data must be in JSON format', no_json_response.json)

        self.user_service.unarchive_user("testArchivedUser")
        response = self.client.post('/user/archiveUser', json={"username": "testArchivedUser"},
                                              headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.user_service.is_archived("testArchivedUser"))
        self.user_service.archive_user("testArchivedUser")

    def test_unarchive_user(self):
        """
        Test the unarchive_user method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")

        # Test for no json
        no_json_response = self.client.post('/user/unarchiveUser',
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_response.status_code)
        self.assertEqual('Request data must be in JSON format', no_json_response.json)

        response = self.client.post('/user/unarchiveUser', json={"username": "testArchivedUser"},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertFalse(self.user_service.is_archived("testArchivedUser"))
        self.user_service.archive_user("testArchivedUser")

    def test_logout(self):
        """
        Test the logout method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")
        response = self.client.post('/user/logout', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        #TODO: Check if session is destroyed

    def test_reset_password(self):
        """
        Test the reset_password method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")
        user_data = self.user_repository.find_by_username("testAdmin1")
        old_password_hash = user_data['passwordHash']

        # Test for no json
        no_json_response = self.client.post('/user/resetPassword',
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_response.status_code)
        self.assertEqual('Request data must be in JSON format', no_json_response.json)

        # Test for archived user
        archive_response = self.client.post('/user/resetPassword', json={"username": "testArchivedUser", "password": "test"},
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, archive_response.status_code)
        self.assertEqual('Password of archived user cannot be reset', archive_response.json)

        response = self.client.post('/user/resetPassword', json={"username": "testAdmin1", "password": "test"},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        user_data = self.user_repository.find_by_username("testAdmin1")
        new_password_hash = user_data['passwordHash']
        self.assertNotEqual(old_password_hash, new_password_hash)
        access_token = self.authenticate("testAdmin1", "test")
        self.assertIsNotNone(access_token)
        self.client.post('/user/resetPassword', json={"username": "testAdmin1", "password": "test_password"},
                         headers={"Authorization": f"Bearer {access_token}"})

    def test_get_profile(self):
        """
        Test the get_profile method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")
        response = self.client.get('/user/getProfile', headers={"Authorization": f"Bearer {access_token}"})
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], "testAdmin1")

    def test_get_contract_info(self):
        """
        Test the get_contract_info method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")
        # Test for no json
        no_json_response = self.client.get('/user/getContractInfo',
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_json_response.status_code)

        response = self.client.get('/user/getContractInfo?username=testHiwi1',
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(12.4, response.json['hourlyWage'])

    def test_get_users(self):
        """
        Test the get_users method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")
        response = self.client.get('/user/getUsers', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    def test_get_archived_users(self):
        """
        Test the get_archived_users method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")

        response = self.client.get('/user/getArchivedUsers', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        archived_users = [user['username'] for user in response.json]
        self.assertTrue("testArchivedUser" in archived_users)

    def test_get_users_by_role_admin(self):
        """
        Test the get_users_by_role method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")

        # Test for no role
        no_role_response = self.client.get('/user/getUsersByRole',
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_role_response.status_code)
        self.assertEqual('Role parameter is required', no_role_response.json)

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
        access_token = self.authenticate("testAdmin1", "test_password")
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
        access_token = self.authenticate("testAdmin1", "test_password")
        response = self.client.get('/user/getUsersByRole?role=Supervisor',
                                   headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
        for supervisor in response.json:
            self.assertEqual(supervisor['role'], "Supervisor")

    def test_upload_user_file(self):
        """
        Test the upload_user_file method of the UserController class.
        """
        access_token = self.authenticate("testHiwi1", "test_password")
        file = open("../resources/testProfilePic.jpg", "rb")

        # Test for no file
        no_file_response = self.client.post('/user/uploadFile?username=testHiwi1&fileType=Signature',
                                            headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, no_file_response.status_code)
        self.assertEqual("Missing file or file type", no_file_response.json)

        response = self.client.post('/user/uploadFile?username=testHiwi1&fileType=Signature', data={"file": file},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        file.close()
        self.client.delete('/user/deleteFile?username=testHiwi1&fileType=Signature',
                           headers={"Authorization": f"Bearer {access_token}"})

    def test_get_user_file(self):
        """
        Test the get_user_file method of the UserController class.
        """
        access_token = self.authenticate("testHiwi1", "test_password")
        file = open("../resources/testProfilePic.jpg", "rb")

        # Test for archived user
        archived_response = self.client.get('/user/getFile?username=testArchivedUser&fileType=Signature',
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, archived_response.status_code)

        response = self.client.post('/user/uploadFile?username=testHiwi1&fileType=Signature', data={"file": file},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        user_file = self.client.get('/user/getFile?username=testHiwi1&fileType=Signature',
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertIsNotNone(user_file)
        file.close()
        self.client.delete('/user/deleteFile?username=testHiwi1&fileType=Signature',
                           headers={"Authorization": f"Bearer {access_token}"})

    def test_get_hiwis(self):
        """
        Test the get_hiwis method of the UserController class.
        """
        access_token = self.authenticate("testSupervisor1", "test_password")
        response = self.client.get('/user/getHiwis', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)
        for hiwi in response.json:
            self.assertEqual(hiwi['role'], "Hiwi")

    def test_delete_user_file(self):
        """
        Test the delete_user_file method of the UserController class.
        """
        access_token = self.authenticate("testHiwi1", "test_password")
        file = open("../resources/testProfilePic.jpg", "rb")
        # Test for archived user
        archived_response = self.client.delete('/user/deleteFile?username=testArchivedUser&fileType=Signature',
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(400, archived_response.status_code)

        response = self.client.post('/user/uploadFile?username=testHiwi1&fileType=Signature', data={"file": file},
                                    headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 201)
        response = self.client.delete('/user/deleteFile?username=testHiwi1&fileType=Signature',
                                      headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        received_file = self.client.get('/user/getFile?username=testHiwi1&fileType=Signature', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(received_file.status_code, 404)

    def test_get_supervisor_hiwi(self):
        """
        Test the get_supervisors method of the UserController class.
        """
        access_token = self.authenticate("testHiwi1", "test_password")
        response = self.client.get('/user/getSupervisor', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json)

    def test_get_supervisors(self):
        """
        Test the get_supervisors method of the UserController class.
        """
        access_token = self.authenticate("testAdmin1", "test_password")
        response = self.client.get('/user/getSupervisors', headers={"Authorization": f"Bearer {access_token}"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

