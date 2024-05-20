from datetime import datetime
from db import mongo
from model.personal_information import PersonalInfo
from model.role import UserRole


class User:
    def __init__(self, username: str, password_hash: str, personal_info: PersonalInfo, role: str):
        self.username = username
        self.password_hash = password_hash
        self.personal_info = personal_info
        self.role = UserRole[role]
        self.account_creation = None
        self.last_login = None

    def save(self):
        user_data = {
            "username": self.username,
            "password_hash": self.password_hash,
            "personal_info": self.personal_info.to_dict(),
            "employment_details": {
                "role": self.role,
            },
            "account_creation": self.account_creation,
            "last_login": self.last_login
        }
        return mongo.db.users.insert_one(user_data)

    @classmethod
    def find_by_username(cls, username):
        user = mongo.db.users.find_one({"username": username})
        if user:
            return cls(
                username=user['username'],
                password_hash=user['password_hash'],
                personal_info=PersonalInfo(user['personal_info']['first_name'], user['personal_info']['last_name'],
                                           user['personal_info']['email'], user['personal_info']['personal_number']),
                role=user['employment_details']['role'],
            )
        return None

    def is_admin(self):
        """ checks if user is an admin """
        return self.role == UserRole.ADMIN
