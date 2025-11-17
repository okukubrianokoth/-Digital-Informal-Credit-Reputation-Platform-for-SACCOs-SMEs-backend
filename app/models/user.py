# backend/app/models/user.py
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # -------------------------------
    # Loan Relationships
    # -------------------------------
    # Loans where user is the applicant
    loans = db.relationship(
        "Loan",
        lazy=True,
        backref="applicant",
        foreign_keys="Loan.user_id"
    )

    # Loans approved by this user (if admin)
    approved_loans = db.relationship(
        "Loan",
        lazy=True,
        backref="approver",
        foreign_keys="Loan.approved_by"
    )

    # Loans rejected by this user (if admin)
    rejected_loans = db.relationship(
        "Loan",
        lazy=True,
        backref="rejecter",
        foreign_keys="Loan.rejected_by"
    )

    # -------------------------------
    # Group Memberships
    # -------------------------------
    groups = db.relationship(
        "GroupMember",
        lazy=True,
        foreign_keys="GroupMember.user_id",  # explicitly specify FK
        backref="member_user"  # unique backref to avoid conflicts
    )

    # -------------------------------
    # Password Handling
    # -------------------------------
    def set_password(self, password):
        """Hashes and sets the user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password against stored hash."""
        return check_password_hash(self.password_hash, password)

    # -------------------------------
    # Serialization
    # -------------------------------
    def to_dict(self, include_sensitive=False):
        """Return user info as dict."""
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if include_sensitive:
            data["password_hash"] = self.password_hash
        return data
