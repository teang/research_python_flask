from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from config import config
from app.models import db, User
import os


def create_app(config_name='default'):
    """Application Factory สำหรับสร้าง Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Extensions
    db.init_app(app)

    # Setup CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'กรุณาเข้าสู่ระบบเพื่อเข้าถึงหน้านี้'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # สร้างโฟลเดอร์สำหรับอัพโหลดไฟล์
    upload_folders = [
        app.config.get('UPLOAD_FOLDER', 'uploads'),
        'uploads/researches',
        'uploads/avatars'
    ]
    for folder in upload_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Register Blueprints
    from app.routes import main_bp, auth_bp, research_bp
    from app.api import api_bp
    from app.admin_routes import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(research_bp, url_prefix='/research')
    app.register_blueprint(api_bp)  # API routes with /api/v1 prefix
    app.register_blueprint(admin_bp)  # Admin routes with /admin prefix

    # สร้างตารางในฐานข้อมูล
    with app.app_context():
        db.create_all()

    return app
