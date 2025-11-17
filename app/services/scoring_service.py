from app.models.user import User
from app.models.loan import Loan
from app.models.reputation import Reputation
from app.models.group_members import GroupMember
from sqlalchemy import func

class ScoringService:
    """
    Service to calculate user credit score based on:
    - Loan repayment history
    - Group contribution participation
    - Reputation points
    """

    @staticmethod
    def calculate_user_score(user_id):
        """
        Returns a numeric score between 0 and 100.
        """
        user = User.query.get(user_id)
        if not user:
            raise Exception("User not found")

        # Base score from reputation points (0-50)
        reputation = Reputation.query.filter_by(user_id=user_id).first()
        rep_points = reputation.points if reputation else 0
        rep_score = min(rep_points, 50)  # cap at 50

        # Loan repayment score (0-30)
        loans = Loan.query.filter_by(user_id=user_id).all()
        total_loans = len(loans)
        repaid_loans = len([l for l in loans if l.status == "repaid"])
        loan_score = 0
        if total_loans > 0:
            loan_score = int((repaid_loans / total_loans) * 30)

        # Group participation score (0-20)
        memberships = GroupMember.query.filter_by(user_id=user_id).all()
        contributions = sum([m.contributions_total for m in memberships])
        group_score = 0
        if memberships:
            group_score = min(int((contributions / (len(memberships) * 1000)) * 20), 20)

        # Total score
        total_score = rep_score + loan_score + group_score
        return {
            "user_id": user_id,
            "score": total_score,
            "details": {
                "reputation": rep_score,
                "loan_repayment": loan_score,
                "group_participation": group_score
            }
        }
