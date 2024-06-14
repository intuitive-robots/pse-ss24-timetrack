import fillpdf
from fillpdf import fillpdfs

from controller.strategy.document_generator_strategy import DocumentGeneratorStrategy
from pypdf import PdfWriter
import pdfrw

from model.document_data import DocumentData
from model.request_result import RequestResult
from model.time_entry_type import TimeEntryType


class PDFGeneratorStrategy(DocumentGeneratorStrategy):

    def generate_document(self, document_data: DocumentData):
        """
        Generates a PDF document based on the given data.
        :param document_data: The data to use for generating the PDF document.
        :return: The generated PDF document.
        """
        if document_data is None:
            return RequestResult(False, "No data provided", 400)

        fields = fillpdfs.get_form_fields("../documents/Timesheet/timesheet_template.pdf")
        print(fields)
        full_name = document_data.personal_info.last_name + ", " + document_data.personal_info.first_name
        #TODO: Implement GFB, UB
        data_dict = {
            "Personalnummer": document_data.personal_info.personal_number,  # Personalnummer
            "abc": document_data.month,  # Monat
            "abdd": document_data.year,  # Jahr
            "GF": full_name,  # Name, Vorname
            "GFB": "On",  # GF On/Off
            "UB": "On",  # UB On/Off
            "OE": document_data.personal_info.institute_name,  # Institute
            "Std": document_data.contract_info.working_hours,  # Contracted working hours
            "Stundensatz": document_data.contract_info.hourly_wage,  # Hourly wage
            "Summe": document_data.get_monthly_working_hours(),  # Total
            "monatliche SollArbeitszeit": document_data.get_contract_hours_per_month(),  # Monthly target working hours
            "Urlaub anteilig": "Urlaub anteilig",  # Holiday pro rata
            "Übertrag vom Vormonat": document_data.overtime_from_previous_month,  # Transfer from previous month
            "Übertrag in den Folgemonat": document_data.get_overtime(),  # Carryover to the following month

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

        #TODO: This may not work in docker
        output_path = (f"../documents/Timesheet/Export/{document_data.personal_info.first_name}"
                       f" {document_data.personal_info.last_name} {document_data.month}.pdf")
        fillpdfs.write_fillable_pdf("../documents/Timesheet/timesheet_template.pdf",
                                    output_path,
                                    data_dict)
        return RequestResult(True, "Document generated successfully", 200, output_path)

    def generate_multiple_documents(self, documents: list[DocumentData]):
        """
        Generates multiple PDF documents based on the given list of data.
        :param documents: The list of data to use for generating the PDF documents.
        :return: The list of generated PDF documents.
        """
        if documents is None:
            return RequestResult(False, "No data provided", 400)

        output_dir = "../documents/Timesheet/Export/"
        for document_data in documents:
            result = self.generate_document(document_data)
            if result.status_code != 200:
                return RequestResult(False, "Some of the documents couldn't be generated",
                                     result.status_code, output_dir)
        return RequestResult(True, "Documents generated successfully", 200, output_dir)
