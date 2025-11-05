"""
Error monitoring and logging configuration
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger


def init_logging(app):
    """Initialize structured logging"""

    # Create logs directory
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Set log level
    log_level = logging.DEBUG if app.debug else logging.INFO

    # JSON formatter for structured logging
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d'
    )

    # File handler with rotation
    file_handler = RotatingFileHandler(
        'logs/research_app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(json_formatter)
    file_handler.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    console_handler.setLevel(log_level)

    # Configure app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)

    # Log application startup
    app.logger.info('Research Management System starting up', extra={
        'environment': app.config.get('ENV', 'unknown'),
        'debug': app.debug
    })


def init_sentry(app):
    """Initialize Sentry error monitoring"""
    sentry_dsn = app.config.get('SENTRY_DSN')

    if sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.flask import FlaskIntegration
            from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
            from sentry_sdk.integrations.redis import RedisIntegration

            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[
                    FlaskIntegration(),
                    SqlalchemyIntegration(),
                    RedisIntegration(),
                ],
                environment=app.config.get('SENTRY_ENVIRONMENT', 'development'),
                traces_sample_rate=0.1 if not app.debug else 0.0,
                send_default_pii=False,  # Don't send personally identifiable information
            )

            app.logger.info('Sentry error monitoring initialized')

        except ImportError:
            app.logger.warning('Sentry SDK not installed, error monitoring disabled')
        except Exception as e:
            app.logger.error(f'Failed to initialize Sentry: {str(e)}')
    else:
        app.logger.info('Sentry DSN not configured, error monitoring disabled')


def init_metrics(app):
    """Initialize Prometheus metrics"""
    try:
        from prometheus_flask_exporter import PrometheusMetrics

        metrics = PrometheusMetrics(app)
        metrics.info('app_info', 'Application info', version='1.0.0')

        app.logger.info('Prometheus metrics initialized')
        return metrics

    except ImportError:
        app.logger.warning('Prometheus exporter not installed, metrics disabled')
        return None
