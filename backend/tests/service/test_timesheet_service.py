import datetime
import unittest

from bson import ObjectId

from model.repository.timesheet_repository import TimesheetRepository
from model.timesheet import Timesheet
from model.timesheet_status import TimesheetStatus
from service.timesheet_service import TimesheetService


class TestTimesheetService(unittest.TestCase):
    def setUp(self):
        self.timesheet_service = TimesheetService()
        self.timesheet_repository = TimesheetRepository.get_instance()

    def test_ensure_timesheet_exists(self):
        """
        Test the ensure_timesheet_exists method of the TimesheetService class.
        """
        # Test ensuring a timesheet exists for a user
        test_username = "testHiwi1"

        # Test ensuring a timesheet exists for a user that already has one
        result = self.timesheet_service.ensure_timesheet_exists(test_username, 5, 2024)
        self.assertTrue(result.is_successful)
        self.assertEqual(result.status_code, 200)
        self.assertIsNotNone(self.timesheet_repository.get_timesheet(test_username, 5, 2024))

        # Test ensuring a timesheet exists for a user that has no timesheet
        result = self.timesheet_service.ensure_timesheet_exists(test_username, 8, 2024)
        self.assertTrue(result.is_successful)
        self.assertEqual(result.status_code, 201)
        self.assertIsNotNone(self.timesheet_repository.get_timesheet(test_username, 8, 2024))

    def test_create_timesheet(self):
        """
        Test the create_timesheet method of the TimesheetService class.
        """
        # Test creating a timesheet for a user
        test_username = "testHiwi1"
        test_month = 8
        test_year = 2024
        result = self.timesheet_service._create_timesheet(test_username, test_month, test_year)
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(self.timesheet_repository.get_timesheet(test_username, test_month, test_year))
        timesheet_id = self.timesheet_repository.get_timesheet_id(test_username, test_month, test_year)
        delete_result = self.timesheet_repository.delete_timesheet(timesheet_id)
        self.assertTrue(delete_result.is_successful)

    def test_sign_timesheet(self):
        """
        Test the sign_timesheet method of the TimesheetService class.
        """
        # Test signing a timesheet
        test_timesheet_id = "6679ca2935df0d8f7202c5fa"
        self.timesheet_service.sign_timesheet(test_timesheet_id)
        timesheet = self.timesheet_repository.get_timesheet_by_id(test_timesheet_id)
        self.assertEqual("Waiting for Approval", timesheet["status"])
        self.timesheet_repository.set_timesheet_status(test_timesheet_id, TimesheetStatus.NOT_SUBMITTED)
        # Test signing a timesheet that is already signed
        test_signed_timesheet_id = "667bd050cf0aa6181e9c8dd9"
        result = self.timesheet_service.sign_timesheet(test_signed_timesheet_id)
        self.assertFalse(result.is_successful)

    def test_approve_timesheet(self):
        """
        Test the approve_timesheet method of the TimesheetService class.
        """
        # Test approving a timesheet
        test_timesheet_id = "667bd177cf0aa6181e9c8ddb"
        self.timesheet_service.approve_timesheet(test_timesheet_id)
        timesheet = self.timesheet_repository.get_timesheet_by_id(test_timesheet_id)
        self.assertEqual("Complete", timesheet["status"])
        self.timesheet_repository.set_timesheet_status(test_timesheet_id, TimesheetStatus.WAITING_FOR_APPROVAL)
        # Test approving a timesheet that hasn't been submitted
        test_unsigned_timesheet_id = "6679ca2935df0d8f7202c5fa"
        result = self.timesheet_service.approve_timesheet(test_unsigned_timesheet_id)
        self.assertFalse(result.is_successful)

    def test_request_change(self):
        """
        Test the request_timesheet method of the TimesheetService class.
        """
        # Test requesting a timesheet
        test_timesheet_id = "667bd177cf0aa6181e9c8ddb"
        self.timesheet_service.request_change(test_timesheet_id)
        timesheet = self.timesheet_repository.get_timesheet_by_id(test_timesheet_id)
        self.assertEqual("Revision", timesheet["status"])
        self.timesheet_repository.set_timesheet_status(test_timesheet_id, TimesheetStatus.WAITING_FOR_APPROVAL)
        # Test requesting a timesheet that is already complete
        test_completed_timesheet_id = "667bd050cf0aa6181e9c8dd9"
        result = self.timesheet_service.request_change(test_completed_timesheet_id)
        self.assertFalse(result.is_successful)

    def test_get_timesheet_by_id(self):
        """
        Test the get_timesheet_by_id method of the TimesheetService class.
        """
        print(self.timesheet_repository.get_timesheet_by_id("6679ca2935df0d8f7202c5fa"))
        # Test getting a timesheet by ID
        test_timesheet_data = {"_id": ObjectId("6679ca2935df0d8f7202c5fa"),
                               "username": "testHiwi1",
                               "month": 5,
                               "year": 2024,
                               "status": "Not Submitted",
                               "totalTime": 0.0,
                               "overtime": 0.0,
                               "lastSignatureChange": datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)}
        test_timesheet_id = str(test_timesheet_data["_id"])
        result = self.timesheet_service.get_timesheet_by_id(test_timesheet_id)
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(result.data.timesheet_id, test_timesheet_data["_id"])
        # Test getting a nonexistent timesheet by ID
        test_nonexistent_timesheet_id = "000000000000000000000000"
        result = self.timesheet_service.get_timesheet_by_id(test_nonexistent_timesheet_id)
        self.assertFalse(result.is_successful)

    def test_get_timesheets_by_username(self):
        """
        Test the get_timesheets_by_username method of the TimesheetService class.
        """
        # Test getting timesheets by username
        test_timesheet_data = [
            {"_id": ObjectId("6679ca2935df0d8f7202c5fa"), "username": "testHiwi1", "month": 5, "year": 2024,
             "status": "Not Submitted", "totalTime": 0.0, "overtime": 0.0,
             "lastSignatureChange": datetime.datetime(2024, 6, 24, 21, 22, 35, 855000)},
            {"_id": ObjectId("667bd050cf0aa6181e9c8dd9"), "username": "testHiwi1", "month": 4, "year": 2024,
             "status": "Complete", "totalTime": 0.0, "overtime": 0.0,
             "lastSignatureChange": datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)},
            {"_id": ObjectId("667bd14ecf0aa6181e9c8dda"), "username": "testHiwi1", "month": 3, "year": 2024,
             "status": "Complete", "totalTime": 0.0, "overtime": 0.0,
             "lastSignatureChange": datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)}]
        result = self.timesheet_service.get_timesheets_by_username("testHiwi1")
        self.assertTrue(result.is_successful)
        self.assertEqual(len(result.data), len(test_timesheet_data))
        self.assertEqual(result.data[0].timesheet_id, test_timesheet_data[0]["_id"])
        self.assertEqual(result.data[1].timesheet_id, test_timesheet_data[1]["_id"])
        self.assertEqual(result.data[2].timesheet_id, test_timesheet_data[2]["_id"])

    def test_get_timesheets_by_username_status(self):
        """
        Test the get_timesheets_by_username_status method of the TimesheetService class.
        """
        test_timesheet_data = [
            {"_id": ObjectId("667bd050cf0aa6181e9c8dd9"), "username": "testHiwi1", "month": 4, "year": 2024,
             "status": "Complete", "totalTime": 0.0, "overtime": 0.0,
             "lastSignatureChange": datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)},
            {"_id": ObjectId("667bd14ecf0aa6181e9c8dda"), "username": "testHiwi1", "month": 3, "year": 2024,
             "status": "Complete", "totalTime": 0.0, "overtime": 0.0,
             "lastSignatureChange": datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)}]
        result = self.timesheet_service.get_timesheets_by_username_status("testHiwi1", TimesheetStatus.COMPLETE)
        self.assertTrue(result.is_successful)
        self.assertEqual(len(result.data), len(test_timesheet_data))
        self.assertEqual(result.data[0].timesheet_id, test_timesheet_data[0]["_id"])
        self.assertEqual(result.data[1].timesheet_id, test_timesheet_data[1]["_id"])

    def test_get_timesheet_id(self):
        """
        Test the get_timesheet_id method of the TimesheetService class.        :return:
        """
        # Test existing timesheet
        test_timesheet_data = {"_id": ObjectId("667bd050cf0aa6181e9c8dd9"),
                               "username": "testHiwi1",
                               "month": 4,
                               "year": 2024,
                               "status": "Complete",
                               "totalTime": 0.0,
                               "overtime": 0.0,
                               "lastSignatureChange": datetime.datetime(2024, 6, 26, 9, 56, 45, 440000)}
        result = self.timesheet_service.get_timesheet_id(test_timesheet_data["username"], test_timesheet_data["month"], test_timesheet_data["year"])
        self.assertEqual(test_timesheet_data["_id"], result.data)
        # Test nonexistent timesheet
        fail_result = self.timesheet_service.get_timesheet_id("testHiwiNonexistent", 5, 2024)
        self.assertFalse(fail_result.is_successful)

    def test_get_current_timesheet(self):
        """
        Test the get_current_timesheet method of the TimesheetService class.
        """
        # Test getting the current timesheet for a user
        test_username = "testHiwi1"
        test_timesheet_id = ObjectId("6679ca2935df0d8f7202c5fa")
        result = self.timesheet_service.get_current_timesheet(test_username)
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(result.data.timesheet_id, test_timesheet_id)
        # Test getting current timesheet of a user that has no unsubmitted timesheets
        test_fail_username = "testHiwi3"
        fail_result = self.timesheet_service.get_current_timesheet(test_fail_username)
        self.assertFalse(fail_result.is_successful)

    def test_get_timesheet(self):
        """
        Test the get_timesheet method of the TimesheetService class.
        """
        # Test getting a timesheet for a user
        test_username = "testHiwi1"
        test_month = 5
        test_year = 2024
        test_timesheet_id = ObjectId("6679ca2935df0d8f7202c5fa")
        result = self.timesheet_service.get_timesheet(test_username, test_month, test_year)
        self.assertTrue(result.is_successful)
        self.assertIsNotNone(result.data)
        self.assertEqual(test_timesheet_id, result.data.timesheet_id)
        # Test getting a nonexistent timesheet for a user
        test_nonexistent_username = "testHiwiNonexistent"
        result = self.timesheet_service.get_timesheet(test_nonexistent_username, test_month, test_year)
        self.assertFalse(result.is_successful)

