import os
from datetime import timedelta


class Config:
    """การตั้งค่าสำหรับ Flask Application"""

    # Secret Key สำหรับ Session และ CSRF Protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database Configuration - PostgreSQL
    # Format: postgresql://username:password@localhost:5432/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/research_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }

    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Upload Configuration (สำหรับอัพโหลดไฟล์ PDF ในอนาคต)
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}


class DevelopmentConfig(Config):
    """การตั้งค่าสำหรับ Development"""
    DEBUG = True


class ProductionConfig(Config):
    """การตั้งค่าสำหรับ Production"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
