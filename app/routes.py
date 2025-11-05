from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, abort
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, Research, Category, Tag, Bookmark, Comment
from app.forms import (LoginForm, RegistrationForm, ResearchForm, CategoryForm,
                      CommentForm, ProfileForm, AdvancedSearchForm)
from app.utils import (save_uploaded_file, format_citation, export_researches_csv,
                      export_researches_excel, export_researches_bibtex, export_researches_ris)
from sqlalchemy import or_, and_, func
from datetime import datetime
import os

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
    """แดชบอร์ดผู้ใช้ - AdminLTE Style"""
    # ดึงงานวิจัยของผู้ใช้
    user_researches = Research.query.filter_by(user_id=current_user.id)\
        .order_by(Research.created_at.desc()).all()

    # คำนวณสถิติต่างๆ
    stats = {
        'total_researches': len(user_researches),
        'total_bookmarks': Bookmark.query.filter_by(user_id=current_user.id).count(),
        'total_views': sum(r.view_count for r in user_researches),
        'total_downloads': sum(r.download_count for r in user_researches),
        'total_comments': Comment.query.filter_by(user_id=current_user.id).count(),
        'most_viewed': Research.query.filter_by(user_id=current_user.id)\
            .order_by(Research.view_count.desc()).first() if user_researches else None
    }

    return render_template('dashboard.html', researches=user_researches, stats=stats)


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
    """แสดงรายการงานวิจัยทั้งหมด พร้อมการค้นหาขั้นสูง"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    publication_type = request.args.get('publication_type', '')
    year_from = request.args.get('year_from', type=int)
    year_to = request.args.get('year_to', type=int)
    tags = request.args.get('tags', '')
    sort_by = request.args.get('sort_by', 'created_at')

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

    # กรองตามประเภทการตีพิมพ์
    if publication_type:
        query = query.filter_by(publication_type=publication_type)

    # กรองตามช่วงปี
    if year_from:
        query = query.filter(Research.year >= year_from)
    if year_to:
        query = query.filter(Research.year <= year_to)

    # กรองตามแท็ก
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        query = query.join(Research.tags).filter(Tag.name.in_(tag_list))

    # เรียงลำดับ
    if sort_by == 'created_at':
        query = query.order_by(Research.created_at.desc())
    elif sort_by == 'created_at_asc':
        query = query.order_by(Research.created_at.asc())
    elif sort_by == 'title':
        query = query.order_by(Research.title.asc())
    elif sort_by == 'year':
        query = query.order_by(Research.year.desc())
    elif sort_by == 'year_asc':
        query = query.order_by(Research.year.asc())
    elif sort_by == 'view_count':
        query = query.order_by(Research.view_count.desc())
    else:
        query = query.order_by(Research.created_at.desc())

    researches = query.paginate(page=page, per_page=10, error_out=False)

    categories = Category.query.all()

    # ตรวจสอบว่าผู้ใช้ได้บุ๊กมาร์กงานวิจัยใดบ้าง
    bookmarked_ids = []
    if current_user.is_authenticated:
        bookmarked_ids = [b.research_id for b in Bookmark.query.filter_by(user_id=current_user.id).all()]

    return render_template('research/list.html',
                         researches=researches,
                         categories=categories,
                         selected_category=category_id,
                         search=search,
                         publication_type=publication_type,
                         year_from=year_from,
                         year_to=year_to,
                         tags=tags,
                         sort_by=sort_by,
                         bookmarked_ids=bookmarked_ids)


@research_bp.route('/<int:id>', methods=['GET', 'POST'])
def view(id):
    """ดูรายละเอียดงานวิจัย พร้อมคอมเมนต์"""
    research = Research.query.get_or_404(id)

    # เพิ่มจำนวนการดู
    research.increment_view_count()

    # ฟอร์มคอมเมนต์
    comment_form = CommentForm()
    if comment_form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            content=comment_form.content.data,
            rating=comment_form.rating.data if comment_form.rating.data > 0 else None,
            user_id=current_user.id,
            research_id=research.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('เพิ่มความคิดเห็นสำเร็จ!', 'success')
        return redirect(url_for('research.view', id=id))

    # ดึงคอมเมนต์ทั้งหมด
    comments = Comment.query.filter_by(research_id=id).order_by(Comment.created_at.desc()).all()

    # คำนวณคะแนนเฉลี่ย
    ratings = [c.rating for c in comments if c.rating]
    avg_rating = sum(ratings) / len(ratings) if ratings else None

    # ตรวจสอบว่าผู้ใช้ได้บุ๊กมาร์กหรือยัง
    is_bookmarked = False
    if current_user.is_authenticated:
        is_bookmarked = Bookmark.query.filter_by(
            user_id=current_user.id,
            research_id=id
        ).first() is not None

    # จัดรูปแบบการอ้างอิง
    citations = {
        'apa': format_citation(research, 'apa'),
        'mla': format_citation(research, 'mla'),
        'chicago': format_citation(research, 'chicago'),
        'bibtex': format_citation(research, 'bibtex'),
    }

    return render_template('research/view.html',
                         research=research,
                         comment_form=comment_form,
                         comments=comments,
                         avg_rating=avg_rating,
                         is_bookmarked=is_bookmarked,
                         citations=citations)


@research_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """เพิ่มงานวิจัยใหม่"""
    form = ResearchForm()
    form.category_id.choices = [(0, 'ไม่ระบุ')] + [
        (c.id, c.name) for c in Category.query.all()
    ]

    if form.validate_on_submit():
        # จัดการไฟล์อัพโหลด
        file_path = form.file_path.data
        file_size = 0
        if form.pdf_file.data:
            filepath, filesize = save_uploaded_file(form.pdf_file.data)
            if filepath:
                file_path = filepath
                file_size = filesize

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
            file_path=file_path,
            file_size=file_size,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            user_id=current_user.id
        )
        db.session.add(research)

        # จัดการแท็ก
        if form.tags.data:
            tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                research.tags.append(tag)

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

    # Set default tags
    if request.method == 'GET':
        form.tags.data = ', '.join([tag.name for tag in research.tags])

    if form.validate_on_submit():
        # จัดการไฟล์อัพโหลด
        if form.pdf_file.data:
            filepath, filesize = save_uploaded_file(form.pdf_file.data)
            if filepath:
                # ลบไฟล์เก่า (ถ้ามี)
                if research.file_path and os.path.exists(research.file_path):
                    try:
                        os.remove(research.file_path)
                    except:
                        pass
                research.file_path = filepath
                research.file_size = filesize
        elif form.file_path.data:
            research.file_path = form.file_path.data

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
        research.category_id = form.category_id.data if form.category_id.data != 0 else None

        # จัดการแท็ก
        research.tags.clear()
        if form.tags.data:
            tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                research.tags.append(tag)

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


# ============================================
# Bookmark Routes
# ============================================

@research_bp.route('/<int:id>/bookmark/add', methods=['POST'])
@login_required
def add_bookmark(id):
    """เพิ่มบุ๊กมาร์ก"""
    research = Research.query.get_or_404(id)

    # ตรวจสอบว่ามีบุ๊กมาร์กอยู่แล้วหรือไม่
    existing = Bookmark.query.filter_by(user_id=current_user.id, research_id=id).first()
    if existing:
        flash('คุณได้บุ๊กมาร์กงานวิจัยนี้แล้ว', 'info')
    else:
        bookmark = Bookmark(user_id=current_user.id, research_id=id)
        db.session.add(bookmark)
        db.session.commit()
        flash('เพิ่มบุ๊กมาร์กสำเร็จ!', 'success')

    return redirect(request.referrer or url_for('research.view', id=id))


@research_bp.route('/<int:id>/bookmark/remove', methods=['POST'])
@login_required
def remove_bookmark(id):
    """ลบบุ๊กมาร์ก"""
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, research_id=id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        flash('ลบบุ๊กมาร์กสำเร็จ!', 'success')
    else:
        flash('ไม่พบบุ๊กมาร์ก', 'danger')

    return redirect(request.referrer or url_for('research.view', id=id))


@main_bp.route('/bookmarks')
@login_required
def bookmarks():
    """แสดงรายการบุ๊กมาร์กของผู้ใช้"""
    page = request.args.get('page', 1, type=int)
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id)\
        .order_by(Bookmark.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)

    return render_template('bookmarks.html', bookmarks=bookmarks)


# ============================================
# Export Routes
# ============================================

@research_bp.route('/export/csv')
def export_csv():
    """ส่งออกงานวิจัยเป็น CSV"""
    researches = Research.query.all()
    return export_researches_csv(researches)


@research_bp.route('/export/excel')
def export_excel():
    """ส่งออกงานวิจัยเป็น Excel"""
    researches = Research.query.all()
    return export_researches_excel(researches)


@research_bp.route('/export/bibtex')
def export_bibtex():
    """ส่งออกงานวิจัยเป็น BibTeX"""
    researches = Research.query.all()
    return export_researches_bibtex(researches)


@research_bp.route('/export/ris')
def export_ris():
    """ส่งออกงานวิจัยเป็น RIS"""
    researches = Research.query.all()
    return export_researches_ris(researches)


# ============================================
# File Download Routes
# ============================================

@research_bp.route('/<int:id>/download')
@login_required
def download_file(id):
    """ดาวน์โหลดไฟล์ PDF"""
    research = Research.query.get_or_404(id)

    if not research.file_path or not os.path.exists(research.file_path):
        flash('ไม่พบไฟล์ PDF', 'danger')
        return redirect(url_for('research.view', id=id))

    # เพิ่มจำนวนการดาวน์โหลด
    research.increment_download_count()

    return send_file(research.file_path, as_attachment=True)


# ============================================
# Analytics Dashboard
# ============================================

@main_bp.route('/analytics')
@login_required
def analytics():
    """แดชบอร์ดสถิติและวิเคราะห์"""
    # สถิติทั่วไป
    total_researches = Research.query.count()
    total_users = User.query.count()
    total_categories = Category.query.count()
    total_tags = Tag.query.count()
    total_bookmarks = Bookmark.query.count()
    total_comments = Comment.query.count()

    # สถิติตามประเภท
    pub_types = db.session.query(
        Research.publication_type,
        func.count(Research.id)
    ).group_by(Research.publication_type).all()

    # สถิติตามปี
    year_stats = db.session.query(
        Research.year,
        func.count(Research.id)
    ).filter(Research.year.isnot(None))\
     .group_by(Research.year)\
     .order_by(Research.year.desc())\
     .limit(10).all()

    # สถิติตามหมวดหมู่
    category_stats = db.session.query(
        Category.name,
        func.count(Research.id)
    ).join(Research, Category.id == Research.category_id)\
     .group_by(Category.name).all()

    # งานวิจัยยอดนิยม (ตามจำนวนการดู)
    popular_researches = Research.query.order_by(Research.view_count.desc()).limit(10).all()

    # งานวิจัยล่าสุด
    recent_researches = Research.query.order_by(Research.created_at.desc()).limit(10).all()

    # แท็กยอดนิยม
    popular_tags = db.session.query(
        Tag.name,
        func.count(Research.id)
    ).join(research_tags).join(Research)\
     .group_by(Tag.name)\
     .order_by(func.count(Research.id).desc())\
     .limit(10).all()

    # ผู้ใช้ที่มีงานวิจัยมากที่สุด
    top_contributors = db.session.query(
        User.full_name,
        User.username,
        func.count(Research.id)
    ).join(Research, User.id == Research.user_id)\
     .group_by(User.id)\
     .order_by(func.count(Research.id).desc())\
     .limit(10).all()

    return render_template('analytics.html',
                         total_researches=total_researches,
                         total_users=total_users,
                         total_categories=total_categories,
                         total_tags=total_tags,
                         total_bookmarks=total_bookmarks,
                         total_comments=total_comments,
                         pub_types=pub_types,
                         year_stats=year_stats,
                         category_stats=category_stats,
                         popular_researches=popular_researches,
                         recent_researches=recent_researches,
                         popular_tags=popular_tags,
                         top_contributors=top_contributors)


# ============================================
# User Profile Routes
# ============================================

@main_bp.route('/profile')
@login_required
def profile():
    """หน้าโปรไฟล์ผู้ใช้"""
    user_researches = Research.query.filter_by(user_id=current_user.id)\
        .order_by(Research.created_at.desc()).all()
    user_bookmarks = Bookmark.query.filter_by(user_id=current_user.id).count()
    user_comments = Comment.query.filter_by(user_id=current_user.id).count()

    return render_template('profile.html',
                         user_researches=user_researches,
                         user_bookmarks=user_bookmarks,
                         user_comments=user_comments)


@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """แก้ไขโปรไฟล์"""
    form = ProfileForm(original_email=current_user.email, obj=current_user)

    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.email_notifications = form.email_notifications.data

        # จัดการรูปโปรไฟล์
        if form.avatar.data:
            filepath, _ = save_uploaded_file(form.avatar.data, 'uploads/avatars')
            if filepath:
                # ลบรูปเก่า
                if current_user.avatar and os.path.exists(current_user.avatar):
                    try:
                        os.remove(current_user.avatar)
                    except:
                        pass
                current_user.avatar = filepath

        db.session.commit()
        flash('แก้ไขโปรไฟล์สำเร็จ!', 'success')
        return redirect(url_for('main.profile'))

    return render_template('edit_profile.html', form=form)


@main_bp.route('/user/<int:user_id>')
def user_profile(user_id):
    """ดูโปรไฟล์ผู้ใช้อื่น"""
    user = User.query.get_or_404(user_id)
    researches = Research.query.filter_by(user_id=user_id)\
        .order_by(Research.created_at.desc())\
        .limit(10).all()

    research_count = Research.query.filter_by(user_id=user_id).count()
    comment_count = Comment.query.filter_by(user_id=user_id).count()

    return render_template('user_profile.html',
                         user=user,
                         researches=researches,
                         research_count=research_count,
                         comment_count=comment_count)


# ============================================
# Tag Routes
# ============================================

@research_bp.route('/tags')
def tags():
    """แสดงรายการแท็กทั้งหมด"""
    all_tags = db.session.query(
        Tag.id,
        Tag.name,
        func.count(Research.id).label('count')
    ).join(research_tags, Tag.id == research_tags.c.tag_id, isouter=True)\
     .join(Research, Research.id == research_tags.c.research_id, isouter=True)\
     .group_by(Tag.id)\
     .order_by(func.count(Research.id).desc()).all()

    return render_template('research/tags.html', tags=all_tags)


@research_bp.route('/tag/<int:tag_id>')
def tag_researches(tag_id):
    """แสดงงานวิจัยตามแท็ก"""
    tag = Tag.query.get_or_404(tag_id)
    page = request.args.get('page', 1, type=int)

    researches = Research.query.join(Research.tags).filter(Tag.id == tag_id)\
        .order_by(Research.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)

    return render_template('research/tag_researches.html', tag=tag, researches=researches)


# ============================================
# Comment Management Routes
# ============================================

@research_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    """ลบคอมเมนต์"""
    comment = Comment.query.get_or_404(comment_id)

    # ตรวจสอบสิทธิ์
    if comment.user_id != current_user.id and not current_user.is_admin:
        flash('คุณไม่มีสิทธิ์ลบคอมเมนต์นี้', 'danger')
        return redirect(url_for('research.view', id=comment.research_id))

    research_id = comment.research_id
    db.session.delete(comment)
    db.session.commit()
    flash('ลบคอมเมนต์สำเร็จ!', 'success')

    return redirect(url_for('research.view', id=research_id))
