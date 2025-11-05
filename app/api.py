"""REST API endpoints for the research management system"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Research, Category, User, Tag, Bookmark, Comment
from sqlalchemy import or_

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


# ============================================
# Helper Functions
# ============================================

def research_to_dict(research, include_full=False):
    """แปลง Research object เป็น dictionary"""
    data = {
        'id': research.id,
        'title': research.title,
        'title_en': research.title_en,
        'authors': research.authors,
        'year': research.year,
        'publication_type': research.publication_type,
        'view_count': research.view_count,
        'download_count': research.download_count,
        'created_at': research.created_at.isoformat() if research.created_at else None,
        'updated_at': research.updated_at.isoformat() if research.updated_at else None,
    }

    if include_full:
        data.update({
            'abstract': research.abstract,
            'keywords': research.keywords,
            'journal_name': research.journal_name,
            'volume': research.volume,
            'issue': research.issue,
            'pages': research.pages,
            'doi': research.doi,
            'url': research.url,
            'file_path': research.file_path,
            'category': {
                'id': research.category.id,
                'name': research.category.name
            } if research.category else None,
            'uploader': {
                'id': research.uploader.id,
                'username': research.uploader.username,
                'full_name': research.uploader.full_name
            } if research.uploader else None,
            'tags': [{'id': tag.id, 'name': tag.name} for tag in research.tags],
            'comments_count': len(research.comments)
        })

    return data


# ============================================
# Research API Endpoints
# ============================================

@api_bp.route('/researches', methods=['GET'])
def get_researches():
    """ดึงรายการงานวิจัยทั้งหมด

    Query Parameters:
        - page: หน้าที่ต้องการ (default: 1)
        - per_page: จำนวนต่อหน้า (default: 10, max: 100)
        - search: คำค้นหา
        - category_id: ID หมวดหมู่
        - publication_type: ประเภทการตีพิมพ์
        - year: ปีที่เผยแพร่
        - sort_by: เรียงลำดับตาม (created_at, title, year, view_count)
        - order: ASC หรือ DESC
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    search = request.args.get('search', '')
    category_id = request.args.get('category_id', type=int)
    publication_type = request.args.get('publication_type', '')
    year = request.args.get('year', type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'DESC').upper()

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

    # กรองตามประเภท
    if publication_type:
        query = query.filter_by(publication_type=publication_type)

    # กรองตามปี
    if year:
        query = query.filter_by(year=year)

    # เรียงลำดับ
    sort_column = getattr(Research, sort_by, Research.created_at)
    if order == 'DESC':
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'success': True,
        'data': [research_to_dict(r) for r in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    })


@api_bp.route('/researches/<int:id>', methods=['GET'])
def get_research(id):
    """ดึงข้อมูลงานวิจัยตาม ID"""
    research = Research.query.get_or_404(id)

    # เพิ่มจำนวนการดู
    research.increment_view_count()

    return jsonify({
        'success': True,
        'data': research_to_dict(research, include_full=True)
    })


@api_bp.route('/researches', methods=['POST'])
@login_required
def create_research():
    """สร้างงานวิจัยใหม่"""
    data = request.get_json()

    if not data or not data.get('title') or not data.get('authors'):
        return jsonify({
            'success': False,
            'error': 'กรุณาระบุชื่อและผู้แต่ง'
        }), 400

    research = Research(
        title=data.get('title'),
        title_en=data.get('title_en'),
        authors=data.get('authors'),
        abstract=data.get('abstract'),
        keywords=data.get('keywords'),
        year=data.get('year'),
        publication_type=data.get('publication_type'),
        journal_name=data.get('journal_name'),
        volume=data.get('volume'),
        issue=data.get('issue'),
        pages=data.get('pages'),
        doi=data.get('doi'),
        url=data.get('url'),
        category_id=data.get('category_id'),
        user_id=current_user.id
    )

    db.session.add(research)
    db.session.commit()

    return jsonify({
        'success': True,
        'data': research_to_dict(research, include_full=True)
    }), 201


