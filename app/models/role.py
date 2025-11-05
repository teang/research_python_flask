from datetime import datetime
from app.models import db

# Many-to-Many relationship between Role and Permission
role_permissions = db.Table('role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)


class Role(db.Model):
    """โมเดลสำหรับบทบาท (Role) ในระบบ RBAC"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    name_th = db.Column(db.String(100), nullable=False)  # ชื่อภาษาไทย
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ความสัมพันธ์
    permissions = db.relationship('Permission', secondary=role_permissions,
                                 backref=db.backref('roles', lazy='dynamic'))

    def __repr__(self):
        return f'<Role {self.name}>'

    def has_permission(self, permission_name):
        """ตรวจสอบว่า Role นี้มี Permission ที่ระบุหรือไม่"""
        return any(p.name == permission_name for p in self.permissions)

    def add_permission(self, permission):
        """เพิ่ม Permission ให้กับ Role"""
        if permission not in self.permissions:
            self.permissions.append(permission)

    def remove_permission(self, permission):
        """ลบ Permission จาก Role"""
        if permission in self.permissions:
            self.permissions.remove(permission)


class Permission(db.Model):
    """โมเดลสำหรับสิทธิ์ (Permission) ในระบบ RBAC"""
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    name_th = db.Column(db.String(150), nullable=False)  # ชื่อภาษาไทย
    description = db.Column(db.Text)
    resource = db.Column(db.String(50))  # ทรัพยากรที่เกี่ยวข้อง เช่น 'research', 'user', 'category'
    action = db.Column(db.String(50))  # การกระทำ เช่น 'create', 'read', 'update', 'delete'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Permission {self.name}>'
