# 📚 ระบบจัดเก็บงานวิจัย (Research Management System)

ระบบจัดการและค้นหางานวิจัยออนไลน์แบบครบวงจร พัฒนาด้วย Flask Framework รองรับภาษาไทยและอังกฤษ พร้อมฟีเจอร์ขั้นสูงสำหรับการจัดการงานวิจัยอย่างมืออาชีพ

## ✨ คุณสมบัติหลัก

### 🔐 ระบบสมาชิกและความปลอดภัย
- **ลงทะเบียนและเข้าสู่ระบบ** - ระบบ Authentication ที่ปลอดภัยด้วย Flask-Login
- **จัดการโปรไฟล์** - แก้ไขข้อมูลส่วนตัว, รูปโปรไฟล์, ประวัติ
- **สิทธิ์ผู้ใช้** - แยกสิทธิ์ Admin และ User ทั่วไป
- **การแจ้งเตือน** - รับการแจ้งเตือนทางอีเมล (ถ้าเปิดใช้งาน)

### 📚 จัดการงานวิจัย
- **CRUD ครบวงจร** - เพิ่ม แก้ไข ลบ และดูรายละเอียดงานวิจัย
- **อัพโหลด PDF** - อัพโหลดไฟล์ PDF พร้อมระบบจัดเก็บที่ปลอดภัย
- **ดาวน์โหลดไฟล์** - ดาวน์โหลด PDF พร้อมนับจำนวนดาวน์โหลด
- **จัดการหมวดหมู่** - จัดกลุ่มงานวิจัยตามหมวดหมู่ที่กำหนดเอง
- **ระบบแท็ก (Tags)** - เพิ่มแท็กเพื่อจัดหมวดหมู่แบบยืดหยุ่น
- **ติดตามสถิติ** - นับจำนวนการดูและดาวน์โหลดแต่ละงานวิจัย

### 🔍 ค้นหาและกรองข้อมูล
- **ค้นหาแบบเต็มรูปแบบ** - ค้นหาจากชื่อเรื่อง, ผู้วิจัย, คำสำคัญ
- **ค้นหาขั้นสูง (Advanced Search)** - กรองตาม:
  - หมวดหมู่
  - ประเภทการตีพิมพ์ (วารสาร, การประชุม, วิทยานิพนธ์)
  - ช่วงปีที่เผยแพร่
  - แท็ก
- **เรียงลำดับ** - จัดเรียงตามวันที่, ชื่อ, ปี, จำนวนการดู
- **Pagination** - แบ่งหน้าเพื่อการแสดงผลที่รวดเร็ว

### 💬 ระบบโต้ตอบและบุ๊กมาร์ก
- **คอมเมนต์และรีวิว** - แสดงความคิดเห็นและให้คะแนนงานวิจัย
- **ระบบเรตติ้ง** - ให้คะแนน 1-5 ดาว พร้อมคำนวณค่าเฉลี่ย
- **บุ๊กมาร์ก** - บันทึกงานวิจัยที่สนใจสำหรับอ่านภายหลัง
- **จัดการคอมเมนต์** - ลบคอมเมนต์ของตนเอง หรือ Admin ลบได้ทั้งหมด

### 📊 แดชบอร์ดและสถิติ
- **Dashboard ผู้ใช้** - ติดตามงานวิจัยของตนเอง
- **Analytics Dashboard** - แดชบอร์ดวิเคราะห์ข้อมูลแบบละเอียด:
  - สถิติทั่วไป (จำนวนงานวิจัย, ผู้ใช้, หมวดหมู่)
  - สถิติตามประเภทการตีพิมพ์
  - สถิติตามปี
  - สถิติตามหมวดหมู่
  - งานวิจัยยอดนิยม (Top 10)
  - แท็กยอดนิยม
  - ผู้ใช้ที่มีงานวิจัยมากที่สุด
- **หน้าโปรไฟล์** - แสดงสถิติส่วนตัวของแต่ละผู้ใช้

### 📤 ส่งออกและการอ้างอิง
- **Export หลายรูปแบบ**:
  - CSV - สำหรับ Excel และโปรแกรมสเปรดชีต
  - Excel (XLSX) - รูปแบบ Microsoft Excel
  - BibTeX - สำหรับ LaTeX และ Reference Manager
  - RIS - สำหรับ EndNote, Mendeley, Zotero
