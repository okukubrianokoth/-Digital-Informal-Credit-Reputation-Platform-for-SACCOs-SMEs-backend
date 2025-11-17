# backend/app/routes/group_routes.py

from flask import Blueprint, request, jsonify
from app.services.group_service import GroupService
from app.models.group import Group
from app.models.group_members import GroupMember
from app.extensions import db

group_bp = Blueprint("groups", __name__, url_prefix="/api/groups")


@group_bp.route("/", methods=["POST"])
def create_group():
    data = request.get_json()
    name = data.get("name")
    admin_id = data.get("admin_id")

    try:
        group = GroupService.create_group(name, admin_id)
        return jsonify({"message": "Group created successfully", "group_id": group.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@group_bp.route("/<int:group_id>/add_member", methods=["POST"])
def add_member(group_id):
    data = request.get_json()
    user_id = data.get("user_id")

    try:
        member = GroupService.add_member(group_id, user_id)
        return jsonify({"message": "Member added successfully", "member_id": member.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@group_bp.route("/<int:group_id>", methods=["GET"])
def get_group(group_id):
    group = Group.query.get(group_id)
    if not group:
        return jsonify({"error": "Group not found"}), 404

    members = [{"id": m.user_id} for m in group.members]
    return jsonify({"id": group.id, "name": group.name, "admin_id": group.admin_id, "members": members})


@group_bp.route("/", methods=["GET"])
def get_all_groups():
    groups = Group.query.all()
    group_list = [{"id": g.id, "name": g.name, "admin_id": g.admin_id} for g in groups]
    return jsonify(group_list)