@api_bp.route('/researches/<int:id>', methods=['PUT'])
@login_required
def update_research(id):
    """แก้ไขงานวิจัย"""
    research = Research.query.get_or_404(id)

    # ตรวจสอบสิทธิ์
    if research.user_id != current_user.id and not current_user.is_admin:
        return jsonify({
            'success': False,
            'error': 'คุณไม่มีสิทธิ์แก้ไขงานวิจัยนี้'
        }), 403

    data = request.get_json()

    if data.get('title'):
        research.title = data.get('title')
    if 'title_en' in data:
        research.title_en = data.get('title_en')
    if data.get('authors'):
        research.authors = data.get('authors')
    if 'abstract' in data:
        research.abstract = data.get('abstract')
    if 'keywords' in data:
        research.keywords = data.get('keywords')
    if 'year' in data:
        research.year = data.get('year')
    if 'publication_type' in data:
        research.publication_type = data.get('publication_type')
    if 'journal_name' in data:
        research.journal_name = data.get('journal_name')
    if 'volume' in data:
        research.volume = data.get('volume')
    if 'issue' in data:
        research.issue = data.get('issue')
    if 'pages' in data:
        research.pages = data.get('pages')
    if 'doi' in data:
        research.doi = data.get('doi')
    if 'url' in data:
        research.url = data.get('url')
    if 'category_id' in data:
        research.category_id = data.get('category_id')

    db.session.commit()

    return jsonify({
        'success': True,
        'data': research_to_dict(research, include_full=True)
    })


@api_bp.route('/researches/<int:id>', methods=['DELETE'])
@login_required
def delete_research(id):
    """ลบงานวิจัย"""
    research = Research.query.get_or_404(id)

    # ตรวจสอบสิทธิ์
    if research.user_id != current_user.id and not current_user.is_admin:
        return jsonify({
            'success': False,
            'error': 'คุณไม่มีสิทธิ์ลบงานวิจัยนี้'
        }), 403

    db.session.delete(research)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'ลบงานวิจัยสำเร็จ'
    })


# ============================================
# Category API Endpoints
# ============================================

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """ดึงรายการหมวดหมู่ทั้งหมด"""
    categories = Category.query.all()
    return jsonify({
        'success': True,
        'data': [{
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'research_count': len(c.researches)
        } for c in categories]
    })


@api_bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    """ดึงข้อมูลหมวดหมู่ตาม ID"""
    category = Category.query.get_or_404(id)
    return jsonify({
        'success': True,
        'data': {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'research_count': len(category.researches)
        }
    })


# ============================================
# Tag API Endpoints
# ============================================

@api_bp.route('/tags', methods=['GET'])
def get_tags():
    """ดึงรายการแท็กทั้งหมด"""
    tags = Tag.query.all()
    return jsonify({
        'success': True,
        'data': [{
            'id': t.id,
            'name': t.name,
            'research_count': len(t.researches)
        } for t in tags]
    })


# ============================================
# Bookmark API Endpoints
# ============================================

@api_bp.route('/bookmarks', methods=['GET'])
@login_required
def get_bookmarks():
    """ดึงรายการบุ๊กมาร์กของผู้ใช้"""
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'success': True,
        'data': [{
            'id': b.id,
            'research': research_to_dict(b.research),
            'created_at': b.created_at.isoformat() if b.created_at else None
        } for b in bookmarks]
    })


@api_bp.route('/bookmarks/<int:research_id>', methods=['POST'])
@login_required
def add_bookmark(research_id):
    """เพิ่มบุ๊กมาร์ก"""
    research = Research.query.get_or_404(research_id)

    # ตรวจสอบว่ามีบุ๊กมาร์กอยู่แล้วหรือไม่
    existing = Bookmark.query.filter_by(
        user_id=current_user.id,
        research_id=research_id
    ).first()

    if existing:
        return jsonify({
            'success': False,
            'error': 'คุณได้บุ๊กมาร์กงานวิจัยนี้แล้ว'
        }), 400

    bookmark = Bookmark(user_id=current_user.id, research_id=research_id)
    db.session.add(bookmark)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'เพิ่มบุ๊กมาร์กสำเร็จ'
    }), 201


