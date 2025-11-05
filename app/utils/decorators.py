from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def permission_required(permission_name):
    """
    Decorator สำหรับตรวจสอบสิทธิ์ Permission

    Usage:
        @permission_required('research.create')
        def add_research():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('กรุณาเข้าสู่ระบบก่อน', 'warning')
                return redirect(url_for('auth.login'))

            if not current_user.has_permission(permission_name):
                flash('คุณไม่มีสิทธิ์เข้าถึงหน้านี้', 'danger')
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def role_required(role_name):
    """
    Decorator สำหรับตรวจสอบบทบาท Role

    Usage:
        @role_required('admin')
        def admin_dashboard():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('กรุณาเข้าสู่ระบบก่อน', 'warning')
                return redirect(url_for('auth.login'))

            if not current_user.has_role(role_name):
                flash('คุณไม่มีสิทธิ์เข้าถึงหน้านี้', 'danger')
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
