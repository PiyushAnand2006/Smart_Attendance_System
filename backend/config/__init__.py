# Flask Configuration
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///smartattend.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Attendance Settings
    ATTENDANCE_THRESHOLD = float(os.environ.get('ATTENDANCE_THRESHOLD', '75.0'))
    LATE_THRESHOLD_MINUTES = int(os.environ.get('LATE_THRESHOLD_MINUTES', '15'))
    
    # QR Settings
    QR_TOKEN_EXPIRY_SECONDS = int(os.environ.get('QR_TOKEN_EXPIRY_SECONDS', '300'))
    QR_SESSION_EXPIRY_MINUTES = int(os.environ.get('QR_SESSION_EXPIRY_MINUTES', '60'))
    
    # WhatsApp Settings
    WHATSAPP_MODE = os.environ.get('WHATSAPP_MODE', 'mock')
    WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')
    WHATSAPP_BUSINESS_ACCOUNT_ID = os.environ.get('WHATSAPP_BUSINESS_ACCOUNT_ID', '')
    WHATSAPP_API_VERSION = os.environ.get('WHATSAPP_API_VERSION', 'v18.0')
    WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')
    
    # Face Recognition Settings
    FACE_RECOGNITION_TOLERANCE = float(os.environ.get('FACE_RECOGNITION_TOLERANCE', '0.6'))
    FACE_ENROLLMENT_SAMPLES = int(os.environ.get('FACE_ENROLLMENT_SAMPLES', '5'))
    
    # Notification Settings
    NOTIFICATION_RETRY_ATTEMPTS = int(os.environ.get('NOTIFICATION_RETRY_ATTEMPTS', '3'))
    NOTIFICATION_RETRY_DELAY_SECONDS = int(os.environ.get('NOTIFICATION_RETRY_DELAY_SECONDS', '60'))
    
    # File Upload Settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}