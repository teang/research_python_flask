#!/usr/bin/env python3
"""
ระบบจัดเก็บงานวิจัย - Flask Application
สำหรับจัดการและค้นหางานวิจัยอย่างมีประสิทธิภาพ
"""
import os
from app import create_app

# สร้าง Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # รันเซิร์ฟเวอร์
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG']
    )