- **จัดรูปแบบการอ้างอิง** - แสดงในหน้ารายละเอียดงานวิจัย:
  - APA (American Psychological Association)
  - MLA (Modern Language Association)
  - Chicago
  - BibTeX
- **คัดลอกได้ง่าย** - คัดลอกการอ้างอิงเพียงคลิกเดียว

### 🚀 REST API
- **API สำหรับนักพัฒนา** - REST API เต็มรูปแบบพร้อมเอกสาร
- **Endpoints ครบถ้วน**:
  - งานวิจัย (GET, POST, PUT, DELETE)
  - หมวดหมู่ (GET)
  - แท็ก (GET)
  - บุ๊กมาร์ก (GET, POST, DELETE)
  - คอมเมนต์ (GET, POST)
  - สถิติระบบ (GET)
- **รองรับ Pagination และ Filter** - API ที่มีประสิทธิภาพ
- **JSON Response** - รูปแบบการตอบกลับมาตรฐาน

### 🎨 UI/UX สวยงาม
- **Bootstrap 5** - ดีไซน์ทันสมัยและตอบสนอง
- **Bootstrap Icons** - ไอคอนสวยงามและชัดเจน
- **Responsive Design** - รองรับทุกขนาดหน้าจอ (Desktop, Tablet, Mobile)
- **รองรับภาษาไทย** - Interface และฐานข้อมูลรองรับภาษาไทยเต็มรูปแบบ

## 📋 ข้อมูลที่เก็บในแต่ละงานวิจัย

### ข้อมูลพื้นฐาน
- ชื่อเรื่อง (ภาษาไทย) *
- ชื่อเรื่อง (ภาษาอังกฤษ)
- รายชื่อผู้วิจัย *
- บทคัดย่อ
- คำสำคัญ
- ปีที่เผยแพร่

### ข้อมูลการตีพิมพ์
- ประเภทการตีพิมพ์ (วารสาร/journal, การประชุม/conference, วิทยานิพนธ์/thesis, รายงาน/report, อื่นๆ/other)
- ชื่อวารสาร/การประชุม
- เล่มที่ (Volume)
- ฉบับที่ (Issue)
- หน้า (Pages)
- DOI (Digital Object Identifier)
- URL

### ข้อมูลเพิ่มเติม
- ไฟล์ PDF (อัพโหลดได้)
- ขนาดไฟล์
- หมวดหมู่
- แท็ก (Tags)
- ผู้อัพโหลด
- วันที่สร้าง/แก้ไข
- จำนวนการดู
- จำนวนการดาวน์โหลด
- คะแนนเฉลี่ยจากผู้ใช้

**หมายเหตุ**: ฟิลด์ที่มีเครื่องหมาย * จำเป็นต้องกรอก

## 🛠️ เทคโนโลยีที่ใช้

### Backend
- **Flask 3.0** - Web Framework หลัก
- **Flask-SQLAlchemy** - ORM สำหรับจัดการฐานข้อมูล
- **Flask-Login** - จัดการ Authentication
- **Flask-WTF + WTForms** - จัดการ Forms และ Validation
- **Werkzeug** - เข้ารหัสรหัสผ่านและจัดการไฟล์

### Database
- **SQLite** - ฐานข้อมูลเริ่มต้น (สามารถเปลี่ยนเป็น PostgreSQL, MySQL ได้)

### Frontend
- **Bootstrap 5** - CSS Framework
- **Bootstrap Icons** - ไอคอนเซ็ต
- **Jinja2** - Template Engine
- **JavaScript (Vanilla)** - สำหรับ Interactive Features

### Libraries เพิ่มเติม
- **Pandas** - สำหรับ Export CSV/Excel
- **OpenPyXL** - สำหรับ Excel Writer

## 📦 การติดตั้งและเริ่มใช้งาน

### ความต้องการของระบบ

- **Python** 3.8 หรือสูงกว่า
- **pip** (Python package manager)
- **Git** (สำหรับ Clone โปรเจกต์)

### ขั้นตอนที่ 1: Clone โปรเจกต์

```bash
git clone <repository-url>
cd research_python_flask
```

### ขั้นตอนที่ 2: สร้าง Virtual Environment

สร้าง Virtual Environment เพื่อแยกการติดตั้ง Package จากระบบหลัก

```bash
# สร้าง Virtual Environment
python -m venv venv

# เปิดใช้งาน Virtual Environment
# บน Linux/Mac
source venv/bin/activate

# บน Windows
venv\Scripts\activate
```

