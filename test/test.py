# Filename: tests/test_end_to_end.py

import unittest
from src.main import app
from src.login import authenticate_user
from src.reservation import create_reservation
from src.stripe import process_payment

class TestHotelManagementSystem(unittest.TestCase):
    def setUp(self):
        """Set up the test client for Flask app and test data."""
        self.app = app.test_client()
        self.app.testing = True
        self.user_credentials = {'username': 'testuser', 'password': 'password123'}
        self.booking_details = {
            'user_id': 1,
            'room_type': 'Deluxe',
            'check_in': '2025-01-10',
            'check_out': '2025-01-15',
            'guests': 2
        }
        self.payment_details = {
            'amount': 500.00,
            'currency': 'USD',
            'payment_method': 'test_card_1234'
        }

    def test_user_authentication(self):
        """Test user login functionality."""
        response = authenticate_user(self.user_credentials['username'], self.user_credentials['password'])
        self.assertTrue(response, "User authentication failed")

    def test_booking_creation(self):
        """Test booking creation functionality."""
        response = create_reservation(**self.booking_details)
        self.assertIsNotNone(response, "Failed to create booking")
        self.assertEqual(response['status'], 'success', "Booking status is not 'success'")

    def test_payment_processing(self):
        """Test payment processing functionality."""
        response = process_payment(self.payment_details['amount'], self.payment_details['currency'], self.payment_details['payment_method'])
        self.assertIsNotNone(response, "Failed to process payment")
        self.assertEqual(response['status'], 'success', "Payment status is not 'success'")

    def test_end_to_end_booking_flow(self):
        """Test end-to-end booking flow including authentication, booking, and payment."""
        # Step 1: Authenticate User
        auth_response = authenticate_user(self.user_credentials['username'], self.user_credentials['password'])
        self.assertTrue(auth_response, "End-to-end: User authentication failed")

        # Step 2: Create Booking
        booking_response = create_reservation(**self.booking_details)
        self.assertIsNotNone(booking_response, "End-to-end: Booking creation failed")
        self.assertEqual(booking_response['status'], 'success', "End-to-end: Booking status is not 'success'")

        # Step 3: Process Payment
        payment_response = process_payment(self.payment_details['amount'], self.payment_details['currency'], self.payment_details['payment_method'])
        self.assertIsNotNone(payment_response, "End-to-end: Payment processing failed")
        self.assertEqual(payment_response['status'], 'success', "End-to-end: Payment status is not 'success'")

if __name__ == "__main__":
    unittest.main()
