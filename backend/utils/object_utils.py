from bson import ObjectId


class ObjectUtils:
    @staticmethod
    def convert_objectids_to_strings(data):
        """
        Recursively converts all fields within a dictionary that are instances of bson.ObjectId to strings.

        :param data: The dictionary to convert.
        :return: The dictionary with all ObjectId fields converted to strings.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = ObjectUtils.convert_objectids_to_strings(value)
        elif isinstance(data, list):
            return [ObjectUtils.convert_objectids_to_strings(item) for item in data]
        elif isinstance(data, ObjectId):
            return str(data)
        return data
