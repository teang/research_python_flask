# Dublin Core Metadata Standard Implementation Guide

## 📋 ภาพรวม

ระบบ Research Python Flask ได้รองรับมาตรฐาน **Dublin Core Metadata** อย่างเต็มรูปแบบตามข้อกำหนดของ Dublin Core Metadata Initiative (DCMI)

Dublin Core เป็นชุดคำศัพท์พื้นฐาน (Metadata) ที่ออกแบบมาให้เรียบง่ายและเป็นสากล เพื่อใช้อธิบายทรัพยากรดิจิทัล ทำให้ระบบต่างๆ สามารถแลกเปลี่ยนและค้นหาข้อมูลข้ามกันได้ (Interoperability)

## 🔗 เอกสารอ้างอิง

- **Dublin Core Metadata Initiative:** https://www.dublincore.org/
- **Dublin Core Elements (15 รายการ):** https://www.dublincore.org/specifications/dublin-core/dces/

---

## 📊 Dublin Core Elements ทั้ง 15 รายการ

| # | Element | ฟิลด์ในระบบ | คำอธิบาย |
|---|---------|------------|---------|
| 1 | **DC.Title** | `title`, `title_en` | ชื่อของงานวิจัย |
| 2 | **DC.Creator** | `authors` | ผู้สร้างสรรค์/ผู้แต่ง |
| 3 | **DC.Subject** | `keywords`, `tags` | หัวเรื่อง/คำสำคัญ |
| 4 | **DC.Description** | `abstract` | คำอธิบาย/บทคัดย่อ |
| 5 | **DC.Publisher** | `publisher` | ผู้เผยแพร่ (องค์กร/สำนักพิมพ์) |
| 6 | **DC.Contributor** | `contributor` | ผู้มีส่วนร่วม (ที่ปรึกษา, บรรณาธิการ) |
| 7 | **DC.Date** | `year`, `created_at` | วันที่เผยแพร่ |
| 8 | **DC.Type** | `publication_type` | ประเภทของทรัพยากร (Text, Dataset, etc.) |
| 9 | **DC.Format** | `format` | รูปแบบไฟล์ (MIME type เช่น application/pdf) |
| 10 | **DC.Identifier** | `doi`, `url`, `id` | ตัวระบุเอกลักษณ์ (DOI, URL, Local ID) |
| 11 | **DC.Source** | `source` | แหล่งที่มาของงาน |
| 12 | **DC.Language** | `language` | ภาษา (ISO 639-1 เช่น th, en) |
| 13 | **DC.Relation** | `relation` | ความสัมพันธ์กับทรัพยากรอื่น |
| 14 | **DC.Coverage** | `coverage` | ขอบเขตภูมิศาสตร์หรือช่วงเวลา |
| 15 | **DC.Rights** | `rights` | สิทธิ์/ลิขสิทธิ์ (CC-BY, All Rights Reserved, etc.) |

---

## 🚀 วิธีการใช้งาน

### 1. การเพิ่มงานวิจัยพร้อม Dublin Core Metadata

เมื่อเพิ่มหรือแก้ไขงานวิจัย คุณจะพบฟิลด์ Dublin Core ในฟอร์ม:

#### ฟิลด์พื้นฐาน (มีอยู่แล้ว)
- **ชื่อหัวข้อวิจัย** → DC.Title
- **ผู้วิจัย** → DC.Creator
- **บทคัดย่อ** → DC.Description
- **คำสำคัญ** → DC.Subject
- **ปีที่เผยแพร่** → DC.Date

#### ฟิลด์ Dublin Core เพิ่มเติม (ใหม่)
- **ผู้เผยแพร่** → DC.Publisher
- **ผู้มีส่วนร่วม** → DC.Contributor
- **ภาษา** → DC.Language (เลือกจาก dropdown: th, en, th,en)
- **สิทธิ์/ลิขสิทธิ์** → DC.Rights (เลือกจาก Creative Commons หรือ All Rights Reserved)
- **แหล่งที่มา** → DC.Source
- **ความสัมพันธ์** → DC.Relation
- **ขอบเขต** → DC.Coverage

### 2. การดู Dublin Core Metadata

เมื่อเปิดดูรายละเอียดงานวิจัย หากมีข้อมูล Dublin Core จะแสดงในส่วน **"Dublin Core Metadata"** พร้อมไอคอนและข้อมูลแบ่งหมวดหมู่

### 3. การ Export Dublin Core Metadata

ระบบรองรับการ export metadata ในรูปแบบมาตรฐาน:

#### Export งานวิจัยเดี่ยว
ที่หน้ารายละเอียดงานวิจัย มีปุ่ม:
- **Export DC XML** - ส่งออกเป็น Dublin Core XML
- **Export DC JSON** - ส่งออกเป็น Dublin Core JSON

#### Export งานวิจัยทั้งหมด
เข้าที่ URL:
```
/research/export/dublin-core-xml    - ส่งออกทั้งหมดเป็น XML Collection
/research/export/dublin-core-json   - ส่งออกทั้งหมดเป็น JSON Collection
```

---

## 🔧 การติดตั้งและ Migration

### 1. Migration Database

สำหรับระบบที่มีข้อมูลอยู่แล้ว ให้รัน migration script:

```bash
python migrate_dublin_core.py
```

Script นี้จะเพิ่มฟิลด์ Dublin Core ใหม่ลงในตาราง `researches` โดยไม่ลบข้อมูลเดิม:
- `publisher` (VARCHAR 200)
- `contributor` (TEXT)
- `format` (VARCHAR 100)
- `source` (VARCHAR 500)
- `language` (VARCHAR 10, default 'th')
- `relation` (TEXT)
- `coverage` (VARCHAR 200)
- `rights` (VARCHAR 200)

### 2. สร้างฐานข้อมูลใหม่

สำหรับระบบใหม่ เพียงรัน:

```bash
python run.py
```

ระบบจะสร้างตารางพร้อมฟิลด์ Dublin Core ทั้งหมดโดยอัตโนมัติ

---

## 📡 API Endpoints

### Export Dublin Core Metadata

#### 1. Export งานวิจัยเดี่ยวเป็น XML
```
GET /research/<id>/export/dublin-core/xml
```

**ตัวอย่าง Response:**
```xml
<?xml version='1.0' encoding='utf-8'?>
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">
  <dc:title>ชื่องานวิจัย</dc:title>
  <dc:creator>ชื่อผู้วิจัย</dc:creator>
  <dc:subject>คำสำคัญ1</dc:subject>
  <dc:subject>คำสำคัญ2</dc:subject>
  <dc:description>บทคัดย่อ...</dc:description>
  <dc:publisher>มหาวิทยาลัย</dc:publisher>
  <dc:date>2024</dc:date>
  <dc:type>Text</dc:type>
  <dc:format>application/pdf</dc:format>
  <dc:identifier>doi:10.xxxx/xxxxx</dc:identifier>
  <dc:language>th</dc:language>
  <dc:rights>CC-BY</dc:rights>
</metadata>
```

#### 2. Export งานวิจัยเดี่ยวเป็น JSON
```
GET /research/<id>/export/dublin-core/json
```

**ตัวอย่าง Response:**
```json
{
  "title": "ชื่องานวิจัย",
  "creator": "ชื่อผู้วิจัย",
  "subject": ["คำสำคัญ1", "คำสำคัญ2"],
  "description": "บทคัดย่อ...",
  "publisher": "มหาวิทยาลัย",
  "contributor": "ที่ปรึกษา",
  "date": "2024",
  "type": "Text",
  "format": "application/pdf",
  "identifier": ["doi:10.xxxx/xxxxx", "local_id:123"],
  "source": "",
  "language": "th",
  "relation": "",
  "coverage": "ประเทศไทย",
  "rights": "CC-BY"
}
```

#### 3. Export ทั้งหมดเป็น XML Collection
```
GET /research/export/dublin-core-xml
```

#### 4. Export ทั้งหมดเป็น JSON Collection
```
GET /research/export/dublin-core-json
```

---

## 🎯 Best Practices

### 1. การกรอกข้อมูล Publisher
ระบุชื่อองค์กรหรือสำนักพิมพ์ที่เผยแพร่งานวิจัย เช่น:
- มหาวิทยาลัยเกษตรศาสตร์
- สำนักงานกองทุนสนับสนุนการวิจัย (สกว.)
- Springer Nature

### 2. การกรอกข้อมูล Contributor
ระบุผู้ที่มีส่วนร่วมนอกเหนือจากผู้วิจัยหลัก เช่น:
- ที่ปรึกษาหลัก, ที่ปรึกษาร่วม
- บรรณาธิการ
- ผู้ตรวจสอบ
- ผู้สนับสนุนทุน

คั่นด้วยเครื่องหมายจุลภาค (,)

### 3. การเลือกภาษา (Language)
- `th` - งานวิจัยเป็นภาษาไทยเท่านั้น
- `en` - งานวิจัยเป็นภาษาอังกฤษเท่านั้น
- `th,en` - งานวิจัยมีทั้งภาษาไทยและอังกฤษ