**หมายเหตุ**: เมื่อเปิดใช้งาน Virtual Environment จะเห็น `(venv)` ที่หน้า Terminal

### ขั้นตอนที่ 3: ติดตั้ง Dependencies

ติดตั้ง Package ทั้งหมดที่จำเป็นจากไฟล์ `requirements.txt`

```bash
pip install -r requirements.txt
```

Package ที่จะถูกติดตั้ง:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Pandas
- OpenPyXL
- และอื่นๆ

### ขั้นตอนที่ 4: ตั้งค่า Environment Variables (ถ้ามี)

```bash
# คัดลอกไฟล์ตัวอย่าง
cp .env.example .env

# แก้ไขไฟล์ .env ตามต้องการ
# ตัวอย่าง:
# SECRET_KEY=your-secret-key-here
# DATABASE_URI=sqlite:///research.db
# PORT=5000
```

**หมายเหตุ**: ถ้าไม่มีไฟล์ `.env.example` สามารถข้ามขั้นตอนนี้ได้ ระบบจะใช้ค่า Default

### ขั้นตอนที่ 5: สร้างฐานข้อมูล (ครั้งแรกเท่านั้น)

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...
>>> exit()
```

หรือถ้ามีไฟล์ `init_db.py`:

```bash
python init_db.py
```

### ขั้นตอนที่ 6: รันแอปพลิเคชัน

```bash
python run.py
```

แอปพลิเคชันจะทำงานที่ `http://localhost:5000`

### ขั้นตอนที่ 7: เปิดเบราว์เซอร์

เปิดเบราว์เซอร์และเข้าไปที่:

```
http://localhost:5000
```

## 🚀 คู่มือการใช้งาน

### 1. การลงทะเบียนผู้ใช้ใหม่

1. คลิกปุ่ม **"ลงทะเบียน"** บนแถบเมนูด้านบน
2. กรอกข้อมูลในแบบฟอร์ม:
   - **ชื่อผู้ใช้** (Username) - ห้ามซ้ำกับผู้อื่น
   - **อีเมล** - ต้องเป็นอีเมลที่ถูกต้องและไม่ซ้ำ
   - **ชื่อ-นามสกุล** (Full Name)
   - **รหัสผ่าน** - ความยาวอย่างน้อย 8 ตัวอักษร
   - **ยืนยันรหัสผ่าน**
3. คลิก **"ลงทะเบียน"**
4. เมื่อสำเร็จ ระบบจะนำไปหน้า Login

### 2. การเข้าสู่ระบบ

1. คลิกปุ่ม **"เข้าสู่ระบบ"** บนแถบเมนู
2. กรอก **ชื่อผู้ใช้** และ **รหัสผ่าน**
3. คลิก **"เข้าสู่ระบบ"**
4. ระบบจะนำไปหน้า Dashboard

### 3. การเพิ่มงานวิจัยใหม่

1. เข้าสู่ระบบก่อน (ต้อง Login)
2. คลิก **"เพิ่มงานวิจัย"** จากเมนูหลัก
3. กรอกข้อมูลในแบบฟอร์ม:
   - **ข้อมูลพื้นฐาน**: ชื่อเรื่อง, ผู้วิจัย, บทคัดย่อ, คำสำคัญ
   - **ข้อมูลการตีพิมพ์**: ประเภท, วารสาร, เล่มที่, ฉบับที่, หน้า, DOI, URL
   - **หมวดหมู่และแท็ก**: เลือกหมวดหมู่, เพิ่มแท็ก (คั่นด้วยเครื่องหมายจุลภาค)
   - **ไฟล์ PDF**: อัพโหลดไฟล์ (ถ้ามี)
4. คลิก **"บันทึก"**
5. ระบบจะแสดงหน้ารายละเอียดงานวิจัยที่เพิ่ม

**เคล็ดลับ**:
- ฟิลด์ที่มี * สีแดง จำเป็นต้องกรอก
- แท็กช่วยให้ค้นหาได้ง่ายขึ้น แนะนำให้เพิ่มแท็กที่เกี่ยวข้อง

### 4. การแก้ไขงานวิจัย

1. เข้าไปในหน้ารายละเอียดงานวิจัยที่ต้องการแก้ไข
2. คลิกปุ่ม **"แก้ไข"** (แสดงเฉพาะเจ้าของหรือ Admin)
3. แก้ไขข้อมูลตามต้องการ
4. คลิก **"บันทึก"**

