from model.personal_information import PersonalInfo
from model.role import UserRole
from model.user import User


class Supervisor(User):
    def __init__(self, username: str, password_hash: str, personal_info: PersonalInfo, hiwis=None):
        """
        Initializes a new instance of the Supervisor class, which extends the User class.

        :param username: The username for the Supervisor account.
        :param password_hash: The hash of the user's password.
        :param personal_info: An instance of PersonalInfo containing the Supervisor's personal information.
        :param hiwis: A list of Hiwi objects that the Supervisor manages. Defaults to an empty list if none is provided.
        """
        super().__init__(username, password_hash, personal_info, UserRole.SUPERVISOR)
        self.hiwis = hiwis if hiwis is not None else []
        self.signature_image = None

    def add_hiwi(self, hiwi):
        """
        Adds a Hiwi to the Supervisor's list of Hiwis.

        :param hiwi: The Hiwi to be added to the list.
        """
        self.hiwis.append(hiwi)

    def remove_hiwi(self, hiwi):
        """
        Removes a Hiwi from the Supervisor's list of Hiwis.

        :param hiwi: The Hiwi to be removed from the list.
        """
        self.hiwis.remove(hiwi)

    def to_dict(self):
        """
        Converts the Supervisor object to a dictionary.

        :return: A dictionary containing all the current attributes of the Supervisor object.
        """
        user_dict = super().to_dict()
        user_dict.update({
            "hiwis": [hiwi.to_dict() for hiwi in self.hiwis],
        })
        return user_dict
