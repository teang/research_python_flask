from datetime import datetime
from app.models import db


class Category(db.Model):
    """โมเดลสำหรับหมวดหมู่งานวิจัย"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    name_en = db.Column(db.String(100))  # ชื่อภาษาอังกฤษ
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # ไอคอน
    color = db.Column(db.String(20))  # สีประจำหมวดหมู่
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)  # ลำดับการแสดง
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ความสัมพันธ์กับงานวิจัย
    researches = db.relationship('Research', backref='category', lazy=True)

    @property
    def research_count(self):
        """จำนวนงานวิจัยในหมวดหมู่นี้"""
        return len(self.researches)

    def __repr__(self):
        return f'<Category {self.name}>'