@api_bp.route('/bookmarks/<int:research_id>', methods=['DELETE'])
@login_required
def remove_bookmark(research_id):
    """ลบบุ๊กมาร์ก"""
    bookmark = Bookmark.query.filter_by(
        user_id=current_user.id,
        research_id=research_id
    ).first_or_404()

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'ลบบุ๊กมาร์กสำเร็จ'
    })


# ============================================
# Comment API Endpoints
# ============================================

@api_bp.route('/researches/<int:research_id>/comments', methods=['GET'])
def get_comments(research_id):
    """ดึงรายการคอมเมนต์ของงานวิจัย"""
    research = Research.query.get_or_404(research_id)
    comments = Comment.query.filter_by(research_id=research_id).order_by(Comment.created_at.desc()).all()

    return jsonify({
        'success': True,
        'data': [{
            'id': c.id,
            'content': c.content,
            'rating': c.rating,
            'user': {
                'id': c.user.id,
                'username': c.user.username,
                'full_name': c.user.full_name
            },
            'created_at': c.created_at.isoformat() if c.created_at else None,
            'updated_at': c.updated_at.isoformat() if c.updated_at else None
        } for c in comments]
    })


@api_bp.route('/researches/<int:research_id>/comments', methods=['POST'])
@login_required
def add_comment(research_id):
    """เพิ่มคอมเมนต์"""
    research = Research.query.get_or_404(research_id)
    data = request.get_json()

    if not data or not data.get('content'):
        return jsonify({
            'success': False,
            'error': 'กรุณาระบุเนื้อหาคอมเมนต์'
        }), 400

    comment = Comment(
        content=data.get('content'),
        rating=data.get('rating'),
        user_id=current_user.id,
        research_id=research_id
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'เพิ่มคอมเมนต์สำเร็จ',
        'data': {
            'id': comment.id,
            'content': comment.content,
            'rating': comment.rating,
            'created_at': comment.created_at.isoformat() if comment.created_at else None
        }
    }), 201


# ============================================
# Statistics API Endpoints
# ============================================

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """ดึงสถิติของระบบ"""
    total_researches = Research.query.count()
    total_users = User.query.count()
    total_categories = Category.query.count()
    total_tags = Tag.query.count()
    total_bookmarks = Bookmark.query.count()
    total_comments = Comment.query.count()

    # สถิติตามประเภท
    pub_type_stats = db.session.query(
        Research.publication_type,
        db.func.count(Research.id)
    ).group_by(Research.publication_type).all()

    # สถิติตามปี
    year_stats = db.session.query(
        Research.year,
        db.func.count(Research.id)
    ).group_by(Research.year).order_by(Research.year.desc()).limit(10).all()

    # งานวิจัยยอดนิยม
    popular_researches = Research.query.order_by(Research.view_count.desc()).limit(10).all()

    return jsonify({
        'success': True,
        'data': {
            'totals': {
                'researches': total_researches,
                'users': total_users,
                'categories': total_categories,
                'tags': total_tags,
                'bookmarks': total_bookmarks,
                'comments': total_comments
            },
            'publication_types': [{
                'type': t[0] if t[0] else 'ไม่ระบุ',
                'count': t[1]
            } for t in pub_type_stats],
            'by_year': [{
                'year': y[0] if y[0] else 'ไม่ระบุ',
                'count': y[1]
            } for y in year_stats],
            'popular': [research_to_dict(r) for r in popular_researches]
        }
    })


# ============================================
# Error Handlers
# ============================================

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'ไม่พบข้อมูลที่ต้องการ'
    }), 404


@api_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์'
    }), 500
