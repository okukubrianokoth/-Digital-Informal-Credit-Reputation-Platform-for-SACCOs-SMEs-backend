# backend/app/routes/user_routes.py

from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


# -------------------------------
# Register / Create User
# -------------------------------
@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    phone_number = data.get("phone_number")
    is_admin = data.get("is_admin", False)

    if not all([full_name, email, password]):
        return jsonify({"error": "full_name, email, and password are required"}), 400

    try:
        user = UserService.create_user(full_name, email, password, phone_number, is_admin)
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------
# List All Users
# -------------------------------
@user_bp.route("/", methods=["GET"])
def list_users():
    users = UserService.list_users()
    return jsonify([u.to_dict() for u in users]), 200


# -------------------------------
# Get Single User by ID
# -------------------------------
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = UserService.get_user(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


# -------------------------------
# Update User
# -------------------------------
@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    try:
        user = UserService.update_user(user_id, **data)
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# -------------------------------
# Deactivate User
# -------------------------------
@user_bp.route("/<int:user_id>/deactivate", methods=["POST"])
def deactivate_user(user_id):
    try:
        user = UserService.deactivate_user(user_id)
        return jsonify({"message": f"User {user.full_name} deactivated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
