from datetime import datetime
from app.extensions import db

class Transaction(db.Model):
    """
    Transaction model to record MPesa and other payment transactions.
    """
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reference = db.Column(db.String(100), unique=True, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # e.g., STK_PUSH, B2C
    status = db.Column(db.String(20), nullable=False, default="pending")
    response = db.Column(db.JSON, nullable=True)  # Store raw response from MPesa
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "phone_number": self.phone_number,
            "amount": self.amount,
            "reference": self.reference,
            "transaction_type": self.transaction_type,
            "status": self.status,
            "response": self.response,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
