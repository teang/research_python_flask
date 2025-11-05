from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from app.models import db, User, Role, Permission, Research, Category
from app.forms import UserForm, UserEditForm, CategoryForm
from app.utils import role_required, permission_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    """แดชบอร์ดผู้ดูแลระบบ"""
    # สถิติทั่วไป
    total_users = User.query.count()
    total_researches = Research.query.count()
    total_categories = Category.query.count()
    published_researches = Research.query.filter_by(status='published').count()

    # งานวิจัยล่าสุด
    recent_researches = Research.query.order_by(Research.created_at.desc()).limit(5).all()

    # ผู้ใช้ใหม่
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    # สถิติการเข้าชม (Top 5)
    popular_researches = Research.query.order_by(Research.view_count.desc()).limit(5).all()

    # สถิติตามหมวดหมู่
    category_stats = db.session.query(
        Category.name,
        func.count(Research.id).label('count')
    ).outerjoin(Research).group_by(Category.id, Category.name).all()

    # สถิติตามเดือน (6 เดือนล่าสุด)
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    monthly_stats = db.session.query(
        extract('year', Research.created_at).label('year'),
        extract('month', Research.created_at).label('month'),
        func.count(Research.id).label('count')
    ).filter(Research.created_at >= six_months_ago)\
     .group_by('year', 'month')\
     .order_by('year', 'month').all()

    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_researches=total_researches,
                         total_categories=total_categories,
                         published_researches=published_researches,
                         recent_researches=recent_researches,
                         recent_users=recent_users,
                         popular_researches=popular_researches,
                         category_stats=category_stats,
                         monthly_stats=monthly_stats)


# ============================================
# User Management
# ============================================

@admin_bp.route('/users')
@login_required
@role_required('admin')
def users():
    """จัดการผู้ใช้"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = User.query

    if search:
        query = query.filter(
            (User.username.contains(search)) |
            (User.email.contains(search)) |
            (User.full_name.contains(search))
        )

    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/users/list.html', users=users, search=search)


@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_user():
    """เพิ่มผู้ใช้"""
    form = UserForm()
    form.roles.choices = [(r.id, r.name_th) for r in Role.query.all()]

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            department=form.department.data,
            position=form.position.data,
            is_active=form.is_active.data
        )
        user.set_password(form.password.data)

        # กำหนด Roles
        for role_id in form.roles.data:
            role = Role.query.get(role_id)
            if role:
                user.add_role(role)

        db.session.add(user)
        db.session.commit()
        flash('เพิ่มผู้ใช้สำเร็จ!', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/users/form.html', form=form, title='เพิ่มผู้ใช้')


@admin_bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_user(id):
    """แก้ไขผู้ใช้"""
    user = User.query.get_or_404(id)
    form = UserEditForm(user.username, user.email, obj=user)
    form.roles.choices = [(r.id, r.name_th) for r in Role.query.all()]

    if request.method == 'GET':
        form.roles.data = [r.id for r in user.roles]

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.full_name = form.full_name.data
        user.phone = form.phone.data
        user.department = form.department.data
        user.position = form.position.data
        user.is_active = form.is_active.data

        # อัพเดทรหัสผ่าน (ถ้ามี)
        if form.password.data:
            user.set_password(form.password.data)

        # อัพเดท Roles
        user.roles = []
        for role_id in form.roles.data:
            role = Role.query.get(role_id)
            if role:
                user.add_role(role)

        db.session.commit()
        flash('แก้ไขข้อมูลผู้ใช้สำเร็จ!', 'success')
        return redirect(url_for('admin.users'))

    return render_template('admin/users/form.html', form=form, title='แก้ไขผู้ใช้', user=user)


@admin_bp.route('/users/<int:id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(id):
    """ลบผู้ใช้"""
    user = User.query.get_or_404(id)

    if user.id == current_user.id:
        flash('ไม่สามารถลบบัญชีของตนเองได้', 'danger')
        return redirect(url_for('admin.users'))

    db.session.delete(user)
    db.session.commit()
    flash('ลบผู้ใช้สำเร็จ!', 'success')
    return redirect(url_for('admin.users'))


# ============================================
# Research Management
# ============================================

@admin_bp.route('/researches')
@login_required
@role_required('admin')
def researches():
    """จัดการงานวิจัย"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    search = request.args.get('search', '')

    query = Research.query

    if status:
        query = query.filter_by(status=status)

    if search:
        query = query.filter(
            (Research.title.contains(search)) |
            (Research.authors.contains(search))
        )

    researches = query.order_by(Research.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/researches/list.html',
                         researches=researches,
                         selected_status=status,
                         search=search)


@admin_bp.route('/researches/<int:id>/toggle-featured', methods=['POST'])
@login_required
@role_required('admin')
def toggle_featured(id):
    """สลับสถานะงานวิจัยแนะนำ"""
    research = Research.query.get_or_404(id)
    research.is_featured = not research.is_featured
    db.session.commit()

    status = 'เป็นงานวิจัยแนะนำแล้ว' if research.is_featured else 'ยกเลิกการเป็นงานวิจัยแนะนำแล้ว'
    flash(f'{status}', 'success')
    return redirect(request.referrer or url_for('admin.researches'))


# ============================================
# Category Management
# ============================================

@admin_bp.route('/categories')
@login_required
@role_required('admin')
def categories():
    """จัดการหมวดหมู่"""
    categories = Category.query.order_by(Category.display_order, Category.name).all()
    return render_template('admin/categories/list.html', categories=categories)


@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_category():
    """เพิ่มหมวดหมู่"""
    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            name_en=form.name_en.data,
            description=form.description.data,
            icon=form.icon.data,
            color=form.color.data,
            display_order=form.display_order.data,
            is_active=form.is_active.data
        )
        db.session.add(category)
        db.session.commit()
        flash('เพิ่มหมวดหมู่สำเร็จ!', 'success')
        return redirect(url_for('admin.categories'))

    return render_template('admin/categories/form.html', form=form, title='เพิ่มหมวดหมู่')


@admin_bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_category(id):
    """แก้ไขหมวดหมู่"""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        category.name = form.name.data
        category.name_en = form.name_en.data
        category.description = form.description.data
        category.icon = form.icon.data
        category.color = form.color.data
        category.display_order = form.display_order.data
        category.is_active = form.is_active.data

        db.session.commit()
        flash('แก้ไขหมวดหมู่สำเร็จ!', 'success')
        return redirect(url_for('admin.categories'))

    return render_template('admin/categories/form.html', form=form, title='แก้ไขหมวดหมู่', category=category)


@admin_bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_category(id):
    """ลบหมวดหมู่"""
    category = Category.query.get_or_404(id)

    if category.researches:
        flash('ไม่สามารถลบหมวดหมู่ที่มีงานวิจัยอยู่ได้', 'danger')
        return redirect(url_for('admin.categories'))

    db.session.delete(category)
    db.session.commit()
    flash('ลบหมวดหมู่สำเร็จ!', 'success')
    return redirect(url_for('admin.categories'))


# ============================================
# Role & Permission Management
# ============================================

@admin_bp.route('/roles')
@login_required
@role_required('admin')
def roles():
    """จัดการบทบาท"""
    roles = Role.query.all()
    return render_template('admin/roles/list.html', roles=roles)


@admin_bp.route('/roles/<int:id>')
@login_required
@role_required('admin')
def view_role(id):
    """ดูรายละเอียดบทบาท"""
    role = Role.query.get_or_404(id)
    permissions = Permission.query.all()
    return render_template('admin/roles/view.html', role=role, permissions=permissions)
