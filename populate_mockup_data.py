#!/usr/bin/env python3
"""
สคริปต์สำหรับสร้างข้อมูล mockup สำหรับทุก table
"""
from datetime import datetime, timedelta
from app import create_app
from app.models import (
    db, User, Category, Research, Tag, Bookmark, Comment,
    Role, Permission, AuditLog
)

def clear_all_data():
    """ลบข้อมูลทั้งหมดออกจากฐานข้อมูล"""
    print("🗑️  กำลังลบข้อมูลเดิม...")
    # ลบตารางเชื่อมโยง (Many-to-Many)
    db.session.execute(db.text('DELETE FROM research_tags'))
    db.session.execute(db.text('DELETE FROM user_roles'))
    db.session.execute(db.text('DELETE FROM role_permissions'))

    # ลบข้อมูลจากตารางหลัก
    AuditLog.query.delete()
    Comment.query.delete()
    Bookmark.query.delete()
    Research.query.delete()
    Tag.query.delete()
    Category.query.delete()
    User.query.delete()
    Permission.query.delete()
    Role.query.delete()

    db.session.commit()
    print("✅ ลบข้อมูลเดิมเรียบร้อย")

def create_permissions():
    """สร้างข้อมูล Permissions"""
    print("\n📋 กำลังสร้าง Permissions...")
    permissions_data = [
        # User permissions
        {
            'name': 'user.view',
            'display_name': 'ดูข้อมูลผู้ใช้',
            'description': 'สามารถดูข้อมูลผู้ใช้ทั่วไป',
            'category': 'user'
        },
        {
            'name': 'user.create',
            'display_name': 'สร้างผู้ใช้',
            'description': 'สามารถสร้างผู้ใช้ใหม่',
            'category': 'user'
        },
        {
            'name': 'user.edit',
            'display_name': 'แก้ไขผู้ใช้',
            'description': 'สามารถแก้ไขข้อมูลผู้ใช้',
            'category': 'user'
        },
        {
            'name': 'user.delete',
            'display_name': 'ลบผู้ใช้',
            'description': 'สามารถลบผู้ใช้',
            'category': 'user'
        },
        # Research permissions
        {
            'name': 'research.view',
            'display_name': 'ดูงานวิจัย',
            'description': 'สามารถดูงานวิจัย',
            'category': 'research'
        },
        {
            'name': 'research.create',
            'display_name': 'สร้างงานวิจัย',
            'description': 'สามารถอัพโหลดงานวิจัยใหม่',
            'category': 'research'
        },
        {
            'name': 'research.edit',
            'display_name': 'แก้ไขงานวิจัย',
            'description': 'สามารถแก้ไขงานวิจัย',
            'category': 'research'
        },
        {
            'name': 'research.delete',
            'display_name': 'ลบงานวิจัย',
            'description': 'สามารถลบงานวิจัย',
            'category': 'research'
        },
        # Admin permissions
        {
            'name': 'admin.access',
            'display_name': 'เข้าถึงหน้าแอดมิน',
            'description': 'สามารถเข้าถึงหน้าจัดการระบบ',
            'category': 'admin'
        },
        {
            'name': 'admin.manage_roles',
            'display_name': 'จัดการบทบาท',
            'description': 'สามารถจัดการบทบาทและสิทธิ์',
            'category': 'admin'
        },
        {
            'name': 'admin.view_logs',
            'display_name': 'ดู Audit Logs',
            'description': 'สามารถดู Audit Logs',
            'category': 'admin'
        },
    ]

    permissions = []
    for perm_data in permissions_data:
        perm = Permission(**perm_data)
        db.session.add(perm)
        permissions.append(perm)

    db.session.commit()
    print(f"✅ สร้าง {len(permissions)} permissions เรียบร้อย")
    return permissions

