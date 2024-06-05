class PersonalInfo:
    """
    describes the personal information of a user.
    """
    def __init__(self, firstName: str, lastName: str, email: str, personalNumber: str, instituteName: str):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.personalNumber = personalNumber
        self.instituteName = instituteName
        self.profilePicture = None

    def toDict(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "personalNumber": self.personalNumber,
            "instituteName": self.personalNumber
        }
