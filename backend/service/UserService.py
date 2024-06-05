
class UserService:

    def __init__(self):
        self.user_repository = None

    def create_user(self, user_date: dict):
        return self.user_repository.create_user(user_date)