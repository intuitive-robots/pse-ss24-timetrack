import unittest

from controller.factory.secretary_factory import SecretaryFactory
from model.user.role import UserRole
from utils.security_utils import SecurityUtils


class TestSecretaryFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.secretary_factory = SecretaryFactory()

    def setUp(self):
        self.secretary_data = {
            "username":"testSecretary",
            "passwordHash": SecurityUtils.hash_password("test_password"),
            "role": "Secretary",
            "personalInfo": {
                "firstName": "Test",
                "lastName": "Secretary",
                "email": "test@gmail.com",
                "personalNumber": "6381212",
                "instituteName": "Info Institute"
            },
            "accountCreation": None,
            "lastLogin": None,
            "isArchived": False
        }

    def test_create_secretary(self):
        """
        Test that a Secretary object is created correctly
        """
        user = self.secretary_factory.create_user(self.secretary_data)
        self.assertEqual(user.username, "testSecretary")
        self.assertEqual(user.role, UserRole.SECRETARY)

