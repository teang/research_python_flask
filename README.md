# ระบบจัดเก็บงานวิจัย (Research Management System)

ระบบจัดการและค้นหางานวิจัยออนไลน์ที่พัฒนาด้วย Flask Framework รองรับภาษาไทยและอังกฤษ

## ✨ คุณสมบัติหลัก

- 🔐 **ระบบสมาชิก** - ลงทะเบียนและเข้าสู่ระบบอย่างปลอดภัย
- 📚 **จัดการงานวิจัย** - เพิ่ม แก้ไข ลบ และดูรายละเอียดงานวิจัย
- 🔍 **ค้นหางานวิจัย** - ค้นหาจากชื่อเรื่อง ผู้วิจัย คำสำคัญ
- 📁 **จัดหมวดหมู่** - จัดกลุ่มงานวิจัยตามหมวดหมู่
- 📊 **แดชบอร์ด** - ติดตามงานวิจัยของตนเอง
- 🎨 **UI สวยงาม** - ใช้ Bootstrap 5 รองรับ Responsive Design
- 🌐 **รองรับภาษาไทย** - Interface และฐานข้อมูลรองรับภาษาไทยเต็มรูปแบบ

## 📋 ข้อมูลที่เก็บในแต่ละงานวิจัย

- ชื่อเรื่อง (ภาษาไทยและภาษาอังกฤษ)
- รายชื่อผู้วิจัย
- บทคัดย่อ
- คำสำคัญ
- ปีที่เผยแพร่
- ประเภทการตีพิมพ์ (วารสาร, การประชุม, วิทยานิพนธ์)
- ชื่อวารสาร/การประชุม
- เล่มที่, ฉบับที่, หน้า
- DOI
- URL
- ที่อยู่ไฟล์
- หมวดหมู่

## 🛠️ เทคโนโลยีที่ใช้

- **Backend:** Flask 3.0
- **Database:** SQLite (สามารถเปลี่ยนเป็น PostgreSQL, MySQL ได้)
- **ORM:** Flask-SQLAlchemy
- **Authentication:** Flask-Login
- **Forms:** Flask-WTF + WTForms
- **Frontend:** Bootstrap 5 + Bootstrap Icons
- **Template Engine:** Jinja2

## 📦 การติดตั้ง

### ความต้องการของระบบ

- Python 3.8 หรือสูงกว่า
- pip (Python package manager)

### ขั้นตอนการติดตั้ง

1. **Clone โปรเจกต์**
```bash
git clone <repository-url>
cd research_python_flask
```

2. **สร้าง Virtual Environment**
```bash
python -m venv venv

# บน Linux/Mac
source venv/bin/activate

# บน Windows
venv\Scripts\activate
```

3. **ติดตั้ง Dependencies**
```bash
pip install -r requirements.txt
```

4. **ตั้งค่า Environment Variables**
```bash
cp .env.example .env
# แก้ไขไฟล์ .env ตามต้องการ
```

5. **รันแอพพลิเคชัน**
```bash
python run.py
```

6. **เปิดเบราว์เซอร์**
```
http://localhost:5000
```

## 🚀 การใช้งาน

### การลงทะเบียนผู้ใช้ใหม่

1. คลิกที่ "ลงทะเบียน" บนแถบเมนู
2. กรอกข้อมูล: ชื่อผู้ใช้, อีเมล, ชื่อ-นามสกุล, รหัสผ่าน
3. คลิก "ลงทะเบียน"

### การเพิ่มงานวิจัย

1. เข้าสู่ระบบ
2. คลิก "เพิ่มงานวิจัย" จากเมนู
3. กรอกข้อมูลงานวิจัย (ฟิลด์ที่มี * จำเป็นต้องกรอก)
4. คลิก "บันทึก"

### การค้นหางานวิจัย

1. ไปที่หน้า "งานวิจัยทั้งหมด"
2. ใช้ช่องค้นหาเพื่อค้นหาจากชื่อเรื่อง, ผู้วิจัย, คำสำคัญ
3. หรือกรองตามหมวดหมู่ทางด้านซ้าย

### การจัดการหมวดหมู่

1. ไปที่หน้า "หมวดหมู่"
2. คลิก "เพิ่มหมวดหมู่" (ต้องเข้าสู่ระบบ)
3. กรอกชื่อและรายละเอียดหมวดหมู่
4. คลิก "บันทึก"

## 📁 โครงสร้างโปรเจกต์

```
research_python_flask/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── routes.py            # Routes และ views
│   ├── forms.py             # WTForms
│   ├── static/              # Static files (CSS, JS)
│   │   └── css/
│   │       └── style.css
│   └── templates/           # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── dashboard.html
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       └── research/
│           ├── list.html
│           ├── view.html
│           ├── form.html
│           ├── categories.html
│           └── category_form.html
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables example
├── .gitignore              # Git ignore rules
└── README.md               # คุณกำลังอ่านอยู่!
```

## 🔒 ความปลอดภัย

- รหัสผ่านเข้ารหัสด้วย Werkzeug
- CSRF Protection ด้วย Flask-WTF
- Session Management ด้วย Flask-Login
- SQL Injection Protection ด้วย SQLAlchemy ORM

## 🔧 การปรับแต่ง

### เปลี่ยนฐานข้อมูล

แก้ไขใน `config.py`:
```python
# PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/dbname'

# MySQL
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/dbname'
```

### เปลี่ยน Secret Key

แก้ไขใน `.env`:
```
SECRET_KEY=your-new-secret-key-here
```

### เปลี่ยน Port

แก้ไขใน `.env`:
```
PORT=8000
```

## 📝 To-Do / ฟีเจอร์ในอนาคต

- [ ] อัพโหลดไฟล์ PDF
- [ ] Export ข้อมูลเป็น CSV, Excel
- [ ] Advanced Search with filters
- [ ] User roles (Admin, Editor, Viewer)
- [ ] REST API
- [ ] Citation formatting (APA, MLA, etc.)
- [ ] สถิติและรายงาน
- [ ] Email notifications

## 🤝 การมีส่วนร่วม

ยินดีรับ Pull Requests! สำหรับการเปลี่ยนแปลงใหญ่ กรุณาเปิด Issue เพื่อหารือก่อน

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

## 👨‍💻 ผู้พัฒนา

พัฒนาโดย Claude Code สำหรับการศึกษาและใช้งานจริง

## 📞 ติดต่อ / รายงานปัญหา

หากพบปัญหาหรือมีข้อเสนอแนะ กรุณาเปิด Issue ใน GitHub

---

**Happy Researching! 📚✨**
