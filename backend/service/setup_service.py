import time
import random
from db import initialize_db
from model.user.role import UserRole
from model.repository.user_repository import UserRepository
from service.user_service import UserService


class SetupService:
    """
    A service class that ensures the proper setup of the application,
    including the existence of an admin user and the initialization of the
    administration collection in the database.
    """

    ADMIN_COLLECTION = "administration"

    def __init__(self):
        """
        Initializes the SetupService class.
        """
        self.user_service = UserService()
        self.user_repository = UserRepository.get_instance()
        self.db = initialize_db()

    def ensure_admin_exists(self) -> bool:
        """
        Checks if an admin user exists in the database. If no admin is found,
        it creates a default admin user.

        :return: bool - True if an admin already existed, False if a new admin was created.
        """
        admins = self.user_repository.get_users_by_role(UserRole.ADMIN)
        if not admins:
            print("No admin user found, creating default admin...")
            self.create_default_admin()
            return False
        return True

    def create_default_admin(self):
        """
        Creates a default admin user with predefined credentials and details
        if no admin user exists in the system.
        """
        admin_data = {
            "username": "irladmin",
            "password": "irl123",
            "personalInfo": {
                "firstName": "IRL",
                "lastName": "Admin",
                "email": "admin@example.com",
                "personalNumber": "000001",
                "instituteName": "Intuitive Robots Lab"
            },
            "role": UserRole.ADMIN.value,
            "slackId": ""
        }
        result = self.user_service.create_user(admin_data)
        if not result.is_successful:
            print(f"Failed to create default admin user: {result.message}")
            return
        print(f"\033[32mDefault admin user {admin_data.get('username', '')} was initialized successfully.\033[0m")

    def ensure_slack_token_exists(self) -> bool:
        """
        Checks if a SlackToken entry exists in the administration collection.
        If no such entry exists, it creates a default entry with an empty string as the token.

        :return: True if a SlackToken already existed, False if a new SlackToken was created.
        """
        admin_collection = self.db[self.ADMIN_COLLECTION]
        slack_token_entry = admin_collection.find_one({}, {"_id": 0, "slackToken": 1})
        if not slack_token_entry:
            print("No SlackToken found, creating default entry...")
            self.create_default_slack_token()
            return False
        return True

    def initialize_admin_collection(self) -> bool:
        """
        Ensures that the administration collection exists in the database.
        If the collection does not exist, it creates the collection and checks
        for the existence of a SlackToken entry.

        :return: True if the administration collection already existed and was fully initialized,
                    False if any part of the collection or its contents were newly created.
        """
        collection_existed = True
        if self.ADMIN_COLLECTION not in self.db.list_collection_names():
            print(f"Initialize '{self.ADMIN_COLLECTION}' collection...")
            self.db.create_collection(self.ADMIN_COLLECTION)
            collection_existed = False

        slack_token_existed = self.ensure_slack_token_exists()
        return collection_existed and slack_token_existed

    def check_slack_token(self):
        """
        Checks if the SlackToken in the administration collection is empty.
        If the SlackToken is not set, it logs a message to the console.
        """
        admin_collection = self.db[self.ADMIN_COLLECTION]
        slack_token_entry = admin_collection.find_one({}, {"_id": 0, "slackToken": 1})
        if slack_token_entry and slack_token_entry.get("slackToken") == "":
            print(
                "\033[33mSlack Token is not set. Please change the token within the administration section in the database.\033[0m")

    def create_default_slack_token(self):
        """
        Creates a default SlackToken entry in the administration collection
        with an empty string as the token value.
        """
        admin_collection = self.db[self.ADMIN_COLLECTION]
        admin_collection.insert_one({"slackToken": ""})
        print("\033[32mDefault SlackToken entry created.\033[0m")

    def run_setup(self):
        """
        Executes the setup process by ensuring the existence of an admin user
        and initializing the administration collection in the database.
        If everything is already correctly set up, it prints a message indicating so.
        """
        random_delay = random.uniform(0.1, 2.0)
        print(f"Waiting for {random_delay:.2f} seconds to avoid race conditions.")
        time.sleep(random_delay)

        admin_exists = self.ensure_admin_exists()
        admin_collection_initialized = self.initialize_admin_collection()

        if admin_exists and admin_collection_initialized:
            print("\033[32mClockwise is initialized and ready to use.\033[0m")
        else:
            print("\033[32mSetup process completed with necessary adjustments.\033[0m")

        self.check_slack_token()