**หมายเหตุ**: สามารถแก้ไขได้เฉพาะงานวิจัยของตนเอง หรือเป็น Admin

### 5. การลบงานวิจัย

1. เข้าไปในหน้ารายละเอียดงานวิจัย
2. คลิกปุ่ม **"ลบ"** (แสดงเฉพาะเจ้าของหรือ Admin)
3. ยืนยันการลบ
4. งานวิจัยจะถูกลบพร้อมคอมเมนต์และบุ๊กมาร์กที่เกี่ยวข้อง

### 6. การค้นหางานวิจัย

#### ค้นหาแบบง่าย
1. ไปที่หน้า **"งานวิจัยทั้งหมด"**
2. พิมพ์คำค้นหาในช่อง Search
3. กด Enter หรือคลิกปุ่มค้นหา
4. ระบบจะค้นหาจาก: ชื่อเรื่อง, ผู้วิจัย, คำสำคัญ

#### ค้นหาแบบขั้นสูง
1. ใช้ตัวกรองด้านซ้าย:
   - **หมวดหมู่**: เลือกหมวดหมู่ที่ต้องการ
   - **ประเภทการตีพิมพ์**: เลือกประเภท
   - **ช่วงปี**: ระบุปีเริ่มต้นและสิ้นสุด
   - **แท็ก**: พิมพ์ชื่อแท็ก
2. เลือก**การเรียงลำดับ**:
   - ล่าสุด/เก่าสุด
   - ตามชื่อ A-Z
   - ตามปี (ใหม่-เก่า หรือ เก่า-ใหม่)
   - ยอดนิยม (จำนวนการดู)

### 7. การเพิ่มบุ๊กมาร์ก

1. เข้าไปในหน้ารายละเอียดงานวิจัย หรือในหน้ารายการ
2. คลิกไอคอน **บุ๊กมาร์ก** (รูปดาว)
3. งานวิจัยจะถูกเพิ่มเข้ารายการบุ๊กมาร์ก
4. ดูบุ๊กมาร์กทั้งหมดได้ที่เมนู **"บุ๊กมาร์กของฉัน"**

### 8. การเพิ่มคอมเมนต์และให้คะแนน

1. เข้าไปในหน้ารายละเอียดงานวิจัย
2. เลื่อนลงไปที่ส่วน **"ความคิดเห็น"**
3. พิมพ์คอมเมนต์ในช่อง
4. (ถ้าต้องการ) ให้คะแนน 1-5 ดาว
5. คลิก **"เพิ่มความคิดเห็น"**

**หมายเหตุ**: คะแนนเฉลี่ยจะถูกคำนวณและแสดงที่หน้างานวิจัย

### 9. การจัดการหมวดหมู่

1. ไปที่หน้า **"หมวดหมู่"**
2. คลิก **"เพิ่มหมวดหมู่"** (ต้อง Login)
3. กรอก:
   - **ชื่อหมวดหมู่** (ห้ามซ้ำ)
   - **คำอธิบาย** (ถ้ามี)
4. คลิก **"บันทึก"**

### 10. การดูสถิติและวิเคราะห์ข้อมูล

1. เข้าสู่ระบบก่อน
2. ไปที่เมนู **"Analytics"** หรือ **"สถิติ"**
3. ดูข้อมูล:
   - **ภาพรวมระบบ**: จำนวนงานวิจัย, ผู้ใช้, หมวดหมู่, แท็ก
   - **กราฟแสดง**: สถิติตามประเภท, ปี, หมวดหมู่
   - **Top 10**: งานวิจัยยอดนิยม, แท็กยอดนิยม, ผู้ใช้งานเยอะที่สุด

### 11. การส่งออกข้อมูล (Export)

#### Export ทั้งหมด
1. ไปที่หน้า **"งานวิจัยทั้งหมด"**
2. คลิกปุ่ม **"Export"** ด้านบน
3. เลือกรูปแบบ:
   - **CSV** - สำหรับ Excel
   - **Excel (XLSX)** - สำหรับ Microsoft Excel
   - **BibTeX** - สำหรับ LaTeX
   - **RIS** - สำหรับ EndNote/Mendeley/Zotero
4. ไฟล์จะถูกดาวน์โหลดอัตโนมัติ

