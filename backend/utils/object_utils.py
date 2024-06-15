from bson import ObjectId


class ObjectUtils:
    """
    Utility class providing methods for handling and converting BSON ObjectId instances
    within data structures.
    """

    @staticmethod
    def convert_objectids_to_strings(data):
        """
        Recursively converts all fields within a dictionary or list that are instances of bson.ObjectId to strings.

        This method is particularly useful for preparing data for JSON serialization,
        where ObjectId instances need to be converted to string format.

        :param data: The data structure to convert. It can be a dictionary, list, or a single ObjectId instance.
        :type data: dict, list, or ObjectId
        :return: The data structure with all ObjectId fields converted to strings.
        :rtype: dict, list, or str
        """
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = ObjectUtils.convert_objectids_to_strings(value)
        elif isinstance(data, list):
            return [ObjectUtils.convert_objectids_to_strings(item) for item in data]
        elif isinstance(data, ObjectId):
            return str(data)
        return data
