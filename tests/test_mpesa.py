import unittest
from unittest.mock import patch
from app.services.mpesa_service import MpesaService

class MpesaServiceTestCase(unittest.TestCase):

    @patch("app.services.mpesa_service.requests.post")
    @patch("app.services.mpesa_service.get_access_token")
    def test_lipa_na_mpesa_success(self, mock_token, mock_post):
        mock_token.return_value = "fake_token"
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ResponseCode": "0"}

        response = MpesaService.lipa_na_mpesa(
            phone_number="254700000000",
            amount=10,
            account_reference="TEST001",
            transaction_desc="Testing STK Push"
        )

        self.assertIn("ResponseCode", response)
        self.assertEqual(response["ResponseCode"], "0")

if __name__ == "__main__":
    unittest.main()
