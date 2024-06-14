from abc import ABC, abstractmethod


class DocumentGeneratorStrategy(ABC):

    @abstractmethod
    def generate_document(self, data: dict):
        """
        Generates a document based on the given data.
        :param data: The data to use for generating the document.
        :return: The generated document.
        """
        pass

    def generate_multiple_documents(self, data: list):
        """
        Generates multiple documents based on the given list of data.
        :param data: The list of data to use for generating the documents.
        :return: The list of generated documents.
        """
        pass