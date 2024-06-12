class RequestResult:

    def __init__(self, is_successful, message, status_code, data=None):
        """
        Initializes a new RequestResult object with the given parameters.
        :param is_successful: A boolean indicating if the request was successful.
        :param message: The message to be returned with the request result.
        :param status_code: The status code of the request.
        """
        self.data = data
        self.is_successful = is_successful
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """
        Converts the RequestResult object to a dictionary format.
        :return: A dictionary representing the request result.
        """
        return {
            "isSuccessful": self.is_successful,
            "message": self.message
        }


