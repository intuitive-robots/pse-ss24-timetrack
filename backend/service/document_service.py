from controller.strategy.pdf_generator_strategy import PDFGeneratorStrategy
from model.document_data import DocumentData
from model.request_result import RequestResult
from service.time_entry_service import TimeEntryService
from service.timesheet_service import TimesheetService
from service.user_service import UserService
from model.user.hiwi import Hiwi


class DocumentService:

    def __init__(self):
        self.pdf_generator_strategy = PDFGeneratorStrategy()
        self.user_service = UserService()
        self.time_entry_service = TimeEntryService()
        self.timesheet_service = TimesheetService()

    def generate_document(self, month: int, year: int, username: str):
        """
        Generates a document for the given month and year.
        :param month: The month for which to generate the document.
        :param year: The year for which to generate the document.
        :param username: The username of the user for which to generate the document.
        :return: The generated document.
        """

        document_data = self.gather_document_data(month, year, username)
        if document_data is None:
            return RequestResult(False, "Failed to gather document data.", status_code=400)
        return self.pdf_generator_strategy.generate_document(document_data)

    def gather_document_data(self, month: int, year: int, username: str) -> DocumentData | None:
        """
        Gathers the data required for generating a document.
        :param month: The month for which to gather the data.
        :param year: The year for which to gather the data.
        :param username: The username of the user for which to gather the data.
        :return: The document data.
        """
        user = self.user_service.get_profile(username)
        if not isinstance(user, Hiwi):
            return None
        result = self.timesheet_service.get_timesheet(username, month, year)
        if result.status_code != 200:
            return None
        timesheet = result.data
        time_entries = self.time_entry_service.get_entries_of_timesheet(timesheet.timesheet_id)
        return DocumentData(month, year, user.personal_info, user.contract_info, 0.0, time_entries)
