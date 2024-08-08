from model.user.personal_information import PersonalInfo
from model.user.role import UserRole
from model.user.user import User


class Supervisor(User):
    def __init__(self, username: str, password_hash: str,
                 personal_info: PersonalInfo, hiwis=None, currentTimesheetIds=None, is_archived=False, slack_id: str = None):
        """
        Initializes a new instance of the Supervisor class, which extends the User class.

        :param username: The username for the Supervisor account.
        :param password_hash: The hash of the user's password.
        :param personal_info: An instance of PersonalInfo containing the Supervisor's personal information.
        :param hiwis: A list of Hiwi objects that the Supervisor manages. Defaults to an empty list if none is provided.
        """
        super().__init__(username, password_hash, personal_info, UserRole.SUPERVISOR, is_archived=is_archived, slack_id=slack_id)

        self.currentTimesheetIds = currentTimesheetIds if currentTimesheetIds is not None else []
        self.hiwis = hiwis if hiwis is not None else []
        self.signature_image = None

    def add_hiwi(self, hiwi: str):
        """
        Adds a Hiwi to the Supervisor's list of Hiwis.

        :param hiwi: The Hiwi to be added to the list.
        """
        self.hiwis.append(hiwi)

    def remove_hiwi(self, hiwi: str):
        """
        Removes a Hiwi from the Supervisor's list of Hiwis.

        :param hiwi: The Hiwi to be removed from the list.
        """
        self.hiwis.remove(hiwi)

    @classmethod
    def from_dict(cls, supervisor_data: dict):
        """
        Creates a Supervisor object from a dictionary.
        """

        #TODO: Missing: CurrentTimesheetIds
        supervisor = cls(
            username=supervisor_data["username"],
            password_hash=supervisor_data["passwordHash"],
            personal_info=PersonalInfo.from_dict(supervisor_data["personalInfo"]),
            hiwis=supervisor_data["hiwis"]
        )
        return supervisor

    def to_dict(self):
        """
        Converts the Supervisor object to a dictionary.

        :return: A dictionary containing all the current attributes of the Supervisor object.
        """
        user_dict = super().to_dict()
        user_dict.update({
            "hiwis": [hiwi for hiwi in self.hiwis],
        })
        return user_dict

    def to_name_dict(self):
        """
        Converts the Supervisor object to a dictionary with only the name and id.

        :return: A dictionary containing the name and id of the Supervisor object.
        """
        personal_info = self.personal_info
        return {
            "username": self.username,
            "firstName": personal_info.first_name,
            "lastName": personal_info.last_name,
        }
