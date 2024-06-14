import os
from datetime import datetime
import fillpdf
from fillpdf import fillpdfs
from controller.strategy.document_generator_strategy import DocumentGeneratorStrategy
from model.document_data import DocumentData
from model.request_result import RequestResult
from model.time_entry_type import TimeEntryType


class PDFGeneratorStrategy(DocumentGeneratorStrategy):
    TEMPLATE_PATH = "resources/timesheet_template.pdf"
    TEMP_DIR = "resources/temp/"
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

        fields = fillpdfs.get_form_fields(self.TEMPLATE_PATH)
        full_name = document_data.personal_info.last_name + ", " + document_data.personal_info.first_name
        data_dict = {
            "Personalnummer": document_data.personal_info.personal_number,  # Personalnummer
            "abc": document_data.month,  # Monat
            "abdd": document_data.year,  # Jahr
            "GF": full_name,  # Name, Vorname
            "GFB": "On",  # GF On/Off
            "UB": "Off",  # UB On/Off
            "OE": document_data.personal_info.institute_name,  # Institute
            "Std": document_data.contract_info.working_hours,  # Contracted working hours
            "Stundensatz": document_data.contract_info.hourly_wage,  # Hourly wage
            "Summe": document_data.get_monthly_working_hours(),  # Total
            "monatliche SollArbeitszeit": document_data.get_contract_hours_per_month(),  # Monthly target working hours
            "Urlaub anteilig": "Urlaub anteilig",  # Holiday pro rata
            "Übertrag vom Vormonat": document_data.overtime_from_previous_month,  # Transfer from previous month
            "Übertrag in den Folgemonat": document_data.get_overtime(),  # Carryover to the following month
            "Ich bestätige die Richtigkeit der Angaben": str(datetime.now().strftime("%d.%m.%Y") + ", "),  # Date
            "undefined": str(datetime.now().strftime("%d.%m.%Y") + ", ")  # Date
        }
        for i in range(len(document_data.time_entries)):
            time_entry = document_data.time_entries[i]
            if time_entry.entry_type == TimeEntryType.WORK_ENTRY:
                data_dict[f"Tätigkeit Stichwort ProjektRow{i + 1}"] = (time_entry.activity + ", " +
                                                                       time_entry.project_name)
                hours, minutes = divmod(time_entry.break_time, 60)
                formatted_break_time = f"{int(hours):02d}:{int(minutes):02d}"
                data_dict[f"hhmmRow{i + 1}_3"] = formatted_break_time

            data_dict[f"ttmmjjRow{i + 1}"] = time_entry.start_time.strftime("%d.%m.%y")
            data_dict[f"hhmmRow{i + 1}"] = time_entry.start_time.strftime("%H:%M")
            data_dict[f"hhmmRow{i + 1}_2"] = time_entry.end_time.strftime("%H:%M")
            data_dict[f"hhmmRow{i + 1}_4"] = time_entry.get_duration()

        output_path_pdf = (f"{self.TEMP_DIR}{document_data.personal_info.first_name}"
                           f" {document_data.personal_info.last_name} {document_data.month} Raw.pdf")
        fillpdfs.write_fillable_pdf(self.TEMPLATE_PATH,
                                    output_path_pdf,
                                    data_dict)
        signature_path = (f"{self.TEMP_DIR}{document_data.personal_info.first_name} "
                          f"{document_data.personal_info.last_name} Signature.png")
        self._temporary_store_signature(document_data.signature, signature_path)

        supervisor_signature_path = (f"{self.TEMP_DIR}{document_data.personal_info.first_name} "
                                     f"{document_data.personal_info.last_name} Supervisor Signature.png")
        self._temporary_store_signature(document_data.supervisor_signature, supervisor_signature_path)

        output_path_pdf_signed = (f"{self.TEMP_DIR}{document_data.personal_info.first_name}"
                              f" {document_data.personal_info.last_name} {document_data.month} Signed.pdf")
        fillpdfs.place_image(signature_path, self.SIGNATURE_X_POS, self.SIGNATURE_Y_POS, output_path_pdf,
                             output_path_pdf_signed, 1, width=self.SIGNATURE_WIDTH, height=self.SIGNATURE_HEIGHT)

        output_path_pdf_approved = (f"{self.TEMP_DIR}{document_data.personal_info.first_name}"
                                    f" {document_data.personal_info.last_name} {document_data.month}.pdf")
        fillpdfs.place_image(supervisor_signature_path, self.SUPERVISOR_SIGNATURE_X_POS, self.SIGNATURE_Y_POS,
                             output_path_pdf_signed, output_path_pdf_approved, 1,
                             width=self.SIGNATURE_WIDTH, height=self.SIGNATURE_HEIGHT)
        os.remove(signature_path)
        os.remove(supervisor_signature_path)
        os.remove(output_path_pdf)
        os.remove(output_path_pdf_signed)
        return RequestResult(True, "Document generated successfully", 200, output_path_pdf_approved)

    def _temporary_store_signature(self, signature_stream, path):
        """
        Stores the signature image in a temporary file.
        :param signature_stream: The signature image stream.
        :param path: The path to store the signature image.
        """
        with open(path, "wb") as file:
            file.write(signature_stream.read())

    def generate_multiple_documents(self, documents: list[DocumentData]):
        """
        Generates multiple PDF documents based on the given list of data.
        :param documents: The list of data to use for generating the PDF documents.
        :return: The list of generated PDF documents.
        """
        if documents is None:
            return RequestResult(False, "No data provided", 400)

        for document_data in documents:
            result = self.generate_document(document_data)
            if result.status_code != 200:
                return RequestResult(False, "Some of the documents couldn't be generated",
                                     result.status_code, self.TEMP_DIR)
        return RequestResult(True, "Documents generated successfully", 200, self.TEMP_DIR)