#### คัดลอกการอ้างอิง
1. เข้าไปในหน้ารายละเอียดงานวิจัย
2. เลื่อนลงไปที่ส่วน **"การอ้างอิง"**
3. เลือกรูปแบบที่ต้องการ (APA, MLA, Chicago, BibTeX)
4. คลิกปุ่ม **"คัดลอก"** หรือคัดลอกข้อความที่แสดง

### 12. การอัพโหลดและดาวน์โหลด PDF

#### อัพโหลด PDF
1. ขณะเพิ่มหรือแก้ไขงานวิจัย
2. ที่ส่วน **"ไฟล์ PDF"** คลิก **"เลือกไฟล์"**
3. เลือกไฟล์ PDF จากเครื่อง
4. คลิก **"บันทึก"**

#### ดาวน์โหลด PDF
1. เข้าไปในหน้ารายละเอียดงานวิจัย
2. คลิกปุ่ม **"ดาวน์โหลด PDF"** (ถ้ามีไฟล์)
3. ไฟล์จะถูกดาวน์โหลด
4. จำนวนดาวน์โหลดจะเพิ่มขึ้นอัตโนมัติ

### 13. การจัดการโปรไฟล์

1. คลิกที่ **ชื่อผู้ใช้** ด้านบนขวา
2. เลือก **"โปรไฟล์"**
3. คลิก **"แก้ไขโปรไฟล์"**
4. แก้ไขข้อมูล:
   - ชื่อ-นามสกุล
   - อีเมล
   - ประวัติส่วนตัว (Bio)
   - รูปโปรไฟล์
   - การรับการแจ้งเตือนทางอีเมล
5. คลิก **"บันทึก"**

### 14. การใช้งาน REST API

#### ดึงรายการงานวิจัย
```bash
GET /api/v1/researches

# ตัวอย่าง Query Parameters:
# ?page=1&per_page=10
# &search=machine+learning
# &category_id=1
# &publication_type=journal
# &year=2024
# &sort_by=created_at&order=DESC
```

#### ดึงงานวิจัยตาม ID
```bash
GET /api/v1/researches/1
```

#### เพิ่มงานวิจัยใหม่ (ต้อง Login)
```bash
POST /api/v1/researches
Content-Type: application/json

{
  "title": "ชื่องานวิจัย",
  "authors": "ผู้วิจัย",
  "abstract": "บทคัดย่อ",
  "year": 2024,
  "publication_type": "journal"
}
```

#### ดึงสถิติระบบ
```bash
GET /api/v1/statistics
```

**หมายเหตุ**: API บางตัวต้อง Authentication ผ่าน Session Cookie

## 📁 โครงสร้างโปรเจกต์

```
research_python_flask/
│
├── app/                          # โฟลเดอร์แอปพลิเคชันหลัก
│   ├── __init__.py              # Application Factory (สร้างแอป Flask)
│   ├── models.py                # Database Models (User, Research, Category, Tag, Bookmark, Comment)
│   ├── routes.py                # Routes และ Views (main, auth, research)
│   ├── forms.py                 # WTForms สำหรับ Form Validation
│   ├── api.py                   # REST API Endpoints
│   ├── utils.py                 # Utility Functions (export, citation, file upload)
│   │
│   ├── static/                  # Static Files
│   │   ├── css/
│   │   │   └── style.css        # Custom CSS
│   │   ├── js/
│   │   │   └── main.js          # Custom JavaScript
│   │   └── uploads/             # ไฟล์อัพโหลด (PDF, รูปโปรไฟล์)
│   │       ├── researches/      # PDF ของงานวิจัย
│   │       └── avatars/         # รูปโปรไฟล์ผู้ใช้
│   │
│   └── templates/               # HTML Templates (Jinja2)
│       ├── base.html            # Template หลัก
│       ├── index.html           # หน้าแรก
│       ├── dashboard.html       # แดชบอร์ดผู้ใช้
│       ├── analytics.html       # แดชบอร์ดสถิติ
│       ├── bookmarks.html       # หน้าบุ๊กมาร์ก
│       ├── profile.html         # หน้าโปรไฟล์
│       ├── edit_profile.html    # แก้ไขโปรไฟล์
│       ├── user_profile.html    # ดูโปรไฟล์ผู้อื่น
│       │
│       ├── auth/                # Templates สำหรับ Authentication
│       │   ├── login.html       # หน้า Login
│       │   └── register.html    # หน้า Register
│       │
│       └── research/            # Templates สำหรับงานวิจัย
│           ├── list.html        # รายการงานวิจัยทั้งหมด
│           ├── view.html        # รายละเอียดงานวิจัย
│           ├── form.html        # ฟอร์มเพิ่ม/แก้ไขงานวิจัย
│           ├── categories.html  # รายการหมวดหมู่
│           ├── category_form.html # ฟอร์มเพิ่มหมวดหมู่
│           ├── tags.html        # รายการแท็กทั้งหมด
│           └── tag_researches.html # งานวิจัยตามแท็ก
│
├── config.py                    # Configuration Settings
├── run.py                       # Application Entry Point (รันแอป)
├── requirements.txt             # Python Dependencies
├── .env.example                 # ตัวอย่าง Environment Variables
├── .gitignore                   # Git Ignore Rules
├── README.md                    # ไฟล์นี้
│
└── instance/                    # Instance Folder (สร้างอัตโนมัติ)
    └── research.db              # SQLite Database
```

