from flask import Flask
from .config import Config
from .extensions import db, jwt

# Import blueprints
from .routes.auth_routes import auth_bp
from .routes.user_routes import user_bp
from .routes.loan_routes import loan_bp
from .routes.payment_routes import payment_bp
from .routes.group_routes import group_bp
from .routes.reputation_routes import reputation_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(reputation_bp)

    # Create tables if missing
    # Do not automatically create tables here. Tests and deployment
    # environments should manage database migrations or create tables
    # explicitly. Creating tables here can interfere with test DB setup.

    return app
