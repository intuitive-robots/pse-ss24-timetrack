class PersonalInfo:
    """
    describes the personal information of a user.
    """
    def __init__(self, first_name: str, last_name: str, email: str, personal_number: str, instituteName: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.personal_number = personal_number
        self.instituteName = instituteName
        self.profilePicture = None

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "personal_number": self.personal_number,
            "institute_name": self.personal_number
        }
