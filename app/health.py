"""
Health check endpoint for monitoring
"""
from flask import Blueprint, jsonify, current_app
from app.models import db
import redis
from datetime import datetime

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and load balancers

    Returns JSON with status of various components:
    - overall status
    - database connectivity
    - redis connectivity
    - timestamp
    """
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': {}
    }

    # Check database
    try:
        db.session.execute('SELECT 1')
        health_status['checks']['database'] = 'healthy'
    except Exception as e:
        health_status['checks']['database'] = f'unhealthy: {str(e)}'
        health_status['status'] = 'unhealthy'

    # Check Redis (if configured)
    if current_app.config.get('REDIS_URL'):
        try:
            redis_url = current_app.config['REDIS_URL']
            r = redis.from_url(redis_url)
            r.ping()
            health_status['checks']['redis'] = 'healthy'
        except Exception as e:
            health_status['checks']['redis'] = f'unhealthy: {str(e)}'
            # Redis is optional, don't mark overall as unhealthy
            # health_status['status'] = 'unhealthy'

    status_code = 200 if health_status['status'] == 'healthy' else 503
    return jsonify(health_status), status_code


@health_bp.route('/health/liveness', methods=['GET'])
def liveness():
    """Kubernetes liveness probe - is the app running?"""
    return jsonify({'status': 'alive'}), 200


@health_bp.route('/health/readiness', methods=['GET'])
def readiness():
    """Kubernetes readiness probe - is the app ready to serve traffic?"""
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'ready'}), 200
    except:
        return jsonify({'status': 'not ready'}), 503