### คำอธิบายไฟล์สำคัญ

#### `app/__init__.py`
- Application Factory Pattern
- สร้างและตั้งค่า Flask app
- ลงทะเบียน Blueprints และ Extensions

#### `app/models.py`
- Database Models:
  - `User` - ผู้ใช้งานระบบ
  - `Research` - งานวิจัย
  - `Category` - หมวดหมู่
  - `Tag` - แท็ก
  - `Bookmark` - บุ๊กมาร์ก
  - `Comment` - คอมเมนต์
- ความสัมพันธ์ (Relationships): One-to-Many, Many-to-Many

#### `app/routes.py`
- Blueprints:
  - `main_bp` - หน้าหลัก, dashboard, analytics, profile, bookmarks
  - `auth_bp` - login, register, logout
  - `research_bp` - CRUD งานวิจัย, หมวดหมู่, แท็ก, บุ๊กมาร์ก, คอมเมนต์, export

#### `app/api.py`
- REST API Endpoints
- รองรับ JSON Request/Response
- Pagination และ Filtering

#### `app/utils.py`
- Utility Functions:
  - `save_uploaded_file()` - อัพโหลดไฟล์
  - `format_citation()` - จัดรูปแบบการอ้างอิง
  - `export_researches_csv/excel/bibtex/ris()` - Export ข้อมูล

#### `app/forms.py`
- WTForms สำหรับ Validation:
  - LoginForm, RegistrationForm
  - ResearchForm, CategoryForm
  - CommentForm, ProfileForm
  - AdvancedSearchForm

## 🔒 ความปลอดภัย

### การเข้ารหัส
- **รหัสผ่าน**: เข้ารหัสด้วย Werkzeug (bcrypt)
- **Session**: จัดการด้วย Flask-Login
- **Secret Key**: ใช้สำหรับเข้ารหัส Session

### การป้องกัน
- **CSRF Protection**: ป้องกัน Cross-Site Request Forgery ด้วย Flask-WTF
- **SQL Injection**: ป้องกันด้วย SQLAlchemy ORM (Parameterized Queries)
- **XSS**: ป้องกันด้วย Jinja2 Auto-escaping
- **File Upload Security**: ตรวจสอบประเภทไฟล์และใช้ secure_filename()

### การควบคุมการเข้าถึง
- **Authentication**: ตรวจสอบด้วย @login_required
- **Authorization**: ตรวจสอบสิทธิ์เจ้าของหรือ Admin
- **API Access**: บาง API ต้อง Login

### คำแนะนำความปลอดภัย
1. **เปลี่ยน SECRET_KEY** ใน production
2. **ใช้ HTTPS** ในการ deploy
3. **อัปเดต Dependencies** เป็นประจำ
4. **สำรองข้อมูล** เป็นประจำ
5. **ตั้งค่า Firewall** และ Rate Limiting

## 🔧 การปรับแต่งและตั้งค่า

### เปลี่ยนฐานข้อมูล

ระบบรองรับฐานข้อมูลหลายประเภท แก้ไขใน `config.py`:

#### PostgreSQL
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/research_db'
```

ติดตั้ง psycopg2:
```bash
pip install psycopg2-binary
```

#### MySQL
```python
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost:3306/research_db'
```

ติดตั้ง PyMySQL:
```bash
pip install pymysql
```

#### SQLite (Default)
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///research.db'
```

