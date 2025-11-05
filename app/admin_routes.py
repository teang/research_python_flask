"""
Admin Routes - จัดการเส้นทางสำหรับแผงผู้ดูแลระบบ
"""
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func
import os

from app.models import db, User, Role, Permission, Research, Category, Comment, Bookmark, AuditLog

# สร้าง Blueprint สำหรับ Admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator สำหรับตรวจสอบสิทธิ์ผู้ดูแลระบบ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('กรุณาเข้าสู่ระบบก่อน', 'warning')
            return redirect(url_for('auth.login'))

        # ตรวจสอบว่าเป็น admin หรือมีบทบาท admin
        if not current_user.is_admin and not current_user.has_role('admin'):
            flash('คุณไม่มีสิทธิ์เข้าถึงหน้านี้', 'danger')
            return redirect(url_for('main.index'))

        return f(*args, **kwargs)
    return decorated_function


def log_action(action, resource_type=None, resource_id=None, details=None):
    """บันทึกการกระทำของผู้ใช้"""
    try:
        log = AuditLog(
            user_id=current_user.id if current_user.is_authenticated else None,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging action: {e}")


# ==================== Dashboard ====================
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """หน้า Dashboard หลักของ Admin"""
    # สถิติทั่วไป
    stats = {
        'total_users': User.query.count(),
        'total_researches': Research.query.count(),
        'total_comments': Comment.query.count(),
        'total_downloads': db.session.query(func.sum(Research.download_count)).scalar() or 0,
        'new_users_week': User.query.filter(
            User.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count(),
        'new_researches_week': Research.query.filter(
            Research.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count(),
        'new_comments_week': Comment.query.filter(
            Comment.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count(),
        'storage_used': '125 MB'  # TODO: คำนวณจริง
    }

    # งานวิจัยล่าสุด
    recent_researches = Research.query.order_by(Research.created_at.desc()).limit(5).all()

    # หมวดหมู่ยอดนิยม
    popular_categories = db.session.query(
        Category,
        func.count(Research.id).label('research_count')
    ).join(Research).group_by(Category.id).order_by(
        func.count(Research.id).desc()
    ).limit(5).all()

    # กิจกรรมล่าสุด
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()

    log_action('view_admin_dashboard', 'Dashboard', None)

    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_researches=recent_researches,
                         popular_categories=popular_categories,
                         recent_logs=recent_logs,
                         current_time=datetime.utcnow().strftime('%d/%m/%Y %H:%M'))


# ==================== User Management ====================
@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """หน้ารายชื่อผู้ใช้ทั้งหมด"""
    users_list = User.query.order_by(User.created_at.desc()).all()
    all_roles = Role.query.all()

    # สถิติ
    new_users_count = User.query.filter(
        User.created_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    admin_count = User.query.filter(User.is_admin == True).count()
    online_count = 0  # TODO: implement online tracking

    log_action('view_users_list', 'User', None)

    return render_template('admin/users.html',
                         users=users_list,
                         all_roles=all_roles,
                         new_users_count=new_users_count,
                         admin_count=admin_count,
                         online_count=online_count)


@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def user_create():
    """สร้างผู้ใช้ใหม่"""
    from app.forms import AdminUserForm

    form = AdminUserForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            bio=form.bio.data,
            is_admin=form.is_admin.data,
            email_notifications=form.email_notifications.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        log_action('create_user', 'User', user.id, f"Created user: {user.username}")

        flash(f'สร้างผู้ใช้ {user.username} สำเร็จ', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_form.html', form=form, user=None)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    """แก้ไขข้อมูลผู้ใช้"""
    from app.forms import AdminUserForm, PasswordChangeForm

    user = User.query.get_or_404(user_id)
    form = AdminUserForm(obj=user)
    password_form = PasswordChangeForm()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.full_name = form.full_name.data
        user.bio = form.bio.data
        user.is_admin = form.is_admin.data
        user.email_notifications = form.email_notifications.data

        db.session.commit()

        log_action('update_user', 'User', user.id, f"Updated user: {user.username}")

        flash(f'อัปเดตข้อมูลผู้ใช้ {user.username} สำเร็จ', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/user_form.html',
                         form=form,
                         password_form=password_form,
                         user=user)


@admin_bp.route('/users/<int:user_id>/change-password', methods=['POST'])
@login_required
@admin_required
def user_change_password(user_id):
    """เปลี่ยนรหัสผ่านผู้ใช้"""
    from app.forms import PasswordChangeForm

    user = User.query.get_or_404(user_id)
    form = PasswordChangeForm()

    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()

        log_action('change_user_password', 'User', user.id, f"Changed password for: {user.username}")

        flash(f'เปลี่ยนรหัสผ่านของ {user.username} สำเร็จ', 'success')

    return redirect(url_for('admin.user_edit', user_id=user_id))


@admin_bp.route('/users/<int:user_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def user_delete(user_id):
    """ลบผู้ใช้"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'message': 'ไม่สามารถลบตัวเองได้'}), 400

    user = User.query.get_or_404(user_id)
    username = user.username

    log_action('delete_user', 'User', user.id, f"Deleted user: {username}")

    db.session.delete(user)
    db.session.commit()

    return jsonify({'success': True, 'message': f'ลบผู้ใช้ {username} สำเร็จ'})


@admin_bp.route('/users/<int:user_id>/permissions')
@login_required
@admin_required
def user_permissions(user_id):
    """จัดการสิทธิ์ของผู้ใช้"""
    user = User.query.get_or_404(user_id)
    all_roles = Role.query.all()

    log_action('view_user_permissions', 'User', user.id)

    return render_template('admin/user_permissions.html',
                         user=user,
                         all_roles=all_roles)


# ==================== Role Management ====================
@admin_bp.route('/roles')
@login_required
@admin_required
def roles():
    """หน้ารายการบทบาททั้งหมด"""
    roles_list = Role.query.order_by(Role.created_at.desc()).all()
    total_permissions = Permission.query.count()

    log_action('view_roles_list', 'Role', None)

    return render_template('admin/roles.html',
                         roles=roles_list,
                         total_permissions=total_permissions)


@admin_bp.route('/roles/create', methods=['POST'])
@login_required
@admin_required
def role_create():
    """สร้างบทบาทใหม่"""
    name = request.form.get('name')
    display_name = request.form.get('display_name')
    description = request.form.get('description')

    if not name:
        flash('กรุณากรอกชื่อบทบาท', 'danger')
        return redirect(url_for('admin.roles'))

    # ตรวจสอบว่ามีอยู่แล้วหรือไม่
    if Role.query.filter_by(name=name).first():
        flash(f'บทบาท {name} มีอยู่แล้ว', 'danger')
        return redirect(url_for('admin.roles'))

    role = Role(
        name=name,
        display_name=display_name,
        description=description
    )

    db.session.add(role)
    db.session.commit()

    log_action('create_role', 'Role', role.id, f"Created role: {role.name}")

    flash(f'สร้างบทบาท {name} สำเร็จ', 'success')
    return redirect(url_for('admin.roles'))


@admin_bp.route('/roles/<int:role_id>/edit', methods=['POST'])
@login_required
@admin_required
def role_edit(role_id):
    """แก้ไขบทบาท"""
    role = Role.query.get_or_404(role_id)

    role.name = request.form.get('name')
    role.display_name = request.form.get('display_name')
    role.description = request.form.get('description')

    db.session.commit()

    log_action('update_role', 'Role', role.id, f"Updated role: {role.name}")

    flash(f'อัปเดตบทบาท {role.name} สำเร็จ', 'success')
    return redirect(url_for('admin.roles'))


@admin_bp.route('/roles/<int:role_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def role_delete(role_id):
    """ลบบทบาท"""
    role = Role.query.get_or_404(role_id)

    # ตรวจสอบว่ามีผู้ใช้หรือไม่
    if len(role.users) > 0:
        return jsonify({
            'success': False,
            'message': f'ไม่สามารถลบได้ เนื่องจากมีผู้ใช้ {len(role.users)} คนใช้บทบาทนี้'
        }), 400

    role_name = role.name

    log_action('delete_role', 'Role', role.id, f"Deleted role: {role_name}")

    db.session.delete(role)
    db.session.commit()

    return jsonify({'success': True, 'message': f'ลบบทบาท {role_name} สำเร็จ'})


@admin_bp.route('/roles/<int:role_id>/permissions')
@login_required
@admin_required
def role_permissions(role_id):
    """จัดการสิทธิ์ของบทบาท"""
    role = Role.query.get_or_404(role_id)
    all_permissions = Permission.query.order_by(Permission.category, Permission.name).all()

    log_action('view_role_permissions', 'Role', role.id)

    return render_template('admin/role_permissions.html',
                         role=role,
                         all_permissions=all_permissions)


# ==================== Permission Management ====================
@admin_bp.route('/permissions')
@login_required
@admin_required
def permissions():
    """หน้ารายการสิทธิ์ทั้งหมด"""
    permissions_list = Permission.query.order_by(Permission.category, Permission.name).all()

    # นับหมวดหมู่
    categories_count = db.session.query(
        func.count(func.distinct(Permission.category))
    ).scalar()

    log_action('view_permissions_list', 'Permission', None)

    return render_template('admin/permissions.html',
                         permissions=permissions_list,
                         categories_count=categories_count)


@admin_bp.route('/permissions/create', methods=['POST'])
@login_required
@admin_required
def permission_create():
    """สร้างสิทธิ์ใหม่"""
    name = request.form.get('name')
    display_name = request.form.get('display_name')
    category = request.form.get('category')
    description = request.form.get('description')

    if not name or not category:
        flash('กรุณากรอกชื่อสิทธิ์และหมวดหมู่', 'danger')
        return redirect(url_for('admin.permissions'))

    # ตรวจสอบว่ามีอยู่แล้วหรือไม่
    if Permission.query.filter_by(name=name).first():
        flash(f'สิทธิ์ {name} มีอยู่แล้ว', 'danger')
        return redirect(url_for('admin.permissions'))

    permission = Permission(
        name=name,
        display_name=display_name,
        category=category,
        description=description
    )

    db.session.add(permission)
    db.session.commit()

    log_action('create_permission', 'Permission', permission.id, f"Created permission: {permission.name}")

    flash(f'สร้างสิทธิ์ {name} สำเร็จ', 'success')
    return redirect(url_for('admin.permissions'))


@admin_bp.route('/permissions/<int:permission_id>/edit', methods=['POST'])
@login_required
@admin_required
def permission_edit(permission_id):
    """แก้ไขสิทธิ์"""
    permission = Permission.query.get_or_404(permission_id)

    permission.name = request.form.get('name')
    permission.display_name = request.form.get('display_name')
    permission.category = request.form.get('category')
    permission.description = request.form.get('description')

    db.session.commit()

    log_action('update_permission', 'Permission', permission.id, f"Updated permission: {permission.name}")

    flash(f'อัปเดตสิทธิ์ {permission.name} สำเร็จ', 'success')
    return redirect(url_for('admin.permissions'))


@admin_bp.route('/permissions/<int:permission_id>/delete', methods=['DELETE'])
@login_required
@admin_required
def permission_delete(permission_id):
    """ลบสิทธิ์"""
    permission = Permission.query.get_or_404(permission_id)
    permission_name = permission.name

    log_action('delete_permission', 'Permission', permission.id, f"Deleted permission: {permission_name}")

    db.session.delete(permission)
    db.session.commit()

    return jsonify({'success': True, 'message': f'ลบสิทธิ์ {permission_name} สำเร็จ'})


# ==================== Research Management ====================
@admin_bp.route('/researches')
@login_required
@admin_required
def researches():
    """หน้ารายการงานวิจัยทั้งหมด"""
    researches_list = Research.query.order_by(Research.created_at.desc()).all()

    log_action('view_researches_list', 'Research', None)

    return render_template('admin/researches.html', researches=researches_list)


@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """หน้ารายการหมวดหมู่ทั้งหมด"""
    categories_list = Category.query.all()

    log_action('view_categories_list', 'Category', None)

    return render_template('admin/categories.html', categories=categories_list)


@admin_bp.route('/comments')
@login_required
@admin_required
def comments():
    """หน้ารายการความคิดเห็นทั้งหมด"""
    comments_list = Comment.query.order_by(Comment.created_at.desc()).all()

    log_action('view_comments_list', 'Comment', None)

    return render_template('admin/comments.html', comments=comments_list)


# ==================== System ====================
@admin_bp.route('/audit-logs')
@login_required
@admin_required
def audit_logs():
    """หน้าบันทึกการใช้งาน"""
    user_id = request.args.get('user_id', type=int)

    query = AuditLog.query
    if user_id:
        query = query.filter_by(user_id=user_id)

    logs = query.order_by(AuditLog.created_at.desc()).limit(100).all()

    return render_template('admin/audit_logs.html', logs=logs)


@admin_bp.route('/settings')
@login_required
@admin_required
def settings():
    """หน้าตั้งค่าระบบ"""
    log_action('view_settings', 'Settings', None)

    return render_template('admin/settings.html')
