from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import or_
from app.models import db, Research, Category
from app.forms import ResearchForm
from app.utils import permission_required

research_bp = Blueprint('research', __name__)


@research_bp.route('/')
def list():
    """แสดงรายการงานวิจัยทั้งหมด - Frontend"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    year = request.args.get('year', type=int)
    pub_type = request.args.get('type', '')

    query = Research.query.filter_by(status='published')

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

    # กรองตามปี
    if year:
        query = query.filter_by(year=year)

    # กรองตามประเภท
    if pub_type:
        query = query.filter_by(publication_type=pub_type)

    researches = query.order_by(Research.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )

    categories = Category.query.filter_by(is_active=True)\
        .order_by(Category.display_order, Category.name).all()

    # ปีที่มีงานวิจัย
    years = db.session.query(Research.year).filter(Research.year.isnot(None), Research.status == 'published')\
        .distinct().order_by(Research.year.desc()).all()
    years = [y[0] for y in years]

    return render_template('frontend/research/list.html',
                         researches=researches,
                         categories=categories,
                         years=years,
                         selected_category=category_id,
                         selected_year=year,
                         selected_type=pub_type,
                         search=search)


@research_bp.route('/<int:id>')
def view(id):
    """ดูรายละเอียดงานวิจัย"""
    research = Research.query.get_or_404(id)

    # ตรวจสอบสถานะ - ถ้าไม่ใช่ published ต้อง login และเป็นเจ้าของหรือ admin
    if research.status != 'published':
        if not current_user.is_authenticated:
            abort(404)
        if research.user_id != current_user.id and not current_user.is_admin:
            abort(404)

    # เพิ่มจำนวนการดู
    research.increment_view()

    # งานวิจัยที่เกี่ยวข้อง
    related = []
    if research.category_id:
        related = Research.query.filter_by(category_id=research.category_id, status='published')\
            .filter(Research.id != id).limit(3).all()

    return render_template('frontend/research/view.html', research=research, related=related)


@research_bp.route('/my')
@login_required
def my_researches():
    """งานวิจัยของฉัน"""
    page = request.args.get('page', 1, type=int)
    researches = Research.query.filter_by(user_id=current_user.id)\
        .order_by(Research.created_at.desc()).paginate(page=page, per_page=10, error_out=False)

    return render_template('backend/research/my_list.html', researches=researches)


@research_bp.route('/add', methods=['GET', 'POST'])
@login_required
@permission_required('research.create')
def add():
    """เพิ่มงานวิจัยใหม่"""
    form = ResearchForm()
    form.category_id.choices = [(0, 'ไม่ระบุ')] + [
        (c.id, c.name) for c in Category.query.filter_by(is_active=True).all()
    ]

    if form.validate_on_submit():
        research = Research(
            title=form.title.data,
            title_en=form.title_en.data,
            authors=form.authors.data,
            abstract=form.abstract.data,
            abstract_en=form.abstract_en.data,
            keywords=form.keywords.data,
            year=form.year.data,
            publication_type=form.publication_type.data,
            journal_name=form.journal_name.data,
            volume=form.volume.data,
            issue=form.issue.data,
            pages=form.pages.data,
            doi=form.doi.data,
            isbn=form.isbn.data,
            url=form.url.data,
            file_path=form.file_path.data,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(research)
        db.session.commit()
        flash('เพิ่มงานวิจัยสำเร็จ!', 'success')
        return redirect(url_for('research.view', id=research.id))

    return render_template('backend/research/form.html', form=form, title='เพิ่มงานวิจัย')


@research_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    """แก้ไขงานวิจัย"""
    research = Research.query.get_or_404(id)

    # ตรวจสอบสิทธิ์
    if research.user_id != current_user.id and not current_user.has_permission('research.update'):
        flash('คุณไม่มีสิทธิ์แก้ไขงานวิจัยนี้', 'danger')
        return redirect(url_for('research.view', id=id))

    form = ResearchForm(obj=research)
    form.category_id.choices = [(0, 'ไม่ระบุ')] + [
        (c.id, c.name) for c in Category.query.filter_by(is_active=True).all()
    ]

    if form.validate_on_submit():
        research.title = form.title.data
        research.title_en = form.title_en.data
        research.authors = form.authors.data
        research.abstract = form.abstract.data
        research.abstract_en = form.abstract_en.data
        research.keywords = form.keywords.data
        research.year = form.year.data
        research.publication_type = form.publication_type.data
        research.journal_name = form.journal_name.data
        research.volume = form.volume.data
        research.issue = form.issue.data
        research.pages = form.pages.data
        research.doi = form.doi.data
        research.isbn = form.isbn.data
        research.url = form.url.data
        research.file_path = form.file_path.data
        research.category_id = form.category_id.data if form.category_id.data != 0 else None
        research.status = form.status.data

        db.session.commit()
        flash('แก้ไขงานวิจัยสำเร็จ!', 'success')
        return redirect(url_for('research.view', id=research.id))

    return render_template('backend/research/form.html', form=form, title='แก้ไขงานวิจัย', research=research)


@research_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    """ลบงานวิจัย"""
    research = Research.query.get_or_404(id)

    # ตรวจสอบสิทธิ์
    if research.user_id != current_user.id and not current_user.has_permission('research.delete'):
        flash('คุณไม่มีสิทธิ์ลบงานวิจัยนี้', 'danger')
        return redirect(url_for('research.view', id=id))

    db.session.delete(research)
    db.session.commit()
    flash('ลบงานวิจัยสำเร็จ!', 'success')
    return redirect(url_for('research.my_researches'))


@research_bp.route('/categories')
def categories():
    """แสดงรายการหมวดหมู่"""
    categories = Category.query.filter_by(is_active=True)\
        .order_by(Category.display_order, Category.name).all()
    return render_template('frontend/categories.html', categories=categories)
