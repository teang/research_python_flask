from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db

# Many-to-Many relationship between User and Role
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class User(UserMixin, db.Model):
    """โมเดลสำหรับผู้ใช้งานระบบ"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    department = db.Column(db.String(100))  # หน่วยงาน
    position = db.Column(db.String(100))  # ตำแหน่ง

    # สถานะ
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    email_verified_at = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)

    # วันที่
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ความสัมพันธ์
    roles = db.relationship('Role', secondary=user_roles,
                           backref=db.backref('users', lazy='dynamic'))
    researches = db.relationship('Research', backref='uploader', lazy=True)

    def set_password(self, password):
        """เข้ารหัสรหัสผ่าน"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ตรวจสอบรหัสผ่าน"""
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        """ตรวจสอบว่าผู้ใช้มี Role ที่ระบุหรือไม่"""
        return any(role.name == role_name for role in self.roles)

    def has_permission(self, permission_name):
        """ตรวจสอบว่าผู้ใช้มี Permission ที่ระบุหรือไม่"""
        for role in self.roles:
            if role.has_permission(permission_name):
                return True
        return False

    def add_role(self, role):
        """เพิ่ม Role ให้กับผู้ใช้"""
        if role not in self.roles:
            self.roles.append(role)

    def remove_role(self, role):
        """ลบ Role จากผู้ใช้"""
        if role in self.roles:
            self.roles.remove(role)

    @property
    def is_admin(self):
        """ตรวจสอบว่าเป็น Admin หรือไม่"""
        return self.has_role('admin')

    @property
    def is_researcher(self):
        """ตรวจสอบว่าเป็นนักวิจัยหรือไม่"""
        return self.has_role('researcher')

    def __repr__(self):
        return f'<User {self.username}>'