def create_roles(permissions):
    """สร้างข้อมูล Roles"""
    print("\n👥 กำลังสร้าง Roles...")

    # สร้าง Admin Role
    admin_role = Role(
        name='admin',
        display_name='ผู้ดูแลระบบ',
        description='มีสิทธิ์เต็มในการจัดการระบบ'
    )
    # Admin มีสิทธิ์ทั้งหมด
    admin_role.permissions = permissions
    db.session.add(admin_role)

    # สร้าง Researcher Role
    researcher_role = Role(
        name='researcher',
        display_name='นักวิจัย',
        description='สามารถอัพโหลดและจัดการงานวิจัยของตนเอง'
    )
    # Researcher มีสิทธิ์เกี่ยวกับงานวิจัย
    researcher_perms = [p for p in permissions if p.category in ['research', 'user'] and 'delete' not in p.name]
    researcher_role.permissions = researcher_perms
    db.session.add(researcher_role)

    # สร้าง User Role (ผู้ใช้ทั่วไป)
    user_role = Role(
        name='user',
        display_name='ผู้ใช้ทั่วไป',
        description='สามารถดูและค้นหางานวิจัย'
    )
    # User มีสิทธิ์ดูเท่านั้น
    user_perms = [p for p in permissions if 'view' in p.name]
    user_role.permissions = user_perms
    db.session.add(user_role)

    db.session.commit()
    print("✅ สร้าง 3 roles เรียบร้อย (admin, researcher, user)")
    return {'admin': admin_role, 'researcher': researcher_role, 'user': user_role}

def create_users(roles):
    """สร้างข้อมูล Users"""
    print("\n👤 กำลังสร้าง Users...")

    users_data = [
        {
            'username': 'admin',
            'email': 'admin@research.com',
            'password': '123456',
            'full_name': 'ผู้ดูแลระบบ',
            'is_admin': True,
            'bio': 'ผู้ดูแลระบบจัดการงานวิจัย',
            'email_notifications': True,
            'roles': [roles['admin']]
        },
        {
            'username': 'somchai',
            'email': 'somchai@university.ac.th',
            'password': '123456',
            'full_name': 'ดร. สมชาย ใจดี',
            'is_admin': False,
            'bio': 'อาจารย์ประจำคณะวิทยาศาสตร์ สาขาวิทยาการคอมพิวเตอร์',
            'email_notifications': True,
            'roles': [roles['researcher']]
        },
        {
            'username': 'pensri',
            'email': 'pensri@university.ac.th',
            'password': '123456',
            'full_name': 'ผศ.ดร. เพ็ญศรี สุขใจ',
            'is_admin': False,
            'bio': 'อาจารย์ประจำคณะวิศวกรรมศาสตร์',
            'email_notifications': True,
            'roles': [roles['researcher']]
        },
        {
            'username': 'manee',
            'email': 'manee@student.ac.th',
            'password': '123456',
            'full_name': 'มานี ขยัน',
            'is_admin': False,
            'bio': 'นักศึกษาปริญญาโท สาขาวิทยาการข้อมูล',
            'email_notifications': False,
            'roles': [roles['user']]
        },
        {
            'username': 'wichai',
            'email': 'wichai@university.ac.th',
            'password': '123456',
            'full_name': 'รศ.ดร. วิชัย พัฒนา',
            'is_admin': False,
            'bio': 'อาจารย์ประจำคณะวิทยาศาสตร์ สาขาฟิสิกส์',
            'email_notifications': True,
            'roles': [roles['researcher']]
        },
    ]

    users = []
    for user_data in users_data:
        password = user_data.pop('password')
        user = User(**user_data)
        user.set_password(password)
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print(f"✅ สร้าง {len(users)} users เรียบร้อย")
    return users

