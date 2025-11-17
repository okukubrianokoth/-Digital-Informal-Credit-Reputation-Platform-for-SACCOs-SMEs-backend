from datetime import datetime
from app.extensions import db

class GroupMember(db.Model):
    __tablename__ = "group_members"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # role in the group: member, admin, treasurer, chair
    role = db.Column(db.String(50), default="member", nullable=False)

    # contribution and withdrawal balances (simple ledger)
    contributions_total = db.Column(db.Numeric, default=0.0)
    withdrawals_total = db.Column(db.Numeric, default=0.0)

    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # relationships
    group = db.relationship("Group", back_populates="members", lazy="joined")
    user = db.relationship("User", backref="group_memberships", lazy="joined")

    def to_dict(self, include_user=False, include_group=False):
        data = {
            "id": self.id,
            "group_id": self.group_id,
            "user_id": self.user_id,
            "role": self.role,
            "contributions_total": float(self.contributions_total or 0.0),
            "withdrawals_total": float(self.withdrawals_total or 0.0),
            "joined_at": self.joined_at.isoformat() if self.joined_at else None,
            "is_active": self.is_active,
        }
        if include_user and self.user:
            data["user"] = {
                "id": self.user.id,
                "full_name": getattr(self.user, "full_name", None) or getattr(self.user, "name", None),
                "phone": getattr(self.user, "phone", None),
                "email": getattr(self.user, "email", None)
            }
        if include_group and self.group:
            data["group"] = {
                "id": self.group.id,
                "name": self.group.name
            }
        return data
