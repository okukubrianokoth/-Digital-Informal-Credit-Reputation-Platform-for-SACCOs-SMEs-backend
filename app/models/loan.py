# backend/app/models/loan.py
from datetime import datetime
from app.extensions import db

class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    term_months = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, default=0.05)
    status = db.Column(db.String(20), default="pending")
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    rejected_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    rejected_reason = db.Column(db.String(255), nullable=True)
    amount_paid = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships (optional backrefs already handled in User)
    group = db.relationship("Group", backref="loans")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "group_id": self.group_id,
            "amount": self.amount,
            "term_months": self.term_months,
            "interest_rate": self.interest_rate,
            "status": self.status,
            "approved_by": self.approved_by,
            "rejected_by": self.rejected_by,
            "rejected_reason": self.rejected_reason,
            "amount_paid": self.amount_paid,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