def create_categories():
    """สร้างข้อมูล Categories"""
    print("\n📚 กำลังสร้าง Categories...")

    categories_data = [
        {
            'name': 'วิทยาการคอมพิวเตอร์',
            'description': 'งานวิจัยด้านวิทยาการคอมพิวเตอร์ อัลกอริทึม และโครงสร้างข้อมูล'
        },
        {
            'name': 'ปัญญาประดิษฐ์',
            'description': 'งานวิจัยด้าน AI, Machine Learning, Deep Learning'
        },
        {
            'name': 'วิศวกรรมซอฟต์แวร์',
            'description': 'งานวิจัยด้านการพัฒนาซอฟต์แวร์และการจัดการโครงการ'
        },
        {
            'name': 'ความมั่นคงปลอดภัยทางไซเบอร์',
            'description': 'งานวิจัยด้านความปลอดภัยของระบบคอมพิวเตอร์และเครือข่าย'
        },
        {
            'name': 'ฐานข้อมูล',
            'description': 'งานวิจัยด้านระบบฐานข้อมูลและ Big Data'
        },
        {
            'name': 'เครือข่ายคอมพิวเตอร์',
            'description': 'งานวิจัยด้านเครือข่ายและการสื่อสารข้อมูล'
        },
    ]

    categories = []
    for cat_data in categories_data:
        cat = Category(**cat_data)
        db.session.add(cat)
        categories.append(cat)

    db.session.commit()
    print(f"✅ สร้าง {len(categories)} categories เรียบร้อย")
    return categories

def create_tags():
    """สร้างข้อมูล Tags"""
    print("\n🏷️  กำลังสร้าง Tags...")

    tag_names = [
        'Machine Learning', 'Deep Learning', 'Neural Networks', 'NLP',
        'Computer Vision', 'Big Data', 'Cloud Computing', 'IoT',
        'Blockchain', 'Cybersecurity', 'Data Mining', 'Web Development',
        'Mobile App', 'DevOps', 'Agile', 'Microservices',
        'Python', 'Java', 'JavaScript', 'React',
        'Database', 'SQL', 'NoSQL', 'API'
    ]

    tags = []
    for tag_name in tag_names:
        tag = Tag(name=tag_name)
        db.session.add(tag)
        tags.append(tag)

    db.session.commit()
    print(f"✅ สร้าง {len(tags)} tags เรียบร้อย")
    return tags

