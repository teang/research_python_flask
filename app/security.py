"""
Security utilities and middleware for the application
"""
from functools import wraps
from flask import request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt
from datetime import datetime, timedelta
import bleach
from werkzeug.exceptions import TooManyRequests
import logging

logger = logging.getLogger(__name__)


# Initialize Rate Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # Will be overridden by Redis in production
    strategy="fixed-window"
)


def init_security(app):
    """Initialize security features"""
    # Initialize rate limiter with app
    limiter.init_app(app)

    # Set Redis storage if available
    if app.config.get('REDIS_URL'):
        limiter.storage_uri = app.config['REDIS_URL']

    # Add security headers middleware
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses"""
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'

        # Prevent MIME sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # XSS Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Content Security Policy (adjust as needed)
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self';"
        )
        response.headers['Content-Security-Policy'] = csp

        # HTTPS enforcement in production
        if not app.config.get('DEBUG'):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        # Permissions Policy (formerly Feature-Policy)
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        return response

    # Error handler for rate limiting
    @app.errorhandler(TooManyRequests)
    def handle_rate_limit_exceeded(e):
        """Handle rate limit exceeded errors"""
        if request.path.startswith('/api/'):
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': str(e.description)
            }), 429
        return "Rate limit exceeded. Please try again later.", 429

    logger.info("Security features initialized")


# JWT Token Management
class JWTManager:
    """Manage JWT tokens for API authentication"""

    @staticmethod
    def generate_token(user_id, expires_in=3600):
        """Generate JWT token for user"""
        try:
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=expires_in),
                'iat': datetime.utcnow()
            }

            token = jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )

            return token

        except Exception as e:
            logger.error(f"Error generating JWT token: {str(e)}")
            return None

    @staticmethod
    def verify_token(token):
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {str(e)}")
            return None


def require_api_token(f):
    """Decorator to require JWT token for API endpoints"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401

        if not token:
            return jsonify({'error': 'Missing authentication token'}), 401

        # Verify token
        payload = JWTManager.verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Add user_id to request context
        request.user_id = payload['user_id']

        return f(*args, **kwargs)

    return decorated


# Input Sanitization
class InputSanitizer:
    """Sanitize user input to prevent XSS and injection attacks"""

    # Allowed HTML tags and attributes for rich text
    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 'a'
    ]

    ALLOWED_ATTRIBUTES = {
        'a': ['href', 'title', 'target'],
        'code': ['class']
    }

    @staticmethod
    def sanitize_html(html_content):
        """Sanitize HTML content"""
        if not html_content:
            return html_content

        return bleach.clean(
            html_content,
            tags=InputSanitizer.ALLOWED_TAGS,
            attributes=InputSanitizer.ALLOWED_ATTRIBUTES,
            strip=True
        )

    @staticmethod
    def sanitize_text(text):
        """Sanitize plain text (strip all HTML)"""
        if not text:
            return text

        return bleach.clean(text, tags=[], strip=True)

    @staticmethod
    def sanitize_url(url):
        """Sanitize and validate URL"""
        if not url:
            return url

        # Remove potentially dangerous protocols
        dangerous_protocols = ['javascript:', 'data:', 'vbscript:']
        url_lower = url.lower().strip()

        for protocol in dangerous_protocols:
            if url_lower.startswith(protocol):
                return ''

        return bleach.clean(url, tags=[], strip=True)


# Password strength validator
class PasswordValidator:
    """Validate password strength"""

    MIN_LENGTH = 8
    REQUIRE_UPPERCASE = True
    REQUIRE_LOWERCASE = True
    REQUIRE_DIGIT = True
    REQUIRE_SPECIAL = False

    @staticmethod
    def validate(password):
        """
        Validate password strength

        Returns:
            tuple: (is_valid, error_message)
        """
        if len(password) < PasswordValidator.MIN_LENGTH:
            return False, f'Password must be at least {PasswordValidator.MIN_LENGTH} characters long'

        if PasswordValidator.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
            return False, 'Password must contain at least one uppercase letter'

        if PasswordValidator.REQUIRE_LOWERCASE and not any(c.islower() for c in password):
            return False, 'Password must contain at least one lowercase letter'

        if PasswordValidator.REQUIRE_DIGIT and not any(c.isdigit() for c in password):
            return False, 'Password must contain at least one digit'

        if PasswordValidator.REQUIRE_SPECIAL:
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(c in special_chars for c in password):
                return False, 'Password must contain at least one special character'

        return True, ''


# File upload security
class FileUploadValidator:
    """Validate file uploads"""

    ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png', 'gif'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileUploadValidator.ALLOWED_EXTENSIONS

    @staticmethod
    def validate_file_size(file):
        """Validate file size"""
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset to start

        if size > FileUploadValidator.MAX_FILE_SIZE:
            return False, f'File too large. Maximum size is {FileUploadValidator.MAX_FILE_SIZE / (1024*1024):.0f}MB'

        return True, ''

    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename to prevent path traversal"""
        from werkzeug.utils import secure_filename
        return secure_filename(filename)


# SQL Injection prevention helpers
class SQLSafetyHelpers:
    """Helpers for SQL injection prevention"""

    @staticmethod
    def validate_order_by(column, allowed_columns):
        """Validate ORDER BY column to prevent SQL injection"""
        if column not in allowed_columns:
            return allowed_columns[0]  # Return default
        return column

    @staticmethod
    def validate_sort_order(order):
        """Validate sort order"""
        return 'ASC' if order.upper() == 'ASC' else 'DESC'

    @staticmethod
    def validate_limit(limit, max_limit=100):
        """Validate LIMIT value"""
        try:
            limit = int(limit)
            if limit < 1:
                return 10
            if limit > max_limit:
                return max_limit
            return limit
        except (ValueError, TypeError):
            return 10


# CSRF token helpers
def generate_csrf_token():
    """Generate CSRF token"""
    import secrets
    return secrets.token_urlsafe(32)


# Rate limiting decorators for specific use cases
def auth_rate_limit():
    """Rate limit decorator for authentication endpoints"""
    return limiter.limit("5 per minute")


def api_rate_limit():
    """Rate limit decorator for API endpoints"""
    return limiter.limit("30 per minute")


def general_rate_limit():
    """Rate limit decorator for general endpoints"""
    return limiter.limit("60 per minute")
