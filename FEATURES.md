# ฟีเจอร์ใหม่ - Research Management System

เอกสารนี้อธิบายฟีเจอร์ทั้งหมดที่ได้เพิ่มเข้ามาในระบบจัดการงานวิจัย

## 📋 สารบัญ

1. [การอัพโหลดไฟล์ PDF](#1-การอัพโหลดไฟล์-pdf)
2. [ระบบส่งออกข้อมูล](#2-ระบบส่งออกข้อมูล)
3. [REST API](#3-rest-api)
4. [การจัดรูปแบบการอ้างอิง](#4-การจัดรูปแบบการอ้างอิง)
5. [การค้นหาขั้นสูง](#5-การค้นหาขั้นสูง)
6. [แดชบอร์ดวิเคราะห์และสถิติ](#6-แดชบอร์ดวิเคราะห์และสถิติ)
7. [ระบบบุ๊กมาร์ก](#7-ระบบบุ๊กมาร์ก)
8. [ระบบแสดงความคิดเห็นและให้คะแนน](#8-ระบบแสดงความคิดเห็นและให้คะแนน)
9. [ระบบแท็ก](#9-ระบบแท็ก)
10. [โปรไฟล์ผู้ใช้](#10-โปรไฟล์ผู้ใช้)
11. [การแจ้งเตือนทางอีเมล](#11-การแจ้งเตือนทางอีเมล)

---

## 1. การอัพโหลดไฟล์ PDF

### คุณสมบัติ
- อัพโหลดไฟล์ PDF งานวิจัยได้โดยตรง
- รองรับไฟล์ขนาดสูงสุด 50 MB
- จัดเก็บไฟล์แบบปลอดภัยพร้อมชื่อไฟล์ที่ไม่ซ้ำกัน (timestamp)
- ดาวน์โหลดไฟล์ PDF ได้
- ติดตามจำนวนการดาวน์โหลด

### วิธีใช้งาน
```python
# ในฟอร์มเพิ่ม/แก้ไขงานวิจัย
- เลือกไฟล์ PDF จากช่อง "อัพโหลดไฟล์ PDF"
- ระบบจะบันทึกไฟล์อัตโนมัติเมื่อกดบันทึก
```

### Routes
- `POST /research/add` - อัพโหลดพร้อมสร้างงานวิจัยใหม่
- `POST /research/<id>/edit` - อัพโหลดไฟล์ใหม่แทนที่ไฟล์เก่า
- `GET /research/<id>/download` - ดาวน์โหลดไฟล์ PDF

---

## 2. ระบบส่งออกข้อมูล

### รูปแบบที่รองรับ
1. **CSV** - สำหรับ Excel และโปรแกรมสเปรดชีต
2. **Excel (.xlsx)** - ไฟล์ Excel พร้อมฟอร์แมตสวยงาม
3. **BibTeX** - สำหรับ LaTeX และ Reference Manager
4. **RIS** - สำหรับ EndNote, Mendeley, Zotero

### ข้อมูลที่ส่งออก
- ข้อมูลพื้นฐาน: ชื่อ, ผู้แต่ง, ปี
- ข้อมูลเพิ่มเติม: DOI, URL, คำสำคัญ
- ข้อมูลการตีพิมพ์: วารสาร, เล่ม, ฉบับ, หน้า
- Metadata: หมวดหมู่, ผู้อัพโหลด, วันที่สร้าง

### Routes
- `GET /research/export/csv` - ส่งออกเป็น CSV
- `GET /research/export/excel` - ส่งออกเป็น Excel
- `GET /research/export/bibtex` - ส่งออกเป็น BibTeX
- `GET /research/export/ris` - ส่งออกเป็น RIS

---

## 3. REST API

### API Endpoints

#### Research Endpoints
- `GET /api/v1/researches` - รายการงานวิจัยทั้งหมด
- `GET /api/v1/researches/<id>` - ข้อมูลงานวิจัยตาม ID
- `POST /api/v1/researches` - สร้างงานวิจัยใหม่
- `PUT /api/v1/researches/<id>` - แก้ไขงานวิจัย
- `DELETE /api/v1/researches/<id>` - ลบงานวิจัย

#### Category Endpoints
- `GET /api/v1/categories` - รายการหมวดหมู่ทั้งหมด
- `GET /api/v1/categories/<id>` - ข้อมูลหมวดหมู่ตาม ID

#### Tag Endpoints
- `GET /api/v1/tags` - รายการแท็กทั้งหมด

#### Bookmark Endpoints
- `GET /api/v1/bookmarks` - รายการบุ๊กมาร์กของผู้ใช้
- `POST /api/v1/bookmarks/<research_id>` - เพิ่มบุ๊กมาร์ก
- `DELETE /api/v1/bookmarks/<research_id>` - ลบบุ๊กมาร์ก

#### Comment Endpoints
- `GET /api/v1/researches/<id>/comments` - รายการคอมเมนต์
- `POST /api/v1/researches/<id>/comments` - เพิ่มคอมเมนต์

#### Statistics Endpoint
- `GET /api/v1/statistics` - สถิติของระบบ

### Query Parameters
```
GET /api/v1/researches?page=1&per_page=10&search=machine learning&category_id=1&publication_type=journal&year=2023&sort_by=view_count&order=DESC
```

### Response Format
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## 4. การจัดรูปแบบการอ้างอิง

### รูปแบบที่รองรับ
1. **APA** (American Psychological Association)
2. **MLA** (Modern Language Association)
3. **Chicago** (Chicago Manual of Style)
4. **BibTeX** (LaTeX)
5. **RIS** (Research Information Systems)

### ตัวอย่างผลลัพธ์

**APA:**
```
Smith, J., & Johnson, M. (2023). Machine Learning Applications. Journal of AI Research, 15(3), 45-67. https://doi.org/10.1234/example
```

**MLA:**
```
Smith, J., and M. Johnson. "Machine Learning Applications." Journal of AI Research 15.3 (2023): 45-67.
```

**BibTeX:**
```bibtex
@article{research123,
  author = {Smith, J. and Johnson, M.},
  title = {Machine Learning Applications},
  journal = {Journal of AI Research},
  year = {2023},
  volume = {15},
  number = {3},
  pages = {45-67},
  doi = {10.1234/example}
}
```

### วิธีใช้งาน
- แสดงอัตโนมัติในหน้ารายละเอียดงานวิจัย
- คัดลอกรูปแบบที่ต้องการได้ทันที

---

## 5. การค้นหาขั้นสูง

### ตัวกรองที่รองรับ
- **คำค้นหา**: ค้นหาในชื่อ, ชื่อภาษาอังกฤษ, ผู้แต่ง, คำสำคัญ
- **หมวดหมู่**: กรองตามหมวดหมู่
- **ประเภทการตีพิมพ์**: วารสาร, การประชุม, วิทยานิพนธ์, รายงาน
- **ช่วงปี**: ปีเริ่มต้น - ปีสิ้นสุด
- **แท็ก**: ค้นหาตามแท็ก (หลายแท็กได้)

### ตัวเลือกการเรียงลำดับ
- วันที่สร้าง (ใหม่-เก่า / เก่า-ใหม่)
- ชื่อ (ก-ฮ)
- ปี (มาก-น้อย / น้อย-มาก)
- ความนิยม (จำนวนการดู)

### ตัวอย่าง URL
```
/research/?search=AI&category=1&publication_type=journal&year_from=2020&year_to=2023&tags=machine learning,deep learning&sort_by=view_count
```

---

## 6. แดชบอร์ดวิเคราะห์และสถิติ

### สถิติที่แสดง

#### สถิติทั่วไป
- จำนวนงานวิจัยทั้งหมด
- จำนวนผู้ใช้
- จำนวนหมวดหมู่
- จำนวนแท็ก
- จำนวนบุ๊กมาร์ก
- จำนวนความคิดเห็น

#### สถิติแบบกราฟ
- **กราฟประเภทการตีพิมพ์**: แสดงสัดส่วนแต่ละประเภท
- **กราฟจำนวนงานวิจัยตามปี**: 10 ปีล่าสุด
- **กราฟจำนวนตามหมวดหมู่**: เปรียบเทียบหมวดหมู่

#### รายการอันดับ
- งานวิจัยยอดนิยม (Top 10 ตามจำนวนการดู)
- งานวิจัยล่าสุด (10 รายการ)
- แท็กยอดนิยม (Top 10)
- ผู้มีส่วนร่วมสูงสุด (Top 10)

### Route
- `GET /analytics` - แดชบอร์ดวิเคราะห์

---

## 7. ระบบบุ๊กมาร์ก

### คุณสมบัติ
- บันทึกงานวิจัยที่สนใจ
- เข้าถึงบุ๊กมาร์กได้ง่าย
- จัดการบุ๊กมาร์กส่วนตัว
- ป้องกันการบุ๊กมาร์กซ้ำ

### Routes
- `POST /research/<id>/bookmark/add` - เพิ่มบุ๊กมาร์ก
- `POST /research/<id>/bookmark/remove` - ลบบุ๊กมาร์ก
- `GET /bookmarks` - รายการบุ๊กมาร์กทั้งหมด

---

## 8. ระบบแสดงความคิดเห็นและให้คะแนน

### คุณสมบัติ
- แสดงความคิดเห็นในงานวิจัย
- ให้คะแนน 1-5 ดาว
- คำนวณคะแนนเฉลี่ย
- แก้ไข/ลบความคิดเห็นของตัวเอง
- Admin สามารถลบความคิดเห็นใดก็ได้

### Routes
- `POST /research/<id>` - เพิ่มความคิดเห็น (ในหน้า view)
- `POST /research/comment/<comment_id>/delete` - ลบความคิดเห็น

### Database Schema
```sql
Table: comments
- id (PK)
- content (TEXT)
- rating (INTEGER, 1-5)
- user_id (FK)
- research_id (FK)
- created_at
- updated_at
```

---

## 9. ระบบแท็ก

### คุณสมบัติ
- เพิ่มแท็กได้หลายแท็กต่องานวิจัย
- แท็กถูกสร้างอัตโนมัติ (ถ้ายังไม่มี)
- ค้นหาตามแท็กได้
- แสดงจำนวนงานวิจัยต่อแท็ก
- หน้ารวมแท็กทั้งหมด

### Routes
- `GET /research/tags` - รายการแท็กทั้งหมด
- `GET /research/tag/<tag_id>` - งานวิจัยตามแท็ก

### วิธีใช้งาน
```
# ในฟอร์มเพิ่ม/แก้ไขงานวิจัย
แท็ก: machine learning, AI, deep learning, neural networks

# ระบบจะแยกแท็กอัตโนมัติโดยใช้ , (comma)
```

---

## 10. โปรไฟล์ผู้ใช้

### คุณสมบัติโปรไฟล์
- แก้ไขข้อมูลส่วนตัว (ชื่อ, อีเมล)
- เพิ่มประวัติส่วนตัว (Bio)
- อัพโหลดรูปโปรไฟล์
- ตั้งค่าการแจ้งเตือนทางอีเมล

### สถิติส่วนตัว
- จำนวนงานวิจัยที่สร้าง
- จำนวนบุ๊กมาร์ก
- จำนวนความคิดเห็น
- รายการงานวิจัยทั้งหมด

### Routes
- `GET /profile` - หน้าโปรไฟล์ของตัวเอง
- `GET /profile/edit` - แก้ไขโปรไฟล์
- `GET /user/<user_id>` - ดูโปรไฟล์ผู้ใช้อื่น

---

## 11. การแจ้งเตือนทางอีเมล

### คุณสมบัติ
- ตั้งค่าการรับอีเมลแจ้งเตือน
- แจ้งเตือนเมื่อมีงานวิจัยใหม่ (อนาคต)
- แจ้งเตือนเมื่อมีความคิดเห็นใหม่ (อนาคต)

### Configuration
ตั้งค่าในไฟล์ `.env`:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_password
MAIL_DEFAULT_SENDER=noreply@research.local
```

---

## 📊 Database Schema เพิ่มเติม

### ตารางใหม่

#### `tags`
```sql
- id (PK)
- name (UNIQUE)
- created_at
```

#### `bookmarks`
```sql
- id (PK)
- user_id (FK)
- research_id (FK)
- created_at
- UNIQUE(user_id, research_id)
```

#### `comments`
```sql
- id (PK)
- content (TEXT)
- rating (INTEGER)
- user_id (FK)
- research_id (FK)
- created_at
- updated_at
```

#### `research_tags` (Many-to-Many)
```sql
- research_id (FK, PK)
- tag_id (FK, PK)
```

### ฟิลด์เพิ่มเติมในตาราง `researches`
```sql
- file_size (INTEGER)
- view_count (INTEGER, default=0)
- download_count (INTEGER, default=0)
```

### ฟิลด์เพิ่มเติมในตาราง `users`
```sql
- bio (TEXT)
- avatar (VARCHAR)
- email_notifications (BOOLEAN, default=True)
```

---

## 🔧 การติดตั้งและการใช้งาน

### ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### สร้างฐานข้อมูล
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
```

### รันแอปพลิเคชัน
```bash
python run.py
```

### เข้าถึง API
```
http://localhost:5000/api/v1/researches
```

---

## 📱 การใช้งาน API

### ตัวอย่างการเรียกใช้ API

#### ดึงรายการงานวิจัย
```bash
curl http://localhost:5000/api/v1/researches
```

#### สร้างงานวิจัยใหม่
```bash
curl -X POST http://localhost:5000/api/v1/researches \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Machine Learning Research",
    "authors": "John Doe",
    "year": 2023
  }'
```

#### ค้นหางานวิจัย
```bash
curl "http://localhost:5000/api/v1/researches?search=AI&category_id=1&year=2023"
```

---

## 🎯 สรุปฟีเจอร์ทั้งหมด

✅ **การจัดการไฟล์**
- อัพโหลด PDF
- ดาวน์โหลดไฟล์
- ติดตามการดาวน์โหลด

✅ **การส่งออกข้อมูล**
- CSV, Excel, BibTeX, RIS

✅ **REST API**
- CRUD operations
- การค้นหาและกรอง
- Pagination
- CORS Support

✅ **การอ้างอิง**
- APA, MLA, Chicago, BibTeX, RIS

✅ **การค้นหา**
- ค้นหาแบบเต็มรูปแบบ
- กรองหลายเงื่อนไข
- เรียงลำดับได้หลายรูปแบบ

✅ **Analytics**
- สถิติแบบเรียลไทม์
- กราฟและแผนภูมิ
- อันดับยอดนิยม

✅ **Social Features**
- บุ๊กมาร์ก
- ความคิดเห็น
- คะแนน
- แท็ก

✅ **User Management**
- โปรไฟล์
- รูปโปรไฟล์
- สถิติส่วนตัว

✅ **Notifications**
- การแจ้งเตือนทางอีเมล

---

## 📝 หมายเหตุ

- ระบบรองรับทั้งภาษาไทยและภาษาอังกฤษ
- ใช้ SQLite เป็น Database (สามารถเปลี่ยนเป็น PostgreSQL/MySQL ได้)
- รองรับการ Deploy บน Production
- มี Security features: CSRF Protection, Password Hashing, Input Validation

---

## 🚀 การพัฒนาในอนาคต

- [ ] การอัพโหลดหลายไฟล์
- [ ] Full-text search ในไฟล์ PDF
- [ ] Social sharing
- [ ] Notification system แบบ real-time
- [ ] Admin panel
- [ ] Dashboard แบบ interactive
- [ ] Mobile app
- [ ] AI-powered recommendations

---

**เวอร์ชัน**: 2.0
**อัพเดตล่าสุด**: 2025-11-05
