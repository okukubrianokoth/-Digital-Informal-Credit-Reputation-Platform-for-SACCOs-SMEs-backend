# backend/app/routes/auth_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.services.user_service import UserService
from app.models.user import User  # <-- required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# -------------------------------
# User Login
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    try:
        # authenticate using real UserService from services layer
        user = UserService.authenticate(email, password)

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------
# Refresh Token
# -------------------------------
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": access_token}), 200


# -------------------------------
# Protected Route Example
# -------------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = UserService.get_user(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200
