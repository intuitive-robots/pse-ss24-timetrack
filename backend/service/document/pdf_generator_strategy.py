import os
from datetime import datetime

import pytz
from fillpdf import fillpdfs

from model.vacation_entry import VacationEntry
from service.document.document_generator_strategy import DocumentGeneratorStrategy
from model.document_data import DocumentData
from model.request_result import RequestResult
from model.time_entry_type import TimeEntryType


class PDFGeneratorStrategy(DocumentGeneratorStrategy):
    """
    The PDFGeneratorStrategy class is responsible for generating PDF documents.

    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_PATH = os.path.join(BASE_DIR, "..", "resources", "timesheet_template.pdf")
    TEMP_DIR = os.path.join(BASE_DIR, "..", "resources", "temp")
    SIGNATURE_WIDTH = 300
    SIGNATURE_HEIGHT = 30
    SIGNATURE_X_POS = 18
    SIGNATURE_Y_POS = 637
    SUPERVISOR_SIGNATURE_X_POS = 257
    SUPERVISOR_SIGNATURE_Y_POS = 637

    def generate_document(self, document_data: DocumentData):
        """
        Generates a PDF document based on the given data.

        :param document_data: The data to use for generating the PDF document.

        :return: The generated PDF document.
        """
        if document_data is None:
            return RequestResult(False, "No data provided", 400)

        if not os.path.exists(self.TEMP_DIR):
            os.makedirs(self.TEMP_DIR)

        if document_data.time_entries is None:
            document_data.time_entries = []

        data_dict = self._prepare_data_dict(document_data)
        vacation_minutes = 0
        for i in range(len(document_data.time_entries)):
            time_entry = document_data.time_entries[i]
            if time_entry.entry_type == TimeEntryType.VACATION_ENTRY:
                vacation_minutes += time_entry.get_duration()
            formatted_data = self._format_time_entry_data(time_entry, i)
            data_dict.update(formatted_data)
        hours, minutes = divmod(vacation_minutes, 60)
        duration_str = f"{int(hours):02d}:{int(minutes):02d}"
        data_dict["Urlaub anteilig"] = duration_str
        output_path_pdf = self._get_output_path(document_data, "Unsigned.pdf")
        fillpdfs.write_fillable_pdf(self.TEMPLATE_PATH,
                                    output_path_pdf,
                                    data_dict)
        signature_path = self._get_output_path(document_data, "Signature.png")
        self._temporary_store_signature(document_data.signature, signature_path)

        supervisor_signature_path = self._get_output_path(document_data, "SupervisorSignature.png")
        self._temporary_store_signature(document_data.supervisor_signature, supervisor_signature_path)

        output_path_pdf_signed = self._get_output_path(document_data, "Signed.pdf")
        self._place_signature(output_path_pdf, output_path_pdf_signed, signature_path, True)

        output_path_pdf_approved = self._get_output_path(document_data, "Approved.pdf")
        self._place_signature(output_path_pdf_signed, output_path_pdf_approved, supervisor_signature_path, False)
        self._cleanup_temp_files([output_path_pdf, output_path_pdf_signed, signature_path, supervisor_signature_path])

        return RequestResult(True, "Document generated successfully", 200, output_path_pdf_approved)

    def _place_signature(self, pdf_path, output_path, signature_path, type_hiwi: bool):
        """
        Places the signature on the PDF document.

        :param pdf_path: The path to the PDF document.
        :param output_path: The path to the output PDF document.
        :param signature_path: The path to the signature image.
        :param type_hiwi: The type of the signature (Hiwi or supervisor).
        """
        signature_x_pos = self.SIGNATURE_X_POS if type_hiwi else self.SUPERVISOR_SIGNATURE_X_POS

        fillpdfs.place_image(signature_path, signature_x_pos, self.SIGNATURE_Y_POS, pdf_path, output_path, 1,
                             width=self.SIGNATURE_WIDTH, height=self.SIGNATURE_HEIGHT)


    def _get_output_path(self, document_data, suffix):
        """
        Returns the output path for the generated PDF document.

        :param document_data: The document data.
        :param suffix: The suffix to append to the file name.

        :return: The output path for the generated PDF document.
        """
        return os.path.join(self.TEMP_DIR,
                            f"{document_data.personal_info.first_name}_{document_data.personal_info.last_name}"
                            f"_{document_data.month}_{suffix}")
    def _format_time_entry_data(self, time_entry, i):
        """
        Formats the time entry data for the PDF document.

        :param time_entry: The time entry data to format.
        :param i: The index of the time entry.

        :return: The formatted time entry data.
        """
        formatted_data = {}
        if time_entry.entry_type == TimeEntryType.WORK_ENTRY:
            formatted_data[f"Tätigkeit Stichwort ProjektRow{i + 1}"] = time_entry.get_activity_project_str()
            hours, minutes = divmod(time_entry.break_time, 60)
            formatted_break_time = f"{int(hours):02d}:{int(minutes):02d}"
            formatted_data[f"hhmmRow{i + 1}_3"] = formatted_break_time
        else:
            formatted_data[f"Tätigkeit Stichwort ProjektRow{i + 1}"] = "Urlaub"

        berlin_tz = pytz.timezone('Europe/Berlin')
        start_time_berlin = time_entry.start_time.replace(tzinfo=pytz.utc).astimezone(berlin_tz)
        end_time_berlin = time_entry.end_time.replace(tzinfo=pytz.utc).astimezone(berlin_tz)
        formatted_data[f"ttmmjjRow{i + 1}"] = start_time_berlin.strftime("%d.%m.%y")
        formatted_data[f"hhmmRow{i + 1}"] = start_time_berlin.strftime("%H:%M")
        formatted_data[f"hhmmRow{i + 1}_2"] = end_time_berlin.strftime("%H:%M")
        formatted_data[f"hhmmRow{i + 1}_4"] = time_entry.get_duration_hhmm()
        return formatted_data

    def _prepare_data_dict(self, document_data):
        """
        Prepares the data dictionary for the PDF document.

        :param document_data: The document data.

        :return: The data dictionary for the PDF document.
        """
        personal_info = document_data.personal_info
        contract_info = document_data.contract_info
        data_dict = {
            "Personalnummer": personal_info.personal_number,
            "abc": document_data.month,
            "abdd": document_data.year,
            "GF": f"{personal_info.last_name}, {personal_info.first_name}",
            "GFB": "On",
            "UB": "Off",
            "OE": personal_info.institute_name,
            "Std": contract_info.working_hours,
            "Stundensatz": contract_info.hourly_wage,
            "Summe": document_data.get_monthly_working_hours(),
            "monatliche SollArbeitszeit": document_data.get_contract_hours_per_month(),
            "Urlaub anteilig": "",
            "Übertrag vom Vormonat": document_data.overtime_from_previous_month,
            "Übertrag in den Folgemonat": document_data.overtime,
            "Ich bestätige die Richtigkeit der Angaben": document_data.last_signature_changed.strftime("%d.%m.%Y, "),
            "undefined": document_data.last_signature_changed.strftime("%d.%m.%Y, ")
        }
        return data_dict

    def _temporary_store_signature(self, signature_stream, path):
        """
        Stores the signature image in a temporary file.

        :param signature_stream: The signature image stream.

        :param path: The path to store the signature image.
        """
        with open(path, "wb") as file:
            file.write(signature_stream.read())
            file.close()

    def _cleanup_temp_files(self, files):
        for file_path in files:
            os.remove(file_path)

    def generate_multiple_documents(self, documents: list[DocumentData]):
        """
        Generates multiple PDF documents based on the given list of data.

        :param documents: The list of data to use for generating the PDF documents.

        :return: The list of generated PDF documents.
        """
        if documents is None:
            return RequestResult(False, "No data provided", 400)

        for document_data in documents:
            if not document_data:
                return RequestResult(False, "No data provided", 400)
            result = self.generate_document(document_data)
            if result.status_code != 200:
                return RequestResult(False, "Some of the documents couldn't be generated",
                                     result.status_code, self.TEMP_DIR)
        return RequestResult(True, "Documents generated successfully", 200, self.TEMP_DIR)
