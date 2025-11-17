# backend/app/services/loan_service.py

from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.loan import Loan
from app.models.user import User
from app.models.group_members import GroupMember
from app.models.group import Group


class LoanService:

    @staticmethod
    def apply_loan(user_id, amount, term_months, group_id=None):
        """Apply for a new loan. Optionally link to a group."""
        if amount <= 0 or term_months <= 0:
            raise Exception("Amount and term must be positive")

        user = User.query.get(user_id)
        if not user:
            raise Exception("User not found")

        group_member = None
        if group_id:
            group_member = GroupMember.query.filter_by(
                group_id=group_id, user_id=user_id
            ).first()
            if not group_member:
                raise Exception("User is not a member of the specified group")

        try:
            loan = Loan(
                user_id=user_id,
                amount=amount,
                term_months=term_months,
                status="pending",
                group_id=group_id
            )
            db.session.add(loan)
            db.session.commit()
            return loan
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to apply loan: {str(e)}")

    @staticmethod
    def get_loan(loan_id):
        """Retrieve a loan by ID."""
        return Loan.query.get(loan_id)

    @staticmethod
    def list_loans(user_id=None, group_id=None):
        """List all loans, optionally filter by user or group."""
        query = Loan.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        if group_id:
            query = query.filter_by(group_id=group_id)
        return query.order_by(Loan.created_at.desc()).all()

    @staticmethod
    def approve_loan(loan_id, approved_by):
        """Approve a pending loan."""
        loan = Loan.query.get(loan_id)
        if not loan:
            raise Exception("Loan not found")
        if loan.status != "pending":
            raise Exception("Only pending loans can be approved")

        try:
            loan.status = "approved"
            loan.approved_by = approved_by
            db.session.commit()
            return loan
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to approve loan: {str(e)}")

    @staticmethod
    def reject_loan(loan_id, rejected_by, reason=None):
        """Reject a pending loan."""
        loan = Loan.query.get(loan_id)
        if not loan:
            raise Exception("Loan not found")
        if loan.status != "pending":
            raise Exception("Only pending loans can be rejected")

        try:
            loan.status = "rejected"
            loan.rejected_by = rejected_by
            loan.rejection_reason = reason
            db.session.commit()
            return loan
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to reject loan: {str(e)}")

    @staticmethod
    def repay_loan(loan_id, amount):
        """Repay an approved loan partially or fully."""
        if amount <= 0:
            raise Exception("Repayment amount must be positive")

        loan = Loan.query.get(loan_id)
        if not loan:
            raise Exception("Loan not found")
        if loan.status != "approved":
            raise Exception("Only approved loans can be repaid")

        try:
            loan.repaid_amount += amount
            if loan.repaid_amount >= loan.amount:
                loan.status = "repaid"
            db.session.commit()
            return loan
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to repay loan: {str(e)}")
