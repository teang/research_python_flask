"""Utility functions for the research management system"""
import os
import io
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
from flask import send_file, current_app


def allowed_file(filename, allowed_extensions={'pdf'}):
    """ตรวจสอบว่าไฟล์ที่อัพโหลดเป็นประเภทที่อนุญาตหรือไม่"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, upload_folder='uploads/researches'):
    """บันทึกไฟล์ที่อัพโหลด"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # เพิ่ม timestamp เพื่อป้องกันชื่อซ้ำ
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"

        filepath = os.path.join(upload_folder, filename)
        os.makedirs(upload_folder, exist_ok=True)
        file.save(filepath)
        return filepath, file.content_length
    return None, 0


def format_citation(research, style='apa'):
    """จัดรูปแบบการอ้างอิง

    Args:
        research: Research object
        style: รูปแบบการอ้างอิง ('apa', 'mla', 'chicago', 'bibtex', 'ris')

    Returns:
        str: การอ้างอิงที่จัดรูปแบบแล้ว
    """
    authors = research.authors if research.authors else "ผู้แต่งไม่ระบุ"
    title = research.title
    year = research.year if research.year else "ไม่ระบุปี"

    if style == 'apa':
        # APA Style: Authors. (Year). Title. Journal, Volume(Issue), Pages. DOI
        citation = f"{authors} ({year}). {title}."
        if research.journal_name:
            citation += f" {research.journal_name}"
            if research.volume:
                citation += f", {research.volume}"
                if research.issue:
                    citation += f"({research.issue})"
            if research.pages:
                citation += f", {research.pages}"
            citation += "."
        if research.doi:
            citation += f" https://doi.org/{research.doi}"
        return citation

    elif style == 'mla':
        # MLA Style: Authors. "Title." Journal Volume.Issue (Year): Pages. Medium.
        citation = f'{authors}. "{title}."'
        if research.journal_name:
            citation += f" {research.journal_name}"
            if research.volume:
                citation += f" {research.volume}"
                if research.issue:
                    citation += f".{research.issue}"
            citation += f" ({year})"
            if research.pages:
                citation += f": {research.pages}"
            citation += "."
        else:
            citation += f" {year}."
        return citation

    elif style == 'chicago':
        # Chicago Style: Authors. "Title." Journal Volume, no. Issue (Year): Pages.
        citation = f'{authors}. "{title}."'
        if research.journal_name:
            citation += f" {research.journal_name}"
            if research.volume:
                citation += f" {research.volume}"
                if research.issue:
                    citation += f", no. {research.issue}"
            citation += f" ({year})"
            if research.pages:
                citation += f": {research.pages}"
            citation += "."
        else:
            citation += f" {year}."
        return citation

    elif style == 'bibtex':
        # BibTeX format
        authors_list = authors.split(',')
        bibtex_authors = ' and '.join([a.strip() for a in authors_list])

        entry_type = 'article' if research.publication_type == 'journal' else 'inproceedings'
        if research.publication_type == 'thesis':
            entry_type = 'phdthesis'

        citation = f"@{entry_type}{{research{research.id},\n"
        citation += f"  author = {{{bibtex_authors}}},\n"
        citation += f"  title = {{{title}}},\n"
        citation += f"  year = {{{year}}},\n"

        if research.journal_name:
            citation += f"  journal = {{{research.journal_name}}},\n"
        if research.volume:
            citation += f"  volume = {{{research.volume}}},\n"
        if research.issue:
            citation += f"  number = {{{research.issue}}},\n"
        if research.pages:
            citation += f"  pages = {{{research.pages}}},\n"
        if research.doi:
            citation += f"  doi = {{{research.doi}}},\n"
        if research.url:
            citation += f"  url = {{{research.url}}},\n"

        citation += "}"
        return citation

    elif style == 'ris':
        # RIS format
        type_map = {
            'journal': 'JOUR',
            'conference': 'CONF',
            'thesis': 'THES',
            'report': 'RPRT',
            'other': 'GEN'
        }
        ris_type = type_map.get(research.publication_type, 'GEN')

        citation = f"TY  - {ris_type}\n"

        # Authors
        for author in authors.split(','):
            citation += f"AU  - {author.strip()}\n"

        citation += f"TI  - {title}\n"
        citation += f"PY  - {year}\n"

        if research.journal_name:
            citation += f"JO  - {research.journal_name}\n"
        if research.volume:
            citation += f"VL  - {research.volume}\n"
        if research.issue:
            citation += f"IS  - {research.issue}\n"
        if research.pages:
            citation += f"SP  - {research.pages}\n"
        if research.doi:
            citation += f"DO  - {research.doi}\n"
        if research.url:
            citation += f"UR  - {research.url}\n"
        if research.abstract:
            citation += f"AB  - {research.abstract}\n"
        if research.keywords:
            for keyword in research.keywords.split(','):
                citation += f"KW  - {keyword.strip()}\n"

        citation += "ER  -"
        return citation

    else:
        return f"{authors} ({year}). {title}."