def create_researches(users, categories, tags):
    """สร้างข้อมูล Research"""
    print("\n🔬 กำลังสร้าง Researches...")

    researches_data = [
        {
            'title': 'การพัฒนาระบบตรวจจับวัตถุด้วย Deep Learning',
            'title_en': 'Object Detection System Development using Deep Learning',
            'authors': 'ดร. สมชาย ใจดี, มานี ขยัน',
            'abstract': 'งานวิจัยนี้นำเสนอการพัฒนาระบบตรวจจับวัตถุโดยใช้เทคนิค Deep Learning ด้วยโมเดล YOLO v8 สำหรับการตรวจจับวัตถุแบบ Real-time ผลการทดลองแสดงให้เห็นว่าระบบสามารถตรวจจับวัตถุได้อย่างแม่นยำถึง 95%',
            'keywords': 'Deep Learning, Object Detection, YOLO, Computer Vision',
            'year': 2024,
            'publication_type': 'วารสาร',
            'journal_name': 'วารสารวิทยาศาสตร์และเทคโนโลยี',
            'volume': '32',
            'issue': '1',
            'pages': '45-62',
            'doi': '10.1234/jst.2024.001',
            'url': 'https://example.com/research1',
            'view_count': 150,
            'download_count': 45,
            # Dublin Core metadata
            'publisher': 'สำนักพิมพ์มหาวิทยาลัยเทคโนโลยี',
            'contributor': 'ผศ.ดร. วิชัย พัฒนา (ที่ปรึกษา)',
            'format': 'application/pdf',
            'source': 'https://example.com/research1/original',
            'language': 'th',
            'relation': 'https://example.com/research5',
            'coverage': 'ประเทศไทย; 2023-2024',
            'rights': 'CC BY-NC-SA 4.0',
            'category_id': 2,  # ปัญญาประดิษฐ์
            'user_id': 2,  # somchai
            'tags': [tags[0], tags[1], tags[2], tags[4]]  # ML, DL, NN, CV
        },
        {
            'title': 'ระบบจัดการงานโครงการด้วย Agile Methodology',
            'title_en': 'Project Management System with Agile Methodology',
            'authors': 'ผศ.ดร. เพ็ญศรี สุขใจ',
            'abstract': 'การศึกษาและพัฒนาระบบจัดการโครงการซอฟต์แวร์โดยใช้หลักการ Agile Scrum เพื่อเพิ่มประสิทธิภาพในการทำงานของทีม ผลการทดลองพบว่าทีมสามารถส่งมอบงานได้เร็วขึ้น 40%',
            'keywords': 'Agile, Scrum, Project Management, Software Engineering',
            'year': 2023,
            'publication_type': 'การประชุม',
            'journal_name': 'International Conference on Software Engineering',
            'volume': None,
            'issue': None,
            'pages': '112-125',
            'doi': '10.1234/icse.2023.015',
            'url': 'https://example.com/research2',
            'view_count': 89,
            'download_count': 32,
            # Dublin Core metadata
            'publisher': 'IEEE Computer Society',
            'contributor': 'รศ.ดร. วิชัย พัฒนา (ผู้ร่วมวิจัย)',
            'format': 'application/pdf',
            'source': 'Proceedings of ICSE 2023',
            'language': 'en',
            'relation': 'https://example.com/research6',
            'coverage': 'สากล; 2022-2023',
            'rights': 'Copyright © 2023 IEEE',
            'category_id': 3,  # วิศวกรรมซอฟต์แวร์
            'user_id': 3,  # pensri
            'tags': [tags[14], tags[13], tags[11]]  # Agile, DevOps, Web
        },
        {
            'title': 'การวิเคราะห์ความปลอดภัยของระบบ IoT',
            'title_en': 'Security Analysis of IoT Systems',
            'authors': 'รศ.ดร. วิชัย พัฒนา, ดร. สมชาย ใจดี',
            'abstract': 'งานวิจัยนี้ศึกษาและวิเคราะห์ช่องโหว่ด้านความปลอดภัยในระบบ Internet of Things (IoT) พร้อมเสนอแนวทางการป้องกันและแก้ไข โดยทดลองกับอุปกรณ์ IoT จำนวน 50 เครื่อง',
            'keywords': 'IoT, Cybersecurity, Vulnerability, Network Security',
            'year': 2024,
            'publication_type': 'วารสาร',
            'journal_name': 'Journal of Cybersecurity Research',
            'volume': '18',
            'issue': '2',
            'pages': '78-95',
            'doi': '10.1234/jcr.2024.008',
            'url': 'https://example.com/research3',
            'view_count': 234,
            'download_count': 87,
            # Dublin Core metadata
            'publisher': 'Cybersecurity Research Institute',
            'contributor': 'ดร. สมชาย ใจดี (ผู้ร่วมวิจัย)',
            'format': 'application/pdf',
            'source': 'Journal of Cybersecurity Research Vol.18 No.2',
            'language': 'en',
            'relation': None,
            'coverage': 'สากล; 2023-2024',
            'rights': 'CC BY 4.0',
            'category_id': 4,  # ความมั่นคงปลอดภัย
            'user_id': 5,  # wichai
            'tags': [tags[7], tags[9], tags[5]]  # IoT, Cybersecurity, Big Data
        },
        {
            'title': 'การประยุกต์ใช้ Blockchain ในระบบจัดการห่วงโซ่อุปทาน',
            'title_en': 'Blockchain Application in Supply Chain Management',
            'authors': 'ผศ.ดร. เพ็ญศรี สุขใจ, รศ.ดร. วิชัย พัฒนา',
            'abstract': 'การนำเทคโนโลยี Blockchain มาประยุกต์ใช้ในการจัดการห่วงโซ่อุปทาน เพื่อเพิ่มความโปร่งใสและความน่าเชื่อถือในการติดตามสินค้า ระบบทดลองแสดงให้เห็นการลดเวลาในการตรวจสอบข้อมูลลง 60%',
            'keywords': 'Blockchain, Supply Chain, Smart Contract, Distributed Ledger',
            'year': 2023,
            'publication_type': 'การประชุม',
            'journal_name': 'International Conference on Blockchain Technology',
            'volume': None,
            'issue': None,
            'pages': '201-215',
            'doi': '10.1234/icbt.2023.025',
            'url': 'https://example.com/research4',
            'view_count': 178,
            'download_count': 65,
            # Dublin Core metadata
            'publisher': 'ACM Digital Library',
            'contributor': 'รศ.ดร. วิชัย พัฒนา (ผู้ร่วมวิจัย)',
            'format': 'application/pdf',
            'source': 'Proceedings of ICBT 2023',
            'language': 'en',
            'relation': None,
            'coverage': 'สากล; 2022-2023',
            'rights': 'Copyright © 2023 ACM',
            'category_id': 1,  # วิทยาการคอมพิวเตอร์
            'user_id': 3,  # pensri
            'tags': [tags[8], tags[5], tags[20]]  # Blockchain, Big Data, Database
        },
        {
            'title': 'ระบบประมวลผลภาษาธรรมชาติสำหรับภาษาไทย',
            'title_en': 'Natural Language Processing System for Thai Language',
            'authors': 'ดร. สมชาย ใจดี, มานี ขยัน',
            'abstract': 'การพัฒนาระบบประมวลผลภาษาธรรมชาติสำหรับภาษาไทยโดยใช้เทคนิค Transformer และ BERT ระบบสามารถทำการตัดคำ, ติดป้ายกำกับคำ และวิเคราะห์ความรู้สึกได้อย่างมีประสิทธิภาพ',
            'keywords': 'NLP, Thai Language, BERT, Transformer, Text Processing',
            'year': 2024,
            'publication_type': 'วารสาร',
            'journal_name': 'Asian Journal of Computer Science',
            'volume': '25',
            'issue': '3',
            'pages': '134-152',
            'doi': '10.1234/ajcs.2024.012',
            'url': 'https://example.com/research5',
            'view_count': 312,
            'download_count': 124,
            # Dublin Core metadata
            'publisher': 'Asian Academic Press',
            'contributor': 'มานี ขยัน (ผู้ช่วยวิจัย)',
            'format': 'application/pdf',
            'source': 'Asian Journal of Computer Science Vol.25 No.3',
            'language': 'th',
            'relation': 'https://example.com/research1',
            'coverage': 'ประเทศไทย; 2023-2024',
            'rights': 'CC BY-NC 4.0',
            'category_id': 2,  # ปัญญาประดิษฐ์
            'user_id': 2,  # somchai
            'tags': [tags[3], tags[0], tags[1], tags[16]]  # NLP, ML, DL, Python
        },
        {
            'title': 'การพัฒนา Web Application ด้วย Microservices Architecture',
            'title_en': 'Web Application Development with Microservices Architecture',
            'authors': 'ผศ.ดร. เพ็ญศรี สุขใจ',
            'abstract': 'งานวิจัยนี้นำเสนอการออกแบบและพัฒนา Web Application แบบ Scalable โดยใช้สถาปัตยกรรม Microservices พร้อม Container orchestration ด้วย Kubernetes',
            'keywords': 'Microservices, Web Development, Docker, Kubernetes, API',
            'year': 2023,
            'publication_type': 'วารสาร',
            'journal_name': 'International Journal of Software Engineering',
            'volume': '15',
            'issue': '4',
            'pages': '89-107',
            'doi': '10.1234/ijse.2023.019',
            'url': 'https://example.com/research6',
            'view_count': 145,
            'download_count': 56,
            # Dublin Core metadata
            'publisher': 'Springer Nature',
            'contributor': None,
            'format': 'application/pdf',
            'source': 'International Journal of Software Engineering Vol.15 No.4',
            'language': 'en',
            'relation': 'https://example.com/research2',
            'coverage': 'สากล; 2022-2023',
            'rights': 'CC BY 4.0',
            'category_id': 3,  # วิศวกรรมซอฟต์แวร์
            'user_id': 3,  # pensri
            'tags': [tags[15], tags[11], tags[23], tags[18]]  # Microservices, Web, API, JS
        },
        {
            'title': 'การวิเคราะห์ Big Data ด้วย Apache Spark และ Machine Learning',
            'title_en': 'Big Data Analysis with Apache Spark and Machine Learning',
            'authors': 'รศ.ดร. วิชัย พัฒนา',
            'abstract': 'การศึกษาและพัฒนาระบบวิเคราะห์ข้อมูลขนาดใหญ่โดยใช้ Apache Spark ร่วมกับเทคนิค Machine Learning สำหรับการทำนายพฤติกรรมผู้ใช้งาน',
            'keywords': 'Big Data, Apache Spark, Machine Learning, Data Mining',
            'year': 2024,
            'publication_type': 'การประชุม',
            'journal_name': 'International Conference on Big Data',
            'volume': None,
            'issue': None,
            'pages': '45-58',
            'doi': '10.1234/icbd.2024.005',
            'url': 'https://example.com/research7',
            'view_count': 198,
            'download_count': 78,
            # Dublin Core metadata
            'publisher': 'IEEE Xplore',
            'contributor': None,
            'format': 'application/pdf',
            'source': 'Proceedings of ICBD 2024',
            'language': 'en',
            'relation': 'https://example.com/research8',
            'coverage': 'สากล; 2023-2024',
            'rights': 'Copyright © 2024 IEEE',
            'category_id': 5,  # ฐานข้อมูล
            'user_id': 5,  # wichai
            'tags': [tags[5], tags[0], tags[10], tags[16]]  # Big Data, ML, Data Mining, Python
        },
        {
            'title': 'ระบบฐานข้อมูล NoSQL สำหรับ Real-time Analytics',
            'title_en': 'NoSQL Database System for Real-time Analytics',
            'authors': 'ดร. สมชาย ใจดี',
            'abstract': 'การออกแบบและพัฒนาระบบฐานข้อมูล NoSQL โดยใช้ MongoDB และ Redis เพื่อรองรับการวิเคราะห์ข้อมูลแบบ Real-time ในระบบที่มีผู้ใช้งานจำนวนมาก',
            'keywords': 'NoSQL, MongoDB, Redis, Real-time, Database',
            'year': 2023,
            'publication_type': 'วารสาร',
            'journal_name': 'Database Systems Journal',
            'volume': '20',
            'issue': '1',
            'pages': '23-41',
            'doi': '10.1234/dsj.2023.003',
            'url': 'https://example.com/research8',
            'view_count': 167,
            'download_count': 61,
            # Dublin Core metadata
            'publisher': 'Elsevier',
            'contributor': None,
            'format': 'application/pdf',
            'source': 'Database Systems Journal Vol.20 No.1',
            'language': 'en',
            'relation': 'https://example.com/research7',
            'coverage': 'สากล; 2022-2023',
            'rights': 'CC BY-NC-ND 4.0',
            'category_id': 5,  # ฐานข้อมูล
            'user_id': 2,  # somchai
            'tags': [tags[22], tags[20], tags[5]]  # NoSQL, Database, Big Data
        },
    ]

    researches = []
    for research_data in researches_data:
        tags_list = research_data.pop('tags')
        research = Research(**research_data)
        research.tags = tags_list
        db.session.add(research)
        researches.append(research)

    db.session.commit()
    print(f"✅ สร้าง {len(researches)} researches เรียบร้อย")
    return researches