### เปลี่ยน Secret Key

แก้ไขใน `.env` หรือ `config.py`:

```python
SECRET_KEY = 'your-new-very-long-secret-key-here'
```

สร้าง Secret Key แบบสุ่ม:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### เปลี่ยน Port

แก้ไขใน `.env`:
```
PORT=8000
```

หรือใน `run.py`:
```python
app.run(host='0.0.0.0', port=8000, debug=True)
```

### ตั้งค่าการอัพโหลดไฟล์

แก้ไขใน `config.py`:

```python
# ขนาดไฟล์สูงสุด (bytes)
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# ประเภทไฟล์ที่อนุญาต
ALLOWED_EXTENSIONS = {'pdf'}

# โฟลเดอร์สำหรับอัพโหลด
UPLOAD_FOLDER = 'app/static/uploads'
```

### ตั้งค่าอีเมล (Flask-Mail)

แก้ไขใน `config.py` และติดตั้ง Flask-Mail:

```bash
pip install Flask-Mail
```

```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'
MAIL_DEFAULT_SENDER = 'your-email@gmail.com'
```

### เพิ่ม Admin User

วิธีที่ 1: ผ่าน Python Shell
```python
python
>>> from app import create_app, db
>>> from app.models import User
>>> app = create_app()
>>> with app.app_context():
...     user = User.query.filter_by(username='yourusername').first()
...     user.is_admin = True
...     db.session.commit()
>>> exit()
```

วิธีที่ 2: แก้ไขในฐานข้อมูลโดยตรง
```sql
UPDATE users SET is_admin = 1 WHERE username = 'yourusername';
```

### ตั้งค่า Pagination

แก้ไขใน `routes.py`:

```python
# เปลี่ยนจำนวนต่อหน้า
researches = query.paginate(page=page, per_page=20, error_out=False)
```

## 🚢 การ Deploy

### Deploy บน Heroku

1. สร้างไฟล์ `Procfile`:
```
web: gunicorn run:app
```

2. ติดตั้ง gunicorn:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

3. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku run python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

### Deploy บน PythonAnywhere

1. อัพโหลดโค้ดไปยัง PythonAnywhere
2. สร้าง Virtual Environment
3. ติดตั้ง Dependencies
4. ตั้งค่า WSGI file
5. Reload แอป

### Deploy บน VPS (Ubuntu/Linux)

