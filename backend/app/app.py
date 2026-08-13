"""Application Factory

The full backend runs on Flask + flask-cors + PyJWT (the packages that are
installed). Data is stored in an in-memory store (see app.store), seeded with
demo data so every feature works out of the box.
"""
from flask import Flask
from flask_cors import CORS
from config import config
import os


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app, resources={r"/api/*": {"origins": "*"}})

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
    from app.routes.face import face_bp
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
    app.register_blueprint(face_bp, url_prefix='/api/face')
    app.register_blueprint(qr_bp, url_prefix='/api/qr')

    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Create upload folder if not exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app
