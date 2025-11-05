from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app.models import db, User, Role
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """ลงทะเบียนผู้ใช้ใหม่"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('research.my_researches'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            department=form.department.data,
            position=form.position.data
        )
        user.set_password(form.password.data)

        # กำหนด Role เริ่มต้นเป็น viewer
        viewer_role = Role.query.filter_by(name='viewer').first()
        if viewer_role:
            user.add_role(viewer_role)

        db.session.add(user)
        db.session.commit()
        flash('ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """เข้าสู่ระบบ"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('research.my_researches'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
                flash('บัญชีของคุณถูกระงับการใช้งาน กรุณาติดต่อผู้ดูแลระบบ', 'danger')
                return redirect(url_for('auth.login'))

            user.last_login = datetime.utcnow()
            db.session.commit()

            login_user(user)
            flash(f'ยินดีต้อนรับ {user.full_name}!', 'success')

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            # Redirect based on role
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('research.my_researches'))
        else:
            flash('ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """ออกจากระบบ"""
    logout_user()
    flash('ออกจากระบบแล้ว', 'info')
    return redirect(url_for('main.index'))
