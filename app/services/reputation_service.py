from app.extensions import db
from app.models.reputation import Reputation
from app.models.user import User

class ReputationService:

    @staticmethod
    def get_reputation(user_id):
        """Get user's reputation, create if doesn't exist."""
        reputation = Reputation.query.filter_by(user_id=user_id).first()
        if not reputation:
            reputation = Reputation(user_id=user_id)
            db.session.add(reputation)
            db.session.commit()
        return reputation

    @staticmethod
    def update_score(user_id, delta):
        """
        Increase or decrease reputation score.
        Delta can be positive or negative based on user activity.
        """
        reputation = ReputationService.get_reputation(user_id)
        reputation.score += delta
        reputation.score = max(reputation.score, 0)  # score can't be negative

        # Update level based on thresholds
        if reputation.score >= 1000:
            reputation.level = "Platinum"
        elif reputation.score >= 500:
            reputation.level = "Gold"
        elif reputation.score >= 250:
            reputation.level = "Silver"
        elif reputation.score >= 100:
            reputation.level = "Bronze"
        else:
            reputation.level = "Novice"

        db.session.commit()
        return reputation

    @staticmethod
    def set_level(user_id, level):
        """Directly set user level."""
        reputation = ReputationService.get_reputation(user_id)
        reputation.level = level
        db.session.commit()
        return reputation
