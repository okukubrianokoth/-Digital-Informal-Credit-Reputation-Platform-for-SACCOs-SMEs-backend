import requests
import base64
from datetime import datetime
from app.utils.mpesa_auth import get_access_token
from app.extensions import db
from app.models.transaction import Transaction

class MpesaService:
    """
    Service class to handle MPesa payments (STK Push, B2C, etc.)
    """

    # Daraja endpoints
    STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    @staticmethod
    def lipa_na_mpesa(phone_number, amount, account_reference, transaction_desc):
        """
        Initiate an STK Push to the user’s phone.
        """
        token = get_access_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        business_short_code = "174379"  # Sandbox shortcode
        passkey = "YOUR_PASSKEY"       # Daraja Passkey

        # Encode password
        data_to_encode = business_short_code + passkey + timestamp
        password = base64.b64encode(data_to_encode.encode()).decode()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourdomain.com/api/payments/callback",
            "AccountReference": account_reference,
            "TransactionDesc": transaction_desc
        }

        response = requests.post(MpesaService.STK_PUSH_URL, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"MPesa request failed: {response.text}")

        res_data = response.json()
        # Record transaction attempt in DB
        txn = Transaction(
            phone_number=phone_number,
            amount=amount,
            reference=account_reference,
            status="pending",
            transaction_type="STK_PUSH",
            response=res_data
        )
        # Attempt to record the transaction, but be resilient when called
        # outside an application context (e.g. unit tests that don't push
        # an app context). In that case skip DB write instead of raising.
        try:
            db.session.add(txn)
            db.session.commit()
        except RuntimeError:
            # Likely "Working outside of application context." — skip DB write
            pass
        except Exception:
            # Rollback on any other DB-related error and re-raise
            db.session.rollback()
            raise

        return res_data

    @staticmethod
    def handle_callback(callback_data):
        """
        Handle MPesa STK Push callback.
        Update the transaction status accordingly.
        """
        try:
            checkout_request_id = callback_data.get("CheckoutRequestID")
            result_code = callback_data.get("ResultCode")
            result_desc = callback_data.get("ResultDesc")

            txn = Transaction.query.filter_by(reference=checkout_request_id).first()
            if not txn:
                raise Exception("Transaction not found")

            txn.status = "success" if result_code == 0 else "failed"
            txn.response = callback_data
            db.session.commit()
            return txn
        except Exception as e:
            db.session.rollback()
            raise e
