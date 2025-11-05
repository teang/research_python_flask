from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ตารางเชื่อมโยงระหว่าง Research และ Tag (Many-to-Many)
research_tags = db.Table('research_tags',
    db.Column('research_id', db.Integer, db.ForeignKey('researches.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

# ตารางเชื่อมโยงระหว่าง User และ Role (Many-to-Many)
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

# ตารางเชื่อมโยงระหว่าง Role และ Permission (Many-to-Many)
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)


class User(UserMixin, db.Model):
    """โมเดลสำหรับผู้ใช้งานระบบ"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text)  # ประวัติส่วนตัว
    avatar = db.Column(db.String(500))  # รูปโปรไฟล์
    email_notifications = db.Column(db.Boolean, default=True)  # รับการแจ้งเตือนทางอีเมล
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ความสัมพันธ์กับงานวิจัย
    researches = db.relationship('Research', backref='uploader', lazy=True, foreign_keys='Research.user_id')
    bookmarks = db.relationship('Bookmark', backref='user', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')

    # ความสัมพันธ์กับบทบาท (Roles)
    roles = db.relationship('Role', secondary=user_roles, lazy='subquery',
                           backref=db.backref('users', lazy=True))

    def set_password(self, password):
        """เข้ารหัสรหัสผ่าน"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ตรวจสอบรหัสผ่าน"""
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        """ตรวจสอบว่าผู้ใช้มีบทบาทนี้หรือไม่"""
        return any(role.name == role_name for role in self.roles)

    def has_permission(self, permission_name):
        """ตรวจสอบว่าผู้ใช้มีสิทธิ์นี้หรือไม่"""
        for role in self.roles:
            if any(perm.name == permission_name for perm in role.permissions):
                return True
        return False

    def get_permissions(self):
        """ดึงรายการสิทธิ์ทั้งหมดของผู้ใช้"""
        permissions = set()
        for role in self.roles:
            for perm in role.permissions:
                permissions.add(perm.name)
        return list(permissions)

    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    """โมเดลสำหรับหมวดหมู่งานวิจัย"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    # ความสัมพันธ์กับงานวิจัย
    researches = db.relationship('Research', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Research(db.Model):
    """โมเดลสำหรับงานวิจัย"""
    __tablename__ = 'researches'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    title_en = db.Column(db.String(300))  # ชื่อภาษาอังกฤษ
    authors = db.Column(db.Text, nullable=False)  # รายชื่อผู้วิจัย
    abstract = db.Column(db.Text)  # บทคัดย่อ
    keywords = db.Column(db.String(500))  # คำสำคัญ
    year = db.Column(db.Integer)  # ปีที่เผยแพร่
    publication_type = db.Column(db.String(50))  # ประเภท: วารสาร, การประชุม, วิทยานิพนธ์
    journal_name = db.Column(db.String(200))  # ชื่อวารสาร/การประชุม
    volume = db.Column(db.String(50))  # เล่มที่
    issue = db.Column(db.String(50))  # ฉบับที่
    pages = db.Column(db.String(50))  # หน้า
    doi = db.Column(db.String(200))  # DOI
    url = db.Column(db.String(500))  # ลิงก์
    file_path = db.Column(db.String(500))  # ที่เก็บไฟล์ PDF
    file_size = db.Column(db.Integer)  # ขนาดไฟล์ (bytes)

    # ข้อมูลเพิ่มเติม
    view_count = db.Column(db.Integer, default=0)  # จำนวนครั้งที่ถูกดู
    download_count = db.Column(db.Integer, default=0)  # จำนวนครั้งที่ถูกดาวน์โหลด
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ความสัมพันธ์
    tags = db.relationship('Tag', secondary=research_tags, lazy='subquery',
                          backref=db.backref('researches', lazy=True))
    bookmarks = db.relationship('Bookmark', backref='research', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='research', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Research {self.title}>'

    def increment_view_count(self):
        """เพิ่มจำนวนการดู"""
        self.view_count += 1
        db.session.commit()

    def increment_download_count(self):
        """เพิ่มจำนวนการดาวน์โหลด"""
        self.download_count += 1
        db.session.commit()


class Tag(db.Model):
    """โมเดลสำหรับแท็ก"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Tag {self.name}>'


class Bookmark(db.Model):
    """โมเดลสำหรับบุ๊กมาร์ก"""
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ป้องกันการบุ๊กมาร์กซ้ำ
    __table_args__ = (db.UniqueConstraint('user_id', 'research_id', name='unique_bookmark'),)

    def __repr__(self):
        return f'<Bookmark User:{self.user_id} Research:{self.research_id}>'


class Comment(db.Model):
    """โมเดลสำหรับคอมเมนต์"""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # คะแนน 1-5
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id}>'


class Role(db.Model):
    """โมเดลสำหรับบทบาท (Roles)"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    display_name = db.Column(db.String(100))  # ชื่อแสดง
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ความสัมพันธ์กับสิทธิ์
    permissions = db.relationship('Permission', secondary=role_permissions, lazy='subquery',
                                 backref=db.backref('roles', lazy=True))

    def __repr__(self):
        return f'<Role {self.name}>'

    def add_permission(self, permission):
        """เพิ่มสิทธิ์ให้กับบทบาท"""
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission):
        """ลบสิทธิ์ออกจากบทบาท"""
        if permission in self.permissions:
            self.permissions.remove(permission)


class Permission(db.Model):
    """โมเดลสำหรับสิทธิ์ (Permissions)"""
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    display_name = db.Column(db.String(150))  # ชื่อแสดง
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # หมวดหมู่ของสิทธิ์ เช่น 'user', 'research', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Permission {self.name}>'


class AuditLog(db.Model):
    """โมเดลสำหรับบันทึกการใช้งาน (Audit Logs)"""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)  # ประเภทของการกระทำ
    resource_type = db.Column(db.String(50))  # ประเภทของทรัพยากร เช่น 'User', 'Research'
    resource_id = db.Column(db.Integer)  # ID ของทรัพยากร
    details = db.Column(db.Text)  # รายละเอียดเพิ่มเติม (JSON)
    ip_address = db.Column(db.String(50))  # IP ของผู้ใช้
    user_agent = db.Column(db.String(500))  # User Agent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ความสัมพันธ์กับผู้ใช้
    user = db.relationship('User', backref='audit_logs', lazy=True)

    def __repr__(self):
        return f'<AuditLog {self.action} by User:{self.user_id}>'