def create_bookmarks(users, researches):
    """สร้างข้อมูล Bookmarks"""
    print("\n🔖 กำลังสร้าง Bookmarks...")

    bookmarks_data = [
        {'user_id': 4, 'research_id': 1},  # manee bookmarks research 1
        {'user_id': 4, 'research_id': 2},  # manee bookmarks research 2
        {'user_id': 4, 'research_id': 5},  # manee bookmarks research 5
        {'user_id': 2, 'research_id': 3},  # somchai bookmarks research 3
        {'user_id': 2, 'research_id': 7},  # somchai bookmarks research 7
        {'user_id': 3, 'research_id': 1},  # pensri bookmarks research 1
        {'user_id': 3, 'research_id': 5},  # pensri bookmarks research 5
        {'user_id': 5, 'research_id': 2},  # wichai bookmarks research 2
        {'user_id': 5, 'research_id': 6},  # wichai bookmarks research 6
    ]

    bookmarks = []
    for bookmark_data in bookmarks_data:
        bookmark = Bookmark(**bookmark_data)
        db.session.add(bookmark)
        bookmarks.append(bookmark)

    db.session.commit()
    print(f"✅ สร้าง {len(bookmarks)} bookmarks เรียบร้อย")
    return bookmarks

def create_comments(users, researches):
    """สร้างข้อมูล Comments"""
    print("\n💬 กำลังสร้าง Comments...")

    comments_data = [
        {
            'content': 'งานวิจัยที่น่าสนใจมากครับ ผลการทดลองแสดงให้เห็นถึงประสิทธิภาพของ YOLO v8 ได้เป็นอย่างดี',
            'rating': 5,
            'user_id': 3,  # pensri
            'research_id': 1
        },
        {
            'content': 'อยากทราบรายละเอียดเกี่ยวกับ dataset ที่ใช้ในการ training ครับ',
            'rating': 4,
            'user_id': 4,  # manee
            'research_id': 1
        },
        {
            'content': 'การนำ Agile มาใช้ในโครงการได้ผลดีจริงๆ ขอบคุณสำหรับงานวิจัยนี้ค่ะ',
            'rating': 5,
            'user_id': 2,  # somchai
            'research_id': 2
        },
        {
            'content': 'ผลการวิจัยด้านความปลอดภัย IoT นี้มีประโยชน์มากสำหรับงานของผมครับ',
            'rating': 5,
            'user_id': 2,  # somchai
            'research_id': 3
        },
        {
            'content': 'การประยุกต์ใช้ Blockchain น่าสนใจมาก แต่อยากทราบเรื่อง performance เพิ่มเติมครับ',
            'rating': 4,
            'user_id': 4,  # manee
            'research_id': 4
        },
        {
            'content': 'ระบบ NLP สำหรับภาษาไทยที่รอคอยมานานค่ะ ทำได้ดีมากเลย',
            'rating': 5,
            'user_id': 3,  # pensri
            'research_id': 5
        },
        {
            'content': 'ผลการทดลองน่าประทับใจครับ อยากดู source code ด้วยครับ',
            'rating': 4,
            'user_id': 4,  # manee
            'research_id': 5
        },
        {
            'content': 'Microservices architecture เป็นแนวทางที่ดีสำหรับ scalability',
            'rating': 5,
            'user_id': 5,  # wichai
            'research_id': 6
        },
        {
            'content': 'การใช้ Apache Spark วิเคราะห์ Big Data ได้ผลลัพธ์ที่ดีครับ',
            'rating': 5,
            'user_id': 3,  # pensri
            'research_id': 7
        },
        {
            'content': 'NoSQL เหมาะกับ real-time analytics จริงๆ ครับ ขอบคุณสำหรับการวิจัยนี้',
            'rating': 4,
            'user_id': 5,  # wichai
            'research_id': 8
        },
    ]

    comments = []
    for comment_data in comments_data:
        comment = Comment(**comment_data)
        db.session.add(comment)
        comments.append(comment)

    db.session.commit()
    print(f"✅ สร้าง {len(comments)} comments เรียบร้อย")
    return comments

