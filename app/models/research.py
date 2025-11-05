from datetime import datetime
from app.models import db


class Research(db.Model):
    """โมเดลสำหรับงานวิจัย"""
    __tablename__ = 'researches'

    id = db.Column(db.Integer, primary_key=True)

    # ข้อมูลพื้นฐาน
    title = db.Column(db.String(300), nullable=False, index=True)
    title_en = db.Column(db.String(300))  # ชื่อภาษาอังกฤษ
    authors = db.Column(db.Text, nullable=False)  # รายชื่อผู้วิจัย
    abstract = db.Column(db.Text)  # บทคัดย่อ
    abstract_en = db.Column(db.Text)  # บทคัดย่อภาษาอังกฤษ
    keywords = db.Column(db.String(500))  # คำสำคัญ

    # ข้อมูลการตีพิมพ์
    year = db.Column(db.Integer, index=True)  # ปีที่เผยแพร่
    publication_type = db.Column(db.String(50))  # ประเภท: journal, conference, thesis
    journal_name = db.Column(db.String(200))  # ชื่อวารสาร/การประชุม
    volume = db.Column(db.String(50))  # เล่มที่
    issue = db.Column(db.String(50))  # ฉบับที่
    pages = db.Column(db.String(50))  # หน้า

    # ข้อมูลอ้างอิง
    doi = db.Column(db.String(200))  # DOI
    isbn = db.Column(db.String(50))  # ISBN (สำหรับหนังสือ)
    url = db.Column(db.String(500))  # ลิงก์
    file_path = db.Column(db.String(500))  # ที่เก็บไฟล์ PDF

    # สถานะ
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    is_featured = db.Column(db.Boolean, default=False)  # งานวิจัยแนะนำ
    view_count = db.Column(db.Integer, default=0)  # จำนวนครั้งที่ถูกดู
    download_count = db.Column(db.Integer, default=0)  # จำนวนครั้งที่ถูกดาวน์โหลด

    # ข้อมูลเพิ่มเติม
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # วันที่
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def increment_view(self):
        """เพิ่มจำนวนการดู"""
        self.view_count += 1
        db.session.commit()

    def increment_download(self):
        """เพิ่มจำนวนการดาวน์โหลด"""
        self.download_count += 1
        db.session.commit()

    def publish(self):
        """เผยแพร่งานวิจัย"""
        self.status = 'published'
        self.published_at = datetime.utcnow()

    def __repr__(self):
        return f'<Research {self.title}>'
