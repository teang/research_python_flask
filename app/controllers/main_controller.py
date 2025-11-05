from flask import Blueprint, render_template
from app.models import Research, Category
from sqlalchemy import func

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """หน้าแรก - Frontend"""
    # งานวิจัยล่าสุด
    recent_researches = Research.query.filter_by(status='published')\
        .order_by(Research.created_at.desc()).limit(6).all()

    # งานวิจัยแนะนำ
    featured_researches = Research.query.filter_by(status='published', is_featured=True)\
        .order_by(Research.created_at.desc()).limit(3).all()

    # สถิติ
    total_researches = Research.query.filter_by(status='published').count()
    total_categories = Category.query.filter_by(is_active=True).count()

    # หมวดหมู่พร้อมจำนวนงานวิจัย
    categories = Category.query.filter_by(is_active=True)\
        .order_by(Category.display_order, Category.name).all()

    return render_template('frontend/index.html',
                         recent_researches=recent_researches,
                         featured_researches=featured_researches,
                         total_researches=total_researches,
                         total_categories=total_categories,
                         categories=categories)


@main_bp.route('/about')
def about():
    """เกี่ยวกับเรา"""
    return render_template('frontend/about.html')


@main_bp.route('/contact')
def contact():
    """ติดต่อเรา"""
    return render_template('frontend/contact.html')
