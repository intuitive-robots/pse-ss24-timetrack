import bcrypt


class SecurityUtils:
    """
    SecurityUtils provides static methods for common security operations
    such as password hashing and password verification using bcrypt.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using bcrypt.

        :param password: The password to hash
        :return: The hashed password
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """
        Checks if a password matches a hashed password.

        :param password: The password to check
        :param hashed_password: The hashed password to compare against
        :return: True if the password matches the hashed password, False otherwise
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
