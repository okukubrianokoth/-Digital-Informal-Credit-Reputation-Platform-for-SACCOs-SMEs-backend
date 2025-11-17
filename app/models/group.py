# app/models/group.py
from datetime import datetime
from app.extensions import db

class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # relationships
    members = db.relationship("GroupMember", back_populates="group", cascade="all, delete-orphan")
    creator = db.relationship("User", backref="created_groups", foreign_keys=[created_by])

    def to_dict(self, include_members=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }
        if include_members:
            data["members"] = [m.to_dict() for m in self.members]
        return data
