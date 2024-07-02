import bcrypt


class SecurityUtils:
    """
    Provides static methods for common security operations such as password
    hashing and password verification using bcrypt.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using bcrypt.

        This method takes a plain text password and returns its hashed version using bcrypt,
        which is a password hashing function designed to be computationally expensive to resist brute-force attacks.

        :param str password: The plain text password to hash.
        :return: The hashed password.
        :rtype: str
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """
        Checks if a plain text password matches a hashed password.

        This method verifies whether the provided plain text password, when hashed,
        matches the given hashed password. This is useful for authentication purposes.

        :param str password: The plain text password to check.
        :param str hashed_password: The hashed password to compare against.
        :return: True if the password matches the hashed password, False otherwise.
        :rtype: bool
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
