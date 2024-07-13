from datetime import datetime

from controller.factory.user_factory import UserFactory
from controller.input_validator.user_data_validator import UserDataValidator
from controller.input_validator.validation_status import ValidationStatus
from model.repository.user_repository import UserRepository
from model.request_result import RequestResult
from model.user.role import UserRole
from model.user.supervisor import Supervisor
from model.user.user import User
from utils.security_utils import SecurityUtils


class UserService:
    """
    Provides service-layer functionality to handle user-related operations, such as creating,
    updating, retrieving, and deleting users. This service works with the UserRepository to
    interact with the model-data layer, ensuring users are managed according to defined business rules.
    """

    def __init__(self):
        """
        Initializes a new instance of the UserService class.

        This service is responsible for managing user data operations, interfacing
        with both the user repository for data storage and retrieval and possibly
        a user factory for creating user instances, as well as a validator for
        user data validation
        """
        self.user_repository = UserRepository.get_instance()
        self.user_validator = UserDataValidator()

    def _recursive_update(self, original: dict, updates: dict, exclude_keys=None) -> dict:
        """
        Recursively update a dictionary with another dictionary, excluding specified keys.

        :param original: The original dictionary to update.
        :param updates: The dictionary containing updates to apply.
        :param exclude_keys: A set or list of keys to exclude from the updates.
        :return: The updated dictionary.
        """
        #TODO: In Util Klasse auslagern

        if exclude_keys is None:
            exclude_keys = set()

        for key, value in updates.items():
            if key in exclude_keys:
                continue  # Skip updating this key if it's in the exclude list

            if isinstance(value, dict) and key in original:
                original[key] = self._recursive_update(original.get(key, {}), value, exclude_keys)
            elif key not in exclude_keys:
                original[key] = value
        return original

    def create_user(self, user_data) -> RequestResult:
        """
        Creates a new user in the system based on the provided user data.

        :param user_data: A dictionary containing user attributes necessary for creating a new user.
        :return: A RequestResult object containing the result of the create operation.
        """
        if 'password' not in user_data or user_data['password'] == "":  # plain password is required on creation
            return RequestResult(False, "Password is required", status_code=400)
        user_data['passwordHash'] = SecurityUtils.hash_password(user_data['password'])
        del user_data['password']  # Remove the plain text password from the data

        #TODO: AccountCreation and LastLogin are also required fields, which should not be the case.
        for key in User.dict_keys():
            if key not in user_data.keys() and key not in ['accountCreation', 'lastLogin']:
                return RequestResult(False, f"Missing required field: {key}", status_code=400)
        result = self.user_validator.is_valid(user_data)  # check if field format is valid
        if result.status == ValidationStatus.FAILURE:
            return RequestResult(False, result.message, status_code=400)
        user_factory = UserFactory.get_factory(user_data['role'])
        if not user_factory:
            return RequestResult(False, "Invalid user role specified", status_code=400)
        user = user_factory.create_user(user_data)

        if not user:
            return RequestResult(False, "User creation failed", status_code=500)
        if user.role == UserRole.HIWI:
            if 'supervisor' not in user_data:
                return RequestResult(False, "Supervisor is required for Hiwi creation", status_code=400)
            supervisor_data = self.user_repository.find_by_username(user_data['supervisor'])
            if not supervisor_data:
                return RequestResult(False, "Supervisor not found", status_code=404)
            if supervisor_data['role'] != 'Supervisor':
                return RequestResult(False, "Supervisor must be of role 'Supervisor'", status_code=400)
            supervisor_data['hiwis'].append(user_data['username'])
            result_user_creation = self.user_repository.create_user(user)
            if not result_user_creation.is_successful:
                return result_user_creation
            result_supervisor_update = self.user_repository.update_user(Supervisor.from_dict(supervisor_data))
            if not result_supervisor_update.is_successful:
                return result_supervisor_update
            return RequestResult(True, "HiWi created successfully", status_code=201)

        return self.user_repository.create_user(user)

    def _calculate_vacation_minutes(self, monthly_working_hours: int):
        """
        Calculates the number of vacation hours based on the monthly working hours.

        :param monthly_working_hours: The number of monthly working hours.
        :return: The number of vacation hours.
        """

        return round(((monthly_working_hours * 20 * 3.95) / (85 * 12) * 2), 0) / 2

    def add_overtime_minutes(self, username: str, minutes: int):
        """
        Adds overtime hours to a user identified by their username.

        :param username: The username of the user to add overtime hours to.
        :param minutes: The number of minutes to add to the user's overtime balance.
        :return: A RequestResult object containing the result of the operation.
        """
        user_data = self.user_repository.find_by_username(username)
        if not user_data:
            return RequestResult(False, "User not found", status_code=404)
        if 'contractInfo' not in user_data:
            return RequestResult(False, "User has no contract information", status_code=400)
        user_data['contractInfo']['overtimeMinutes'] += minutes
        user = UserFactory.create_user_if_factory_exists(user_data)
        return self.user_repository.update_user(user)

    def remove_overtime_minutes(self, username: str, minutes: int):
        """
        Removes overtime hours from a user identified by their username.

        :param username: The username of the user to remove overtime hours from.
        :param minutes: The number of minutes to remove from the user's overtime balance.
        :return: A RequestResult object containing the result of the operation.
        """
        user_data = self.user_repository.find_by_username(username)
        if not user_data:
            return RequestResult(False, "User not found", status_code=404)
        if 'contractInfo' not in user_data:
            return RequestResult(False, "User has no contract information", status_code=400)
        user_data['contractInfo']['overtimeMinutes'] -= minutes
        user = UserFactory.create_user_if_factory_exists(user_data)
        return self.user_repository.update_user(user)

    def add_vacation_minutes(self, username: str, minutes: int = None):
        """
        Adds vacation hours to a user identified by their username.

        :param username: The username of the user to add vacation hours to.
        :param minutes: The number of minutes to add to the user's vacation balance.
        :return: A RequestResult object containing the result of the operation.
        """
        user_data = self.user_repository.find_by_username(username)
        if not user_data:
            return RequestResult(False, "User not found", status_code=404)
        if 'contractInfo' not in user_data:
            return RequestResult(False, "User has no contract information", status_code=400)
        if minutes is not None:
            user_data['contractInfo']['vacationMinutes'] += minutes
        else:
            monthly_working_hours = user_data['contractInfo']['workingHours']
            monthly_vacation_hours = self._calculate_vacation_minutes(monthly_working_hours)
            user_data['contractInfo']['vacationMinutes'] += monthly_vacation_hours * 60
        user = UserFactory.create_user_if_factory_exists(user_data)
        return self.user_repository.update_user(user)

    def remove_vacation_minutes(self, username: str, minutes: int = None):
        """
        Removes vacation hours from a user identified by their username.

        :param username: The username of the user to remove vacation hours from.
        :param minutes: The number of minutes to remove from the user's vacation balance.
        :return: A RequestResult object containing the result of the operation.
        """
        user_data = self.user_repository.find_by_username(username)
        if not user_data:
            return RequestResult(False, "User not found", status_code=404)
        if 'contractInfo' not in user_data:
            return RequestResult(False, "User has no contract information", status_code=400)
        if minutes is not None:
            user_data['contractInfo']['vacationMinutes'] -= minutes
        else:
            monthly_working_hours = user_data['contractInfo']['workingHours']
            monthly_vacation_hours = self._calculate_vacation_minutes(monthly_working_hours)
            user_data['contractInfo']['vacationMinutes'] -= monthly_vacation_hours
        user = UserFactory.create_user_if_factory_exists(user_data)
        return self.user_repository.update_user(user)

    def update_user(self, user_data: dict):
        """
        Updates an existing user in the system with the provided user data.

        :param user_data: A dictionary with user attributes that should be updated.
        :return: RequestResult object containing the result of the update operation.
        """
        if 'username' not in user_data:
            return RequestResult(False, "Username must be provided for user update", status_code=400)
        existing_user_data = self.user_repository.find_by_username(user_data['username'])
        existing_supervisor = existing_user_data.get('supervisor', None)
        if not existing_user_data:
            return RequestResult(False, "User not found", status_code=404)
        updated_user_data = self._recursive_update(existing_user_data, user_data, ['username', 'role', "passwordHash"])

        # Validate the updated user data
        validation_result = self.user_validator.is_valid(updated_user_data)
        if validation_result.status == ValidationStatus.FAILURE:
            return RequestResult(False, validation_result.message, status_code=400)
        # Create a user object using the factory
        updated_user = UserFactory.get_factory(updated_user_data['role']).create_user(updated_user_data)
        if not updated_user:
            return RequestResult(False, "Failed to create user object with updated data", status_code=400)
        if updated_user.role == UserRole.HIWI.value and user_data['supervisor'] != existing_supervisor:
            update_supervisor_result = self._update_supervisor(user_data['username'], existing_supervisor,
                                                               user_data['supervisor'])
            if not update_supervisor_result.is_successful:
                return update_supervisor_result
        return self.user_repository.update_user(updated_user)

    def _update_supervisor(self, hiwi_username: str, supervisor_username: str, new_supervisor_username: str):
        """
        Updates the supervisor of a Hiwi.

        :param hiwi_username: The username of the Hiwi.
        :param supervisor_username: The username of the current supervisor.
        :param new_supervisor_username: The username of the new supervisor.
        :return: A RequestResult object containing the result of the operation.
        """
        hiwi_data = self.user_repository.find_by_username(hiwi_username)
        if not hiwi_data:
            return RequestResult(False, "Hiwi not found", status_code=404)
        if hiwi_data['role'] != 'Hiwi':
            return RequestResult(False, "User is not a Hiwi", status_code=400)
        supervisor_data = self.user_repository.find_by_username(supervisor_username)
        if not supervisor_data:
            return RequestResult(False, "Supervisor not found", status_code=404)
        if supervisor_data['role'] != 'Supervisor':
            return RequestResult(False, "User is not a Supervisor", status_code=400)
        new_supervisor_data = self.user_repository.find_by_username(new_supervisor_username)
        if not new_supervisor_data:
            return RequestResult(False, "New supervisor not found", status_code=404)
        if new_supervisor_data['role'] != 'Supervisor':
            return RequestResult(False, "User is not a Supervisor", status_code=400)
        supervisor_data['hiwis'].remove(hiwi_username)
        result_supervisor_update = self.user_repository.update_user(Supervisor.from_dict(supervisor_data))
        if not result_supervisor_update.is_successful:
            return result_supervisor_update
        new_supervisor_data['hiwis'].append(hiwi_username)
        return self.user_repository.update_user(Supervisor.from_dict(new_supervisor_data))

    def delete_user(self, username: str):
        """
        Deletes a user from the system identified by their username.

        :param username: The username of the user to be deleted.
        :return: A RequestResult object containing the result of the delete operation.
        """
        user_data = self.user_repository.find_by_username(username)
        if not user_data:
            return RequestResult(False, "User not found", status_code=404)
        if user_data['role'] == 'Hiwi':
            supervisor_data = self.user_repository.find_by_username(user_data["supervisor"])
            supervisor_data['hiwis'].remove(user_data['username'])
            result_supervisor_update = self.user_repository.update_user(Supervisor.from_dict(supervisor_data))
            if not result_supervisor_update.is_successful:
                return result_supervisor_update
        return self.user_repository.delete_user(username)

    def get_users(self) -> list[User]:
        """
        Retrieves a list of all users in the system.

        :return: A list of User model instances representing all users in the system.
        :rtype: list[User]
        """
        users_data = self.user_repository.get_users()
        users = list(filter(None, map(UserFactory.create_user_if_factory_exists, users_data)))

        return users

    def get_users_by_role(self, role: str) -> list[User]:
        """
        Retrieves a list of users in the system filtered by a specific role.

        :param str role: The role to filter users by.
        :return: A list of User model instances that match the specified role.
        :rtype: list[User]
        """
        parsedRole = UserRole.get_role_by_value(role)
        if not parsedRole:
            return []
        users_data = self.user_repository.get_users_by_role(parsedRole)
        users = list(filter(None, map(UserFactory.create_user_if_factory_exists, users_data)))

        return RequestResult(True, "", status_code=200, data=users)

    def get_profile(self, username: str) -> User:
        """
        Retrieves the profile of a specific user identified by their username.

        :param str username: The username of the user whose profile is being requested.
        :return: A User model instance representing the user's profile.
        :rtype: User
        """
        user_data = self.user_repository.find_by_username(username)
        return UserFactory.create_user_if_factory_exists(user_data)

    def get_hiwis(self, username: str):
        """
        Retrieves a list of Hiwis managed by a Supervisor identified by their username.

        :param str username: The username of the Supervisor whose Hiwis are being requested.
        :return: A list of Hiwi model instances representing the Supervisor's Hiwis.
        :rtype: list[Hiwi]
        """
        supervisor_data = self.user_repository.find_by_username(username)
        if not supervisor_data:
            return RequestResult(False, "Supervisor not found", status_code=404)
        if supervisor_data['role'] != 'Supervisor':
            return RequestResult(False, "User is not a Supervisor", status_code=400)
        for hiwi_username in supervisor_data['hiwis']:
            print(self.get_profile(hiwi_username))

        hiwis_data = list(self.get_profile(hiwi_username) for hiwi_username in supervisor_data['hiwis'])
        if not hiwis_data:
            return RequestResult(False, "No Hiwis found", status_code=404)
        return RequestResult(True, "", status_code=200, data=hiwis_data)

    def get_supervisor(self, username: str, only_name: bool = False):
        """
        Retrieves information about the supervisor of a Hiwi.

        Returns: A RequestResult object containing the result of the operation.
        """
        hiwi_data = self.user_repository.find_by_username(username)
        if not hiwi_data:
            return RequestResult(False, "Hiwi not found", status_code=404)
        if hiwi_data['role'] != 'Hiwi':
            return RequestResult(False, "User is not a Hiwi", status_code=400)
        supervisor_data = self.user_repository.find_by_username(hiwi_data['supervisor'])
        if not supervisor_data:
            return RequestResult(False, "Supervisor not found", status_code=404)
        if only_name:
            relevant_supervisor_data = {'firstName': supervisor_data['personalInfo']['firstName'],
                                        'lastName': supervisor_data['personalInfo']['lastName']}
            return RequestResult(True, "", status_code=200, data=relevant_supervisor_data)
        relevant_supervisor_data = supervisor_data['personalInfo']
        relevant_supervisor_data.pop('personalNumber', None)
        relevant_supervisor_data['role'] = supervisor_data['role']
        return RequestResult(True, "", status_code=200, data=relevant_supervisor_data)

    def get_supervisors(self):
        """
        Retrieves a list of all Supervisors in the system.


        :return: A list of Supervisor model instances representing all Supervisors in the system.
        :rtype: list[Supervisor]
        """
        supervisors_data = self.user_repository.get_users_by_role(UserRole.SUPERVISOR)
        supervisors = list(filter(None, map(UserFactory.create_user_if_factory_exists, supervisors_data)))
        if not supervisors:
            return RequestResult(False, "No Supervisors found", status_code=404)
        sorted_supervisors = sorted(supervisors, key=lambda x: x.personal_info.last_name)
        return RequestResult(True, "", status_code=200, data=sorted_supervisors)
