# app/__init__.py (Project restructuring)
from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager, cache
from app.models import SiteVisitor, User, ContactMessage
from app.routes import main, api
from app.utils import validators, helpers


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)

    # Register blueprints
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp, url_prefix="/api/v1")

    # Error handlers
    register_error_handlers(app)

    return app
