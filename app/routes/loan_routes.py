# backend/app/routes/loan_routes.py

from flask import Blueprint, request, jsonify
from app.services.loan_service import LoanService

loan_bp = Blueprint("loans", __name__, url_prefix="/api/loans")


# -------------------------------
# Apply for a Loan
# -------------------------------
@loan_bp.route("/", methods=["POST"])
def apply_loan():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")
    term_months = data.get("term_months")
    group_id = data.get("group_id")  # optional

    if not all([user_id, amount, term_months]):
        return jsonify({"error": "user_id, amount, and term_months are required"}), 400

    try:
        loan = LoanService.apply_loan(user_id, amount, term_months, group_id)
        return jsonify(loan.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------
# List Loans
# -------------------------------
@loan_bp.route("/", methods=["GET"])
def list_loans():
    user_id = request.args.get("user_id", type=int)
    group_id = request.args.get("group_id", type=int)

    loans = LoanService.list_loans(user_id=user_id, group_id=group_id)
    return jsonify([loan.to_dict() for loan in loans]), 200


# -------------------------------
# Get Single Loan
# -------------------------------
@loan_bp.route("/<int:loan_id>", methods=["GET"])
def get_loan(loan_id):
    loan = LoanService.get_loan(loan_id)
    if not loan:
        return jsonify({"error": "Loan not found"}), 404
    return jsonify(loan.to_dict()), 200


# -------------------------------
# Approve Loan
# -------------------------------
@loan_bp.route("/<int:loan_id>/approve", methods=["POST"])
def approve_loan(loan_id):
    data = request.json
    approved_by = data.get("approved_by")
    if not approved_by:
        return jsonify({"error": "approved_by is required"}), 400

    try:
        loan = LoanService.approve_loan(loan_id, approved_by)
        return jsonify(loan.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------
# Reject Loan
# -------------------------------
@loan_bp.route("/<int:loan_id>/reject", methods=["POST"])
def reject_loan(loan_id):
    data = request.json
    rejected_by = data.get("rejected_by")
    reason = data.get("reason", None)

    if not rejected_by:
        return jsonify({"error": "rejected_by is required"}), 400

    try:
        loan = LoanService.reject_loan(loan_id, rejected_by, reason)
        return jsonify(loan.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------
# Repay Loan
# -------------------------------
@loan_bp.route("/<int:loan_id>/repay", methods=["POST"])
def repay_loan(loan_id):
    data = request.json
    amount = data.get("amount")
    if not amount:
        return jsonify({"error": "amount is required"}), 400

    try:
        loan = LoanService.repay_loan(loan_id, amount)
        return jsonify(loan.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
