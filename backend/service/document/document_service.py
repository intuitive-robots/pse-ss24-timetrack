import os
from datetime import datetime
from glob import glob
from io import BytesIO
from zipfile import ZipFile

from model.timesheet_status import TimesheetStatus
from service.document.pdf_generator_strategy import PDFGeneratorStrategy
from model.document_data import DocumentData
from model.file.FileType import FileType
from model.request_result import RequestResult
from model.user.role import UserRole
from service.file_service import FileService
from service.time_entry_service import TimeEntryService
from service.timesheet_service import TimesheetService
from service.user_service import UserService


class DocumentService:
    """
    The DocumentService class is responsible for generating documents.

    """

    def __init__(self):
        """
        Initializes the DocumentService instance.

        """
        self.pdf_generator_strategy = PDFGeneratorStrategy()
        self.user_service = UserService()
        self.time_entry_service = TimeEntryService()
        self.timesheet_service = TimesheetService()
        self.file_service = FileService()

    def generate_multiple_documents(self, usernames: list[str], month: int, year: int, requesting_username: str):
        """
        Generates a zip file containing PDF documents for a specified list of users, month, and year.
        Each document is gathered and generated based on user-specific data for the given time period.

        :param usernames: The usernames of the users for which to generate the documents.
        :param month: The month for which to generate the documents.
        :param year: The year for which to generate the documents.

        :return: The generated documents.
        """
        documents = []
        for username in usernames:
            if not self._check_if_authorized(requesting_username, username):
                return RequestResult(False, "Unauthorized to generate document", status_code=403)
            document = self.gather_document_data(month, year, username)
            if document is None:
                return RequestResult(False, "Failed to gather document data.", status_code=400)
            documents.append(document)
        output_dir = self.pdf_generator_strategy.generate_multiple_documents(documents).data
        if not output_dir:
            return RequestResult(False, "Failed to generate documents.", status_code=500)
        stream = self._create_zip_from_directory(output_dir)
        return RequestResult(True, "Documents generated successfully.", 200, stream)

    def generate_document(self, month: int, year: int, username: str, requesting_username: str):
        """
        Generates a document for the given month and year.

        :param month: The month for which to generate the document.
        :param year: The year for which to generate the document.
        :param username: The username of the user for which to generate the document.

        :return: The generated document.
        """
        if not self._check_if_authorized(requesting_username, username):
            return RequestResult(False, "Unauthorized to generate document", status_code=403)
        document_data = self.gather_document_data(month, year, username)
        if document_data is None:
            return RequestResult(False, "Failed to gather document data.", status_code=400)
        return self.pdf_generator_strategy.generate_document(document_data)

    def generate_multiple_documents_by_id(self, timesheet_ids: list[str], requesting_username: str):
        """
        Generates a zip file containing PDF documents for a specified list of timesheet IDs.

        :param timesheet_ids: The timesheet IDs for which to generate the documents.

        :return: The generated documents.
        """
        documents = []
        for timesheet_id in timesheet_ids:
            timesheet = self.timesheet_service.get_timesheet_by_id(timesheet_id).data
            if timesheet is None:
                return RequestResult(False, "Failed to gather document data.", status_code=400)
            if not self._check_if_authorized(requesting_username, timesheet.username):
                return RequestResult(False, "Unauthorized to generate document", status_code=403)
            document = self.gather_document_data(timesheet.month, timesheet.year, timesheet.username)
            if document is None:
                return RequestResult(False, "Failed to gather document data.", status_code=400)
            documents.append(document)
        output_dir = self.pdf_generator_strategy.generate_multiple_documents(documents).data
        if not output_dir:
            return RequestResult(False, "Failed to generate documents.", status_code=500)
        stream = self._create_zip_from_directory(output_dir)
        return RequestResult(True, "Documents generated successfully.", 200, stream)

    def _create_zip_from_directory(self, output_dir: str) -> BytesIO:
        """
        Creates a zip file from all PDF files in the given directory.

        :param output_dir: The directory containing the PDF files.

        :return: The zip file as a BytesIO stream.
        """
        stream = BytesIO()
        with ZipFile(stream, 'w') as zip_file:
            for file in glob(output_dir + '/*.pdf'):
                zip_file.write(file, os.path.basename(file))
                os.remove(file)
        stream.seek(0)
        return stream

    def generate_document_in_date_range(self, start_date: datetime, end_date: datetime, username: str, requesting_username: str):
        """
        Generates a document for the given date range.

        :param start_date: The start date of the date range.
        :param end_date: The end date of the date range.
        :param username: The username of the user for which to generate the document.

        :return: The generated document.
        """
        if not self._check_if_authorized(requesting_username, username):
            return RequestResult(False, "Unauthorized to generate document", status_code=403)
        documents = []
        while start_date <= end_date:
            document = self.gather_document_data(start_date.month, start_date.year, username)
            if document is None:
                start_date = self._increment_month(start_date)
                continue
            documents.append(document)
            start_date = self._increment_month(start_date)
        output_dir = self.pdf_generator_strategy.generate_multiple_documents(documents).data
        if not output_dir:
            return RequestResult(False, "Failed to generate documents.", status_code=500)
        stream = self._create_zip_from_directory(output_dir)
        return RequestResult(True, "Documents generated successfully.", 200, stream)

    def _increment_month(self, date):
        """
        Increments the month of the given date. If the month is December,
         the year is incremented and the month is set to January.

        :param date: The date to increment.

        :return: The date with the month incremented.
        """
        return date.replace(month=date.month + 1) if date.month < 12 else date.replace(month=1, year=date.year + 1)
    def gather_document_data(self, month: int, year: int, username: str):
        """
        Gathers the data required for generating a document.

        :param month: The month for which to gather the data.
        :param year: The year for which to gather the data.
        :param username: The username of the user for which to gather the data.

        :return: The document data.
        """
        user = self.user_service.get_profile(username)
        if user.role != UserRole.HIWI:
            return None
        result = self.timesheet_service.get_timesheet(username, month, year)
        if result.status_code != 200:
            return None
        if result.data.status != TimesheetStatus.COMPLETE:
            return None
        supervisor = self.user_service.get_profile(user.supervisor)
        if supervisor.role != UserRole.SUPERVISOR:
            return None
        timesheet = result.data
        time_entries = self.time_entry_service.get_entries_of_timesheet(timesheet.timesheet_id).data
        signature_stream = self.file_service.get_image(username, FileType.SIGNATURE)
        supervisor_signature_stream = self.file_service.get_image(supervisor.username, FileType.SIGNATURE)
        previous_overtime = self.timesheet_service.get_previous_overtime(username, month, year)
        if signature_stream is None:
            return None
        return DocumentData(month, year, user.personal_info, user.contract_info, self._time_format(previous_overtime), signature_stream,
                            supervisor_signature_stream, self._time_format(timesheet.overtime), time_entries)

    def _time_format(self, minutes: int):
        """
        Formats the given number of minutes to a time string.

        :param minutes: The number of minutes to format.

        :return: The formatted time string.
        """
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02d}:{int(minutes):02d}"
    def _check_if_authorized(self, requesting_username: str, username: str):
        """
        Checks if the requesting user is authorized to access the data of the specified user.

        :param requesting_username: The username of the requesting user.
        :param username: The username of the user whose data is being accessed.

        :return: True if the requesting user is authorized, False otherwise.
        """
        if requesting_username == username:
            return True
        requesting_user = self.user_service.get_profile(requesting_username)
        if requesting_user.role == UserRole.ADMIN or requesting_user.role == UserRole.SECRETARY:
            return True
        if requesting_user.role == UserRole.SUPERVISOR and username in requesting_user.hiwis:
            return True
        else:
            return False
