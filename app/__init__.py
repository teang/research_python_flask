from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import config
from app.models import db, User
import os


# Initialize Flask-Migrate globally
migrate = Migrate()


def create_app(config_name='default'):
    """Application Factory สำหรับสร้าง Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Setup CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize security features
    from app.security import init_security
    init_security(app)

    # Initialize caching
    from app.cache import init_cache
    init_cache(app)

    # Initialize monitoring and logging
    from app.monitoring import init_logging, init_sentry, init_metrics
    init_logging(app)
    init_sentry(app)
    init_metrics(app)

    # Initialize Swagger documentation
    try:
        from app.swagger import init_swagger
        init_swagger(app)
    except ImportError:
        app.logger.warning('Swagger not available, API documentation disabled')

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
    from app.health import health_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(research_bp, url_prefix='/research')
    app.register_blueprint(api_bp)  # API routes with /api/v1 prefix
    app.register_blueprint(admin_bp)  # Admin routes with /admin prefix
    app.register_blueprint(health_bp)  # Health check endpoints

    # Register CLI commands
    from app import cli
    cli.register_commands(app)

    # Log successful startup
    app.logger.info(f'Application started in {config_name} mode')

    return app
