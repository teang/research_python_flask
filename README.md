# ระบบจัดการงานวิจัย (Research Management System)

ระบบจัดการงานวิจัยแบบครบวงจร พัฒนาด้วย Flask Framework พร้อมระบบ RBAC (Role-Based Access Control)

## คุณสมบัติหลัก

- ✅ **MVC Architecture** - โครงสร้างโค้ดแบบ Model-View-Controller
- ✅ **RBAC System** - ระบบจัดการสิทธิ์แบบ Role-Based Access Control
- ✅ **PostgreSQL Database** - ฐานข้อมูล PostgreSQL
- ✅ **Tailwind CSS** - UI ที่สวยงามและ Responsive
- ✅ **Thai Fonts** - ฟอนต์ Kanit (หัวข้อ) และ Sarabun (รายละเอียด)
- ✅ **AdminLTE Style Backend** - Admin panel ที่ใช้งานง่าย
- ✅ **Thai Government Website Style** - Frontend เว็บไซต์ราชการ

## ระบบ RBAC

### บทบาท (Roles)
1. **Admin** - สิทธิ์เต็มในการจัดการระบบ
2. **Editor** - จัดการและเผยแพร่งานวิจัย
3. **Researcher** - จัดการงานวิจัยของตนเอง
4. **Viewer** - ดูงานวิจัยเท่านั้น

## การติดตั้ง

```bash
# 1. Clone repository
git clone <repo>
cd research_python_flask

# 2. สร้าง virtual environment
python -m venv venv
source venv/bin/activate

# 3. ติดตั้ง dependencies
pip install -r requirements.txt

# 4. ตั้งค่า PostgreSQL
# สร้างฐานข้อมูล research_db

# 5. คัดลอก .env
cp .env.example .env
# แก้ไข DATABASE_URL ในไฟล์ .env

# 6. รันแอพ
python run.py
```

เข้าถึงระบบ: http://localhost:5000

## License

MIT License