### 4. การกำหนดสิทธิ์ (Rights)
เลือกให้เหมาะสมกับนโยบายการเผยแพร่:
- **CC0** - สาธารณสมบัติ (ไม่มีลิขสิทธิ์)
- **CC-BY** - อนุญาตให้ใช้ได้โดยต้องแสดงที่มา
- **CC-BY-SA** - แสดงที่มา + อนุญาตแบบเดียวกัน
- **CC-BY-NC** - แสดงที่มา + ไม่ใช้เชิงพาณิชย์
- **All Rights Reserved** - ลิขสิทธิ์สงวนไว้ทั้งหมด

### 5. การกรอกขอบเขต (Coverage)
ระบุขอบเขตภูมิศาสตร์หรือช่วงเวลา เช่น:
- "ประเทศไทย"
- "ภาคตะวันออกเฉียงเหนือ"
- "จังหวัดนครราชสีมา"
- "2020-2023"

---

## 🧪 การทดสอบ

### ทดสอบ Export XML
```bash
curl http://localhost:5000/research/1/export/dublin-core/xml
```

### ทดสอบ Export JSON
```bash
curl http://localhost:5000/research/1/export/dublin-core/json
```

---

## 📚 ตัวอย่างการใช้งาน

### 1. งานวิจัยวารสารวิชาการ
```
Title: การพัฒนาระบบจัดการงานวิจัยด้วย Flask
Creator: สมชาย ใจดี, สมหญิง รักงาน
Publisher: วารสารวิทยาศาสตร์ มหาวิทยาลัยเกษตรศาสตร์
Contributor: รศ.ดร. วิจัย สุดยอด (ที่ปรึกษา)
Language: th,en
Rights: CC-BY-NC-SA
Coverage: ประเทศไทย
```

### 2. วิทยานิพนธ์
```
Title: A Study on Machine Learning for Agricultural Research
Creator: John Doe
Publisher: Kasetsart University
Contributor: Prof. Dr. Advisor Name (Advisor)
Type: thesis
Language: en
Rights: All Rights Reserved
Coverage: Thailand, 2020-2024
```

---

## 🔍 การตรวจสอบ Metadata ที่ถูกต้อง

เมื่อ export ออกมาแล้ว ควรตรวจสอบว่า:

1. ✅ ทุกฟิลด์มี namespace ที่ถูกต้อง (`dc:` หรือ `dcterms:`)
2. ✅ ภาษาใช้รหัส ISO 639-1 (เช่น th, en)
3. ✅ Format เป็น MIME type ที่ถูกต้อง (เช่น application/pdf)
4. ✅ Identifier เป็น URI หรือ DOI ที่สมบูรณ์
5. ✅ Rights ระบุอย่างชัดเจน

---

## 🛠️ การพัฒนาเพิ่มเติม

### เพิ่มฟิลด์ Custom
หากต้องการเพิ่มฟิลด์เฉพาะองค์กร แนะนำให้ใช้ namespace เฉพาะ เช่น:
```xml
<metadata xmlns:custom="http://yourorg.com/metadata/">
  <dc:title>...</dc:title>
  <custom:internal_id>12345</custom:internal_id>
</metadata>
```

### การเชื่อมต่อกับระบบอื่น
Dublin Core XML/JSON ที่ export ออกมาสามารถนำไปใช้กับ:
- OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting)
- DSpace, Fedora Repository
- CKAN Data Portal
- ระบบคลังปัญญาระดับชาติ

---

## 📞 การสนับสนุน

หากพบปัญหาหรือต้องการคำแนะนำ:
1. ตรวจสอบ logs ที่ console
2. ตรวจสอบว่า migration ทำงานสำเร็จ
3. ตรวจสอบว่าข้อมูลในฐานข้อมูลถูกต้อง

---

## 📖 เอกสารอ้างอิงเพิ่มเติม

- [Dublin Core Metadata Element Set](https://www.dublincore.org/specifications/dublin-core/dces/)
- [Dublin Core Usage Guide](https://www.dublincore.org/specifications/dublin-core/usageguide/)
- [Creative Commons Licenses](https://creativecommons.org/licenses/)
- [ISO 639-1 Language Codes](https://www.loc.gov/standards/iso639-2/php/code_list.php)

---

**เวอร์ชัน:** 1.0.0
**วันที่อัพเดท:** 2025-11-05
**ผู้พัฒนา:** Research Python Flask Team