def create_audit_logs(users, researches):
    """สร้างข้อมูล Audit Logs"""
    print("\n📝 กำลังสร้าง Audit Logs...")

    logs_data = [
        {
            'user_id': 1,
            'action': 'user.login',
            'resource_type': 'User',
            'resource_id': 1,
            'details': '{"method": "password", "success": true}',
            'ip_address': '192.168.1.100',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'created_at': datetime.utcnow() - timedelta(days=5)
        },
        {
            'user_id': 2,
            'action': 'research.create',
            'resource_type': 'Research',
            'resource_id': 1,
            'details': '{"title": "การพัฒนาระบบตรวจจับวัตถุด้วย Deep Learning"}',
            'ip_address': '192.168.1.101',
            'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
            'created_at': datetime.utcnow() - timedelta(days=4)
        },
        {
            'user_id': 3,
            'action': 'research.create',
            'resource_type': 'Research',
            'resource_id': 2,
            'details': '{"title": "ระบบจัดการงานโครงการด้วย Agile Methodology"}',
            'ip_address': '192.168.1.102',
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64)',
            'created_at': datetime.utcnow() - timedelta(days=3)
        },
        {
            'user_id': 4,
            'action': 'research.view',
            'resource_type': 'Research',
            'resource_id': 1,
            'details': '{"action": "view", "page": "detail"}',
            'ip_address': '192.168.1.103',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'created_at': datetime.utcnow() - timedelta(days=2)
        },
        {
            'user_id': 4,
            'action': 'research.download',
            'resource_type': 'Research',
            'resource_id': 1,
            'details': '{"action": "download", "file_type": "pdf"}',
            'ip_address': '192.168.1.103',
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)',
            'created_at': datetime.utcnow() - timedelta(days=2)
        },
        {
            'user_id': 1,
            'action': 'user.update',
            'resource_type': 'User',
            'resource_id': 3,
            'details': '{"field": "roles", "action": "add_role", "role": "researcher"}',
            'ip_address': '192.168.1.100',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'created_at': datetime.utcnow() - timedelta(days=1)
        },
        {
            'user_id': 5,
            'action': 'research.create',
            'resource_type': 'Research',
            'resource_id': 3,
            'details': '{"title": "การวิเคราะห์ความปลอดภัยของระบบ IoT"}',
            'ip_address': '192.168.1.104',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'created_at': datetime.utcnow() - timedelta(hours=12)
        },
    ]

    logs = []
    for log_data in logs_data:
        log = AuditLog(**log_data)
        db.session.add(log)
        logs.append(log)

    db.session.commit()
    print(f"✅ สร้าง {len(logs)} audit logs เรียบร้อย")
    return logs

