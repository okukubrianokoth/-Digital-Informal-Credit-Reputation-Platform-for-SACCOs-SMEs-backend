# backend/app/services/user_service.py

from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.user import User


class UserService:

    @staticmethod
    def create_user(full_name, email, password, phone_number=None, is_admin=False):
        """
        Create a new user and hash the password before saving.
        """
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            raise Exception("Email already registered")

        try:
            user = User(
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                is_admin=is_admin
            )
            user.set_password(password)  # Hash password

            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to create user: {str(e)}")

    @staticmethod
    def get_user(user_id):
        """
        Retrieve a user by ID.
        """
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_email(email):
        """
        Retrieve a user by email.
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def authenticate(email, password):
        """
        Authenticate a user by email and password. Returns the user if
        credentials are valid, otherwise returns None.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user

    @staticmethod
    def list_users():
        """
        Return all users.
        """
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def update_user(user_id, **kwargs):
        """
        Update user attributes. Accepts full_name, phone_number, password, is_active, is_admin.
        """
        user = User.query.get(user_id)
        if not user:
            raise Exception("User not found")

        try:
            for key, value in kwargs.items():
                if key == "password":
                    user.set_password(value)
                elif hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to update user: {str(e)}")

    @staticmethod
    def deactivate_user(user_id):
        """
        Deactivate a user account.
        """
        user = User.query.get(user_id)
        if not user:
            raise Exception("User not found")
        try:
            user.is_active = False
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Failed to deactivate user: {str(e)}")