def export_researches_csv(researches):
    """ส่งออกงานวิจัยเป็นไฟล์ CSV"""
    data = []
    for r in researches:
        data.append({
            'ID': r.id,
            'ชื่อ': r.title,
            'ชื่อ (EN)': r.title_en,
            'ผู้วิจัย': r.authors,
            'ปี': r.year,
            'ประเภท': r.publication_type,
            'วารสาร/การประชุม': r.journal_name,
            'เล่มที่': r.volume,
            'ฉบับที่': r.issue,
            'หน้า': r.pages,
            'DOI': r.doi,
            'URL': r.url,
            'คำสำคัญ': r.keywords,
            'หมวดหมู่': r.category.name if r.category else '',
            'ผู้อัพโหลด': r.uploader.full_name if r.uploader else '',
            'วันที่สร้าง': r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
        })

    df = pd.DataFrame(data)

    # สร้าง CSV ในหน่วยความจำ
    output = io.BytesIO()
    df.to_csv(output, index=False, encoding='utf-8-sig')  # utf-8-sig สำหรับ Excel
    output.seek(0)

    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'researches_{datetime.now().strftime("%Y%m%d")}.csv'
    )


def export_researches_excel(researches):
    """ส่งออกงานวิจัยเป็นไฟล์ Excel"""
    data = []
    for r in researches:
        data.append({
            'ID': r.id,
            'ชื่อ': r.title,
            'ชื่อ (EN)': r.title_en,
            'ผู้วิจัย': r.authors,
            'ปี': r.year,
            'ประเภท': r.publication_type,
            'วารสาร/การประชุม': r.journal_name,
            'เล่มที่': r.volume,
            'ฉบับที่': r.issue,
            'หน้า': r.pages,
            'DOI': r.doi,
            'URL': r.url,
            'คำสำคัญ': r.keywords,
            'หมวดหมู่': r.category.name if r.category else '',
            'ผู้อัพโหลด': r.uploader.full_name if r.uploader else '',
            'วันที่สร้าง': r.created_at.strftime('%Y-%m-%d %H:%M:%S') if r.created_at else ''
        })

    df = pd.DataFrame(data)

    # สร้าง Excel ในหน่วยความจำ
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Researches', index=False)
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'researches_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )


def export_researches_bibtex(researches):
    """ส่งออกงานวิจัยเป็นไฟล์ BibTeX"""
    bibtex_entries = []
    for r in researches:
        bibtex_entries.append(format_citation(r, style='bibtex'))

    bibtex_content = '\n\n'.join(bibtex_entries)

    output = io.BytesIO(bibtex_content.encode('utf-8'))
    output.seek(0)

    return send_file(
        output,
        mimetype='application/x-bibtex',
        as_attachment=True,
        download_name=f'researches_{datetime.now().strftime("%Y%m%d")}.bib'
    )


def export_researches_ris(researches):
    """ส่งออกงานวิจัยเป็นไฟล์ RIS"""
    ris_entries = []
    for r in researches:
        ris_entries.append(format_citation(r, style='ris'))

    ris_content = '\n\n'.join(ris_entries)

    output = io.BytesIO(ris_content.encode('utf-8'))
    output.seek(0)

    return send_file(
        output,
        mimetype='application/x-research-info-systems',
        as_attachment=True,
        download_name=f'researches_{datetime.now().strftime("%Y%m%d")}.ris'
    )


def send_email_notification(to_email, subject, body):
    """ส่งการแจ้งเตือนทางอีเมล

    Note: ต้องตั้งค่า Flask-Mail configuration ก่อนใช้งาน
    """
    try:
        from flask_mail import Mail, Message
        mail = Mail(current_app)

        msg = Message(
            subject=subject,
            recipients=[to_email],
            body=body
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