def main():
    """ฟังก์ชันหลักสำหรับสร้างข้อมูล mockup ทั้งหมด"""
    app = create_app()

    with app.app_context():
        print("\n" + "="*60)
        print("🚀 เริ่มสร้างข้อมูล Mockup สำหรับระบบจัดการงานวิจัย")
        print("="*60)

        # ลบข้อมูลเดิม
        clear_all_data()

        # สร้างข้อมูลตามลำดับ
        permissions = create_permissions()
        roles = create_roles(permissions)
        users = create_users(roles)
        categories = create_categories()
        tags = create_tags()
        researches = create_researches(users, categories, tags)
        bookmarks = create_bookmarks(users, researches)
        comments = create_comments(users, researches)
        audit_logs = create_audit_logs(users, researches)

        print("\n" + "="*60)
        print("✨ สร้างข้อมูล Mockup เรียบร้อยแล้ว!")
        print("="*60)
        print("\n📊 สรุปข้อมูลที่สร้าง:")
        print(f"   - Users: {len(users)} คน")
        print(f"   - Roles: {len(roles)} บทบาท")
        print(f"   - Permissions: {len(permissions)} สิทธิ์")
        print(f"   - Categories: {len(categories)} หมวดหมู่")
        print(f"   - Tags: {len(tags)} แท็ก")
        print(f"   - Researches: {len(researches)} งานวิจัย")
        print(f"   - Bookmarks: {len(bookmarks)} บุ๊กมาร์ก")
        print(f"   - Comments: {len(comments)} ความคิดเห็น")
        print(f"   - Audit Logs: {len(audit_logs)} รายการ")
        print("\n🔑 ข้อมูลการเข้าสู่ระบบ:")
        print("   Admin:")
        print("     Username: admin")
        print("     Password: 123456")
        print("     Role: admin")
        print("\n   Researchers:")
        print("     Username: somchai | Password: 123456")
        print("     Username: pensri  | Password: 123456")
        print("     Username: wichai  | Password: 123456")
        print("\n   User:")
        print("     Username: manee   | Password: 123456")
        print("\n" + "="*60)

if __name__ == '__main__':
    main()
