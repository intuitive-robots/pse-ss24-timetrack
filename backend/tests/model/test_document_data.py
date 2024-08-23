import unittest

from model.document_data import DocumentData
from model.user.contract_information import ContractInfo
from model.user.personal_information import PersonalInfo


class TestDocumentData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.document_data = DocumentData(1, 2021, PersonalInfo("Test", "User",
                                                               "test@email.com", "1234567890",
                                                               "Test Institute"), ContractInfo(12.5,
                                                                                               80, 0,
                                                                                               0), 0,
                                         None, None,
                                         0, [])

    def test_get_monthly_working_hours(self):
        """
        Test that the get_monthly_working_hours method returns the correct total number of working hours in a month
        """
        self.assertEqual(self.document_data.get_monthly_working_hours(), "00:00")

    def test_get_contract_hours_per_month(self):
        """
        Test that the get_contract_hours_per_month method returns the correct total number of working hours in a month
        """
        self.assertEqual(self.document_data.get_contract_hours_per_month(), "80:00")

    def test_get_formatted_time_string(self):
        """
        Test that the get_formatted_time_string method returns the correct formatted string representing the time period of the document
        """
        self.assertEqual(self.document_data.get_formatted_time_string(), "January / 2021")
