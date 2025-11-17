from flask import Blueprint, request, jsonify
from app.services.mpesa_service import MpesaService

payment_bp = Blueprint("payments", __name__, url_prefix="/api/payments")


# -------------------------------
# Trigger MPesa Payment (STK Push)
# -------------------------------
@payment_bp.route("/stkpush", methods=["POST"])
def stk_push():
    data = request.json
    phone_number = data.get("phone_number")
    amount = data.get("amount")
    account_ref = data.get("account_reference")
    transaction_desc = data.get("transaction_desc", "Payment")

    if not all([phone_number, amount, account_ref]):
        return jsonify({"error": "phone_number, amount, and account_reference required"}), 400

    try:
        res = MpesaService.lipa_na_mpesa(phone_number, amount, account_ref, transaction_desc)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------
# MPesa Callback Endpoint
# -------------------------------
@payment_bp.route("/callback", methods=["POST"])
def mpesa_callback():
    data = request.json
    try:
        txn = MpesaService.handle_callback(data)
        return jsonify({"message": "Callback handled", "transaction_id": txn.id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
