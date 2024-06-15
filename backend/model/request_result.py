class RequestResult:
    """
    Represents the outcome of a request or operation, encapsulating whether it was successful,
    along with an associated message, status code, and optional additional data.

    This class is typically used to standardize the format of responses across various parts
    of an application, particularly in APIs or service layers where consistent response formats are beneficial.

    Attributes:
        is_successful (bool): Indicates whether the request was successful.
        message (str): A descriptive message associated with the result of the request.
        status_code (int): The HTTP-like status code that summarizes the outcome of the request.
        data (dict, optional): Additional data related to the request result.
    """

    def __init__(self, is_successful, message, status_code, data=None):
        """
        Initializes a new instance of RequestResult with specified values.

        :param is_successful: A boolean indicating if the request was successful. True means success, False indicates failure.
        :type is_successful: bool
        :param message: The message associated with the result of the request, explaining the outcome.
        :type message: str
        :param status_code: The status code summarizing the outcome of the request, similar to HTTP status codes.
        :type status_code: int
        :param data: Optional additional data related to the request result; can be used to pass further information.
        :type data: dict, optional
        """
        self.data = data
        self.is_successful = is_successful
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """
        Converts the RequestResult instance into a dictionary format, which is particularly useful
        for serialization, especially when sending responses from a web API.

        :return: A dictionary containing keys for success status, message, and optionally additional data.
        :rtype: dict

        Example:
            - If instantiated with success=True, message="Operation completed", and no data, the dictionary will be:
              `{'isSuccessful': True, 'message': 'Operation completed'}`
            - If there is additional data provided, it will appear in the dictionary as well.
        """
        result = {
            "isSuccessful": self.is_successful,
            "message": self.message,
            "statusCode": self.status_code
        }
        if self.data:
            result['data'] = self.data
        return result


