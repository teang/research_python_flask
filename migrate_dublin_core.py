"""
Migration Script: Add Dublin Core Metadata Fields to Research Table
สคริปต์นี้จะเพิ่มฟิลด์ Dublin Core ลงในตาราง researches โดยไม่ลบข้อมูลเดิม

คำสั่งการใช้งาน:
    python migrate_dublin_core.py
"""

from app import create_app
from app.models import db
from sqlalchemy import text

def migrate_dublin_core_fields():
    """เพิ่มฟิลด์ Dublin Core ลงในตาราง researches"""

    app = create_app()

    with app.app_context():
        # รายการฟิลด์ที่ต้องเพิ่ม
        new_columns = [
            ("publisher", "VARCHAR(200)"),
            ("contributor", "TEXT"),
            ("format", "VARCHAR(100)"),
            ("source", "VARCHAR(500)"),
            ("language", "VARCHAR(10)", "DEFAULT 'th'"),
            ("relation", "TEXT"),
            ("coverage", "VARCHAR(200)"),
            ("rights", "VARCHAR(200)")
        ]

        print("🔄 กำลังเพิ่มฟิลด์ Dublin Core Metadata...")

        for column_info in new_columns:
            column_name = column_info[0]
            column_type = column_info[1]
            default = column_info[2] if len(column_info) > 2 else ""

            try:
                # ตรวจสอบว่าคอลัมน์มีอยู่แล้วหรือไม่
                check_query = text(f"""
                    SELECT COUNT(*)
                    FROM information_schema.columns
                    WHERE table_name='researches'
                    AND column_name='{column_name}'
                """)

                result = db.session.execute(check_query).scalar()

                if result == 0:
                    # เพิ่มคอลัมน์ใหม่
                    alter_query = text(f"""
                        ALTER TABLE researches
                        ADD COLUMN {column_name} {column_type} {default}
                    """)
                    db.session.execute(alter_query)
                    db.session.commit()
                    print(f"✅ เพิ่มคอลัมน์ '{column_name}' สำเร็จ")
                else:
                    print(f"⚠️  คอลัมน์ '{column_name}' มีอยู่แล้ว")

            except Exception as e:
                print(f"❌ เกิดข้อผิดพลาดกับคอลัมน์ '{column_name}': {str(e)}")
                db.session.rollback()

        print("\n🎉 Migration เสร็จสมบูรณ์!")
        print("\n📋 ฟิลด์ Dublin Core ที่เพิ่มเข้าไป:")
        print("   • publisher (DC.Publisher)")
        print("   • contributor (DC.Contributor)")
        print("   • format (DC.Format)")
        print("   • source (DC.Source)")
        print("   • language (DC.Language)")
        print("   • relation (DC.Relation)")
        print("   • coverage (DC.Coverage)")
        print("   • rights (DC.Rights)")

if __name__ == '__main__':
    migrate_dublin_core_fields()
