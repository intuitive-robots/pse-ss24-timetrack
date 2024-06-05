class PersonalInfo:
    """
    describes the personal information of a user.
    """
    def __init__(self, first_name: str, last_name: str, email: str, personal_number: str, institute_name: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.personal_number = personal_number
        self.institute_name = institute_name
        self.profile_picture = None

    def to_dict(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "personalNumber": self.personal_number,
            "instituteName": self.personal_number
        }
