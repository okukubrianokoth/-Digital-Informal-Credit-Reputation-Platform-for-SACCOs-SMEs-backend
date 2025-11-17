# backend/app/services/group_service.py

from app.models.group import Group
from app.models.user import User
from app.models.group_members import GroupMember
from app.extensions import db

class GroupService:

    # -------------------------------
    # Create a New Group
    # -------------------------------
    @staticmethod
    def create_group(name, description, created_by):
        group = Group(name=name, description=description, created_by=created_by)
        db.session.add(group)
        db.session.commit()

        # Add creator as admin
        GroupService.add_member(group.id, created_by, role="admin")
        return group

    # -------------------------------
    # List All Groups
    # -------------------------------
    @staticmethod
    def list_groups():
        return Group.query.all()

    # -------------------------------
    # Get a Single Group
    # -------------------------------
    @staticmethod
    def get_group(group_id):
        return Group.query.get(group_id)

    # -------------------------------
    # Delete Group
    # -------------------------------
    @staticmethod
    def delete_group(group_id):
        group = Group.query.get(group_id)
        if not group:
            raise Exception("Group not found")
        db.session.delete(group)
        db.session.commit()

    # -------------------------------
    # Add Member
    # -------------------------------
    @staticmethod
    def add_member(group_id, user_id, role="member"):
        group = Group.query.get(group_id)
        if not group:
            raise Exception("Group not found")
        user = User.query.get(user_id)
        if not user:
            raise Exception("User not found")

        existing = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
        if existing:
            raise Exception("User already in group")

        member = GroupMember(group_id=group_id, user_id=user_id, role=role)
        db.session.add(member)
        db.session.commit()
        return member

    # -------------------------------
    # List Members
    # -------------------------------
    @staticmethod
    def list_members(group_id):
        return GroupMember.query.filter_by(group_id=group_id).all()

    # -------------------------------
    # Remove Member
    # -------------------------------
    @staticmethod
    def remove_member(group_id, user_id):
        member = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
        if not member:
            raise Exception("Member not found")
        db.session.delete(member)
        db.session.commit()

    # -------------------------------
    # Change Member Role
    # -------------------------------
    @staticmethod
    def change_role(group_id, user_id, new_role):
        member = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
        if not member:
            raise Exception("Member not found")
        member.role = new_role
        db.session.commit()
        return member

    # -------------------------------
    # Contribute to Group Pool
    # -------------------------------
    @staticmethod
    def contribute(group_id, user_id, amount):
        if amount <= 0:
            raise Exception("Contribution must be positive")
        group = Group.query.get(group_id)
        if not group:
            raise Exception("Group not found")
        member = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
        if not member:
            raise Exception("Member not in group")

        group.pool += amount
        db.session.commit()
        return {"message": f"{amount} contributed to group pool", "pool_balance": group.pool}

    # -------------------------------
    # Withdraw from Group Pool
    # -------------------------------
    @staticmethod
    def withdraw(group_id, user_id, amount):
        if amount <= 0:
            raise Exception("Withdrawal must be positive")
        group = Group.query.get(group_id)
        if not group:
            raise Exception("Group not found")
        member = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
        if not member:
            raise Exception("Member not in group")
        if amount > group.pool:
            raise Exception("Insufficient group funds")

        group.pool -= amount
        db.session.commit()
        return {"message": f"{amount} withdrawn from group pool", "pool_balance": group.pool}
