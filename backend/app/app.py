"""Application Factory

The full backend runs on Flask + flask-cors + PyJWT (installed dependencies) with
a SQLite database (SQLAlchemy). Demo data is seeded on startup so every feature
works out of the box.
"""
from datetime import date, datetime
from decimal import Decimal

from flask import Flask
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from config import config
import os


class SmartAttendJSONProvider(DefaultJSONProvider):
    """JSON encoder that understands datetimes, dates and decimals."""

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.json = SmartAttendJSONProvider(app)
    # Accept both "/api/x" and "/api/x/" without redirecting.
    app.url_map.strict_slashes = False
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Database setup
    from app.db import init_db, session_scope
    from app.store import seed_db
    init_db()
    with session_scope() as session:
        seed_db(session)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.students import students_bp
    from app.routes.faculty import faculty_bp
    from app.routes.admin import admin_bp
    from app.routes.attendance import attendance_bp
    from app.routes.reports import reports_bp
    from app.routes.notifications import notifications_bp
    from app.routes.subjects import subjects_bp
    from app.routes.classes import classes_bp
    from app.routes.qr import qr_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(students_bp, url_prefix='/api/students')
    app.register_blueprint(faculty_bp, url_prefix='/api/faculty')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
    app.register_blueprint(subjects_bp, url_prefix='/api/subjects')
    app.register_blueprint(classes_bp, url_prefix='/api/classes')
    app.register_blueprint(qr_bp, url_prefix='/api/qr')

    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Create upload folder if not exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
