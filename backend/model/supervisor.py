from model.personalInformation import PersonalInfo
from model.role import UserRole
from model.user import User


class Supervisor(User):
    def __init__(self, username: str, passwordHash: str, personalInfo: PersonalInfo, hiwis=None):
        """
        Initializes a new instance of the Supervisor class, which extends the User class.

        :param username: The username for the Supervisor account.
        :param passwordHash: The hash of the user's password.
        :param personalInfo: An instance of PersonalInfo containing the Supervisor's personal information.
        :param hiwis: A list of Hiwi objects that the Supervisor manages. Defaults to an empty list if none is provided.
        """
        super().__init__(username, passwordHash, personalInfo, UserRole.SUPERVISOR)
        self.hiwis = hiwis if hiwis is not None else []
        self.signature_image = None

    def addHiwi(self, hiwi):
        """
        Adds a Hiwi to the Supervisor's list of Hiwis.

        :param hiwi: The Hiwi to be added to the list.
        """
        self.hiwis.append(hiwi)

    def removeHiwi(self, hiwi):
        """
        Removes a Hiwi from the Supervisor's list of Hiwis.

        :param hiwi: The Hiwi to be removed from the list.
        """
        self.hiwis.remove(hiwi)

    def toDict(self):
        """
        Converts the Supervisor object to a dictionary.

        :return: A dictionary containing all the current attributes of the Supervisor object.
        """
        user_dict = super().toDict()
        user_dict.update({
            "hiwis": [hiwi.toDict() for hiwi in self.hiwis],
        })
        return user_dict