1. ติดตั้ง Dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. Clone และติดตั้ง:
```bash
git clone <repo>
cd research_python_flask
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. ติดตั้ง Gunicorn:
```bash
pip install gunicorn
```

4. ตั้งค่า Systemd Service
5. ตั้งค่า Nginx Reverse Proxy
6. ตั้งค่า SSL Certificate (Let's Encrypt)

## 📊 Database Schema

### ตาราง Users
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- full_name
- is_admin
- bio
- avatar
- email_notifications
- created_at

### ตาราง Researches
- id (Primary Key)
- title
- title_en
- authors
- abstract
- keywords
- year
- publication_type
- journal_name
- volume, issue, pages
- doi, url
- file_path, file_size
- view_count, download_count
- category_id (Foreign Key)
- user_id (Foreign Key)
- created_at, updated_at

### ตาราง Categories
- id (Primary Key)
- name (Unique)
- description

### ตาราง Tags
- id (Primary Key)
- name (Unique)

### ตาราง Bookmarks
- id (Primary Key)
- user_id (Foreign Key)
- research_id (Foreign Key)
- created_at

### ตาราง Comments
- id (Primary Key)
- content
- rating (1-5)
- user_id (Foreign Key)
- research_id (Foreign Key)
- created_at, updated_at

### ตาราง research_tags (Many-to-Many)
- research_id (Foreign Key)
- tag_id (Foreign Key)

## 🧪 การทดสอบ

### รันเทส (ถ้ามี)
```bash
pytest
```

### ทดสอบ API ด้วย curl

ดึงรายการงานวิจัย:
```bash
curl http://localhost:5000/api/v1/researches
```

ดึงสถิติ:
```bash
curl http://localhost:5000/api/v1/statistics
```

## 🐛 การแก้ไขปัญหาที่พบบ่อย

### ปัญหา: ไม่สามารถติดตั้ง Dependencies
**วิธีแก้**: อัปเดต pip
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### ปัญหา: ModuleNotFoundError
**วิธีแก้**: ตรวจสอบ Virtual Environment
```bash
which python  # ต้องชี้ไปที่ venv
pip list      # ดู Package ที่ติดตั้ง
```

### ปัญหา: Database Locked (SQLite)
**วิธีแก้**: รีสตาร์ทแอปหรือใช้ฐานข้อมูลอื่น (PostgreSQL, MySQL)

### ปัญหา: File Upload ไม่ทำงาน
**วิธีแก้**:
1. ตรวจสอบสิทธิ์โฟลเดอร์ uploads
2. ตรวจสอบ MAX_CONTENT_LENGTH
3. ตรวจสอบประเภทไฟล์

### ปัญหา: 404 Not Found (หลัง Deploy)
**วิธีแก้**: ตรวจสอบ URL และ Blueprint registration

## 📝 ฟีเจอร์ในอนาคต / To-Do List

- [ ] **Email Notifications** - แจ้งเตือนเมื่อมีคอมเมนต์ใหม่
- [ ] **Advanced Analytics** - กราฟและชาร์ตแบบ Interactive
- [ ] **Full-text Search** - ค้นหาในไฟล์ PDF
- [ ] **Recommendation System** - แนะนำงานวิจัยที่น่าสนใจ
- [ ] **Collaboration** - แชร์และทำงานร่วมกัน
- [ ] **Citation Network** - แสดงความสัมพันธ์ของการอ้างอิง
- [ ] **Multi-language Support** - รองรับหลายภาษา
- [ ] **Dark Mode** - โหมดมืด
- [ ] **Mobile App** - แอปมือถือ (React Native/Flutter)
- [ ] **Import from DOI** - ดึงข้อมูลอัตโนมัติจาก DOI
- [ ] **Batch Upload** - อัพโหลดหลายไฟล์พร้อมกัน
- [ ] **Version Control** - ติดตามการแก้ไขงานวิจัย
- [ ] **Social Features** - Follow ผู้ใช้, Share, Like
- [ ] **Advanced Permissions** - ระบบสิทธิ์แบบละเอียด (Viewer, Editor, Admin)
- [ ] **Backup/Restore** - สำรองและกู้คืนข้อมูล
- [ ] **Audit Log** - บันทึกการเปลี่ยนแปลง

## 🤝 การมีส่วนร่วม (Contributing)

ยินดีรับ Pull Requests และ Contributions!

### ขั้นตอน:
1. Fork โปรเจกต์
2. สร้าง Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add some AmazingFeature'`)
4. Push ไปยัง Branch (`git push origin feature/AmazingFeature`)
5. เปิด Pull Request

### Guidelines:
- เขียนโค้ดตาม PEP 8 (Python Style Guide)
- เพิ่ม Comments และ Docstrings
- ทดสอบโค้ดก่อน Push
- อธิบาย Changes ใน Pull Request

สำหรับการเปลี่ยนแปลงใหญ่ กรุณาเปิด Issue เพื่อหารือก่อน

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 ผู้พัฒนา

พัฒนาด้วย ❤️ โดย **Claude Code** สำหรับการศึกษาและใช้งานจริง

## 📞 ติดต่อ / รายงานปัญหา

- **Issues**: หากพบปัญหาหรือมีข้อเสนอแนะ กรุณาเปิด Issue ใน GitHub
- **Discussions**: สำหรับคำถามและการสนทนาทั่วไป

## 🙏 ขอขอบคุณ

- **Flask** - Web Framework ที่ยอดเยี่ยม
- **Bootstrap** - UI Framework ที่สวยงาม
- **SQLAlchemy** - ORM ที่ทรงพลัง
- **ชุมชน Open Source** - สำหรับ Libraries และเครื่องมือต่างๆ

---

## 📚 เอกสารเพิ่มเติม

### สำหรับผู้ใช้
- [คู่มือการใช้งาน (User Guide)](#-คูมอการใชงาน)
- [FAQ - คำถามที่พบบ่อย](#-การแกไขปญหาทพบบอย)

### สำหรับนักพัฒนา
- [API Documentation](#14-การใชงาน-rest-api)
- [Database Schema](#-database-schema)
- [Project Structure](#-โครงสรางโปรเจกต)

### Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

---

**Happy Researching! 📚✨**

พัฒนาเพื่อส่งเสริมการจัดการงานวิจัยอย่างมีประสิทธิภาพ
