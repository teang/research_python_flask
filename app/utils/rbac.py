"""
Utility สำหรับจัดการระบบ RBAC
"""
from app.models import db, Role, Permission


def init_rbac():
    """สร้างข้อมูล Role และ Permission เริ่มต้น"""

    # สร้าง Permissions
    permissions_data = [
        # Research Permissions
        {'name': 'research.create', 'name_th': 'สร้างงานวิจัย', 'resource': 'research', 'action': 'create'},
        {'name': 'research.read', 'name_th': 'อ่านงานวิจัย', 'resource': 'research', 'action': 'read'},
        {'name': 'research.update', 'name_th': 'แก้ไขงานวิจัย', 'resource': 'research', 'action': 'update'},
        {'name': 'research.delete', 'name_th': 'ลบงานวิจัย', 'resource': 'research', 'action': 'delete'},
        {'name': 'research.publish', 'name_th': 'เผยแพร่งานวิจัย', 'resource': 'research', 'action': 'publish'},

        # Category Permissions
        {'name': 'category.create', 'name_th': 'สร้างหมวดหมู่', 'resource': 'category', 'action': 'create'},
        {'name': 'category.read', 'name_th': 'อ่านหมวดหมู่', 'resource': 'category', 'action': 'read'},
        {'name': 'category.update', 'name_th': 'แก้ไขหมวดหมู่', 'resource': 'category', 'action': 'update'},
        {'name': 'category.delete', 'name_th': 'ลบหมวดหมู่', 'resource': 'category', 'action': 'delete'},

        # User Permissions
        {'name': 'user.create', 'name_th': 'สร้างผู้ใช้', 'resource': 'user', 'action': 'create'},
        {'name': 'user.read', 'name_th': 'อ่านข้อมูลผู้ใช้', 'resource': 'user', 'action': 'read'},
        {'name': 'user.update', 'name_th': 'แก้ไขข้อมูลผู้ใช้', 'resource': 'user', 'action': 'update'},
        {'name': 'user.delete', 'name_th': 'ลบผู้ใช้', 'resource': 'user', 'action': 'delete'},

        # Role Permissions
        {'name': 'role.manage', 'name_th': 'จัดการบทบาท', 'resource': 'role', 'action': 'manage'},

        # System Permissions
        {'name': 'system.admin', 'name_th': 'ดูแลระบบ', 'resource': 'system', 'action': 'admin'},
    ]

    permissions = {}
    for perm_data in permissions_data:
        perm = Permission.query.filter_by(name=perm_data['name']).first()
        if not perm:
            perm = Permission(**perm_data)
            db.session.add(perm)
            print(f"Created permission: {perm_data['name']}")
        permissions[perm_data['name']] = perm

    db.session.commit()

    # สร้าง Roles
    roles_data = [
        {
            'name': 'admin',
            'name_th': 'ผู้ดูแลระบบ',
            'description': 'มีสิทธิ์เต็มในการจัดการระบบทั้งหมด',
            'permissions': list(permissions.values())  # ทุก permissions
        },
        {
            'name': 'researcher',
            'name_th': 'นักวิจัย',
            'description': 'สามารถสร้างและจัดการงานวิจัยของตนเอง',
            'permissions': [
                permissions['research.create'],
                permissions['research.read'],
                permissions['research.update'],
                permissions['category.read'],
            ]
        },
        {
            'name': 'editor',
            'name_th': 'บรรณาธิการ',
            'description': 'สามารถแก้ไขและเผยแพร่งานวิจัย',
            'permissions': [
                permissions['research.create'],
                permissions['research.read'],
                permissions['research.update'],
                permissions['research.delete'],
                permissions['research.publish'],
                permissions['category.read'],
                permissions['category.create'],
                permissions['category.update'],
            ]
        },
        {
            'name': 'viewer',
            'name_th': 'ผู้เข้าชม',
            'description': 'สามารถดูงานวิจัยเท่านั้น',
            'permissions': [
                permissions['research.read'],
                permissions['category.read'],
            ]
        },
    ]

    for role_data in roles_data:
        role = Role.query.filter_by(name=role_data['name']).first()
        if not role:
            role_perms = role_data.pop('permissions')
            role = Role(**role_data)
            for perm in role_perms:
                role.add_permission(perm)
            db.session.add(role)
            print(f"Created role: {role_data['name']}")
        else:
            # Update permissions if role exists
            role_perms = role_data.get('permissions', [])
            role.permissions = role_perms

    db.session.commit()
    print("RBAC initialization completed!")

    return True
