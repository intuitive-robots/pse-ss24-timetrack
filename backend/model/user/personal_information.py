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

    @staticmethod
    def from_dict(data: dict):
        """
        Creates a PersonalInfo instance from a dictionary.

        :param dict data: A dictionary containing keys for first_name, last_name, email, personal_number, and institute_name.
        :return: A new instance of PersonalInfo.
        """
        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        email = data.get("email", "")
        personal_number = data.get("personalNumber", "")
        institute_name = data.get("instituteName", "")

        return PersonalInfo(first_name, last_name, email, personal_number, institute_name)

    def to_dict(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "personalNumber": self.personal_number,
            "instituteName": self.institute_name
        }

    @classmethod
    def dict_keys(cls):
        """ Returns a list of keys used for the dictionary representation of a PersonalInfo object. """
        dummy_personal = cls("", "", "", "", "")
        return list(dummy_personal.to_dict().keys())
