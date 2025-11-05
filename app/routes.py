from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Research, Category
from app.forms import LoginForm, RegistrationForm, ResearchForm, CategoryForm
from sqlalchemy import or_

# Blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
research_bp = Blueprint('research', __name__)


# ============================================
# Main Routes
# ============================================

@main_bp.route('/')
def index():
    """หน้าแรก"""
    recent_researches = Research.query.order_by(Research.created_at.desc()).limit(5).all()
    total_researches = Research.query.count()
    total_categories = Category.query.count()
    return render_template('index.html',
                         recent_researches=recent_researches,
                         total_researches=total_researches,
                         total_categories=total_categories)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """แดชบอร์ดผู้ใช้"""
    user_researches = Research.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', researches=user_researches)


# ============================================
# Authentication Routes
# ============================================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """ลงทะเบียนผู้ใช้ใหม่"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('ลงทะเบียนสำเร็จ! กรุณาเข้าสู่ระบบ', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """เข้าสู่ระบบ"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('เข้าสู่ระบบสำเร็จ!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
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


# ============================================
# Research Routes
# ============================================

@research_bp.route('/')
def list():
    """แสดงรายการงานวิจัยทั้งหมด"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')

    query = Research.query

    # ค้นหา
    if search:
        query = query.filter(
            or_(
                Research.title.contains(search),
                Research.title_en.contains(search),
                Research.authors.contains(search),
                Research.keywords.contains(search)
            )
        )

    # กรองตามหมวดหมู่
    if category_id:
        query = query.filter_by(category_id=category_id)

    researches = query.order_by(Research.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    categories = Category.query.all()
    return render_template('research/list.html',
                         researches=researches,
                         categories=categories,
                         selected_category=category_id,
                         search=search)


@research_bp.route('/<int:id>')
def view(id):
    """ดูรายละเอียดงานวิจัย"""
    research = Research.query.get_or_404(id)
    return render_template('research/view.html', research=research)


@research_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """เพิ่มงานวิจัยใหม่"""
    form = ResearchForm()
    form.category_id.choices = [(0, 'ไม่ระบุ')] + [
        (c.id, c.name) for c in Category.query.all()
    ]

    if form.validate_on_submit():
        research = Research(
            title=form.title.data,
            title_en=form.title_en.data,
            authors=form.authors.data,
            abstract=form.abstract.data,
            keywords=form.keywords.data,
            year=form.year.data,
            publication_type=form.publication_type.data,
            journal_name=form.journal_name.data,
            volume=form.volume.data,
            issue=form.issue.data,
            pages=form.pages.data,
            doi=form.doi.data,
            url=form.url.data,
            file_path=form.file_path.data,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            user_id=current_user.id
        )
        db.session.add(research)
        db.session.commit()
        flash('เพิ่มงานวิจัยสำเร็จ!', 'success')
        return redirect(url_for('research.view', id=research.id))

    return render_template('research/form.html', form=form, title='เพิ่มงานวิจัย')


@research_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """แก้ไขงานวิจัย"""
    research = Research.query.get_or_404(id)

    # ตรวจสอบสิทธิ์
    if research.user_id != current_user.id and not current_user.is_admin:
        flash('คุณไม่มีสิทธิ์แก้ไขงานวิจัยนี้', 'danger')
        return redirect(url_for('research.view', id=id))

    form = ResearchForm(obj=research)
    form.category_id.choices = [(0, 'ไม่ระบุ')] + [
        (c.id, c.name) for c in Category.query.all()
    ]

    if form.validate_on_submit():
        research.title = form.title.data
        research.title_en = form.title_en.data
        research.authors = form.authors.data
        research.abstract = form.abstract.data
        research.keywords = form.keywords.data
        research.year = form.year.data
        research.publication_type = form.publication_type.data
        research.journal_name = form.journal_name.data
        research.volume = form.volume.data
        research.issue = form.issue.data
        research.pages = form.pages.data
        research.doi = form.doi.data
        research.url = form.url.data
        research.file_path = form.file_path.data
        research.category_id = form.category_id.data if form.category_id.data != 0 else None

        db.session.commit()
        flash('แก้ไขงานวิจัยสำเร็จ!', 'success')
        return redirect(url_for('research.view', id=research.id))

    return render_template('research/form.html', form=form, title='แก้ไขงานวิจัย', research=research)


@research_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """ลบงานวิจัย"""
    research = Research.query.get_or_404(id)

    # ตรวจสอบสิทธิ์
    if research.user_id != current_user.id and not current_user.is_admin:
        flash('คุณไม่มีสิทธิ์ลบงานวิจัยนี้', 'danger')
        return redirect(url_for('research.view', id=id))

    db.session.delete(research)
    db.session.commit()
    flash('ลบงานวิจัยสำเร็จ!', 'success')
    return redirect(url_for('research.list'))


# ============================================
# Category Routes
# ============================================

@research_bp.route('/categories')
def categories():
    """แสดงรายการหมวดหมู่"""
    categories = Category.query.all()
    return render_template('research/categories.html', categories=categories)


@research_bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """เพิ่มหมวดหมู่ใหม่"""
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(category)
        db.session.commit()
        flash('เพิ่มหมวดหมู่สำเร็จ!', 'success')
        return redirect(url_for('research.categories'))

    return render_template('research/category_form.html', form=form, title='เพิ่มหมวดหมู่')
