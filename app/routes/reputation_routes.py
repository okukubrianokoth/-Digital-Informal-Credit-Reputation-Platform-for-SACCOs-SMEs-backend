# backend/app/routes/reputation_routes.py

from flask import Blueprint, request, jsonify
from app.services.reputation_service import ReputationService  # Assuming you'll implement this

# Define the blueprint
reputation_bp = Blueprint("reputation", __name__, url_prefix="/api/reputation")

# -------------------------------
# Test / Example Route
# -------------------------------
@reputation_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Reputation routes are working"}), 200

# -------------------------------
# Add reputation points to a user
# -------------------------------
@reputation_bp.route("/add", methods=["POST"])
def add_reputation():
    data = request.json
    user_id = data.get("user_id")
    points = data.get("points", 0)

    if not user_id or points <= 0:
        return jsonify({"error": "user_id and positive points are required"}), 400

    try:
        result = ReputationService.add_points(user_id, points)
        return jsonify({"message": "Points added", "reputation": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------------------
# Get user reputation
# -------------------------------
@reputation_bp.route("/<int:user_id>", methods=["GET"])
def get_reputation(user_id):
    try:
        result = ReputationService.get_reputation(user_id)
        return jsonify({"user_id": user_id, "reputation": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
