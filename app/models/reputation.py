from datetime import datetime
from app.extensions import db

class Reputation(db.Model):
    """
    Tracks user reputation based on loan repayments, contributions, group activity, etc.
    """
    __tablename__ = "reputations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    score = db.Column(db.Float, default=0.0)  # Reputation score
    level = db.Column(db.String(50), default="Novice")  # Novice, Bronze, Silver, Gold, Platinum
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", backref="reputation", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "score": self.score,
            "level": self.level,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
