from abc import ABC, abstractmethod

from model.document_data import DocumentData


class DocumentGeneratorStrategy(ABC):

    @abstractmethod
    def generate_document(self, data: DocumentData):
        """
        Generates a document based on the given data.
        :param data: The data to use for generating the document.
        :return: The generated document.
        """
        pass

    def generate_multiple_documents(self, data: list[DocumentData]):
        """
        Generates multiple documents based on the given list of data.
        :param data: The list of data to use for generating the documents.
        :return: The list of generated documents.
        """
        pass