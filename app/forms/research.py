from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class ResearchForm(FlaskForm):
    """ฟอร์มสำหรับเพิ่ม/แก้ไขงานวิจัย"""
    title = StringField('ชื่อหัวข้อวิจัย (ไทย)', validators=[DataRequired(), Length(max=300)])
    title_en = StringField('ชื่อหัวข้อวิจัย (English)', validators=[Optional(), Length(max=300)])
    authors = TextAreaField('ผู้วิจัย', validators=[DataRequired()],
                           description='ระบุชื่อผู้วิจัยทุกคน คั่นด้วยเครื่องหมายจุลภาค')
    abstract = TextAreaField('บทคัดย่อ (ไทย)', validators=[Optional()])
    abstract_en = TextAreaField('บทคัดย่อ (English)', validators=[Optional()])
    keywords = StringField('คำสำคัญ', validators=[Optional(), Length(max=500)],
                          description='คั่นด้วยเครื่องหมายจุลภาค')
    year = IntegerField('ปีที่เผยแพร่', validators=[Optional()])
    publication_type = SelectField('ประเภทการตีพิมพ์',
                                  choices=[
                                      ('', 'เลือกประเภท'),
                                      ('journal', 'วารสารวิชาการ'),
                                      ('conference', 'การประชุมวิชาการ'),
                                      ('thesis', 'วิทยานิพนธ์'),
                                      ('report', 'รายงานวิจัย'),
                                      ('other', 'อื่นๆ')
                                  ])
    journal_name = StringField('ชื่อวารสาร/การประชุม', validators=[Optional(), Length(max=200)])
    volume = StringField('เล่มที่', validators=[Optional(), Length(max=50)])
    issue = StringField('ฉบับที่', validators=[Optional(), Length(max=50)])
    pages = StringField('หน้า', validators=[Optional(), Length(max=50)],
                       description='เช่น 1-10')
    doi = StringField('DOI', validators=[Optional(), Length(max=200)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=50)])
    url = StringField('URL', validators=[Optional(), Length(max=500)])
    file_path = StringField('ที่อยู่ไฟล์', validators=[Optional(), Length(max=500)])
    category_id = SelectField('หมวดหมู่', coerce=int, validators=[Optional()])
    status = SelectField('สถานะ',
                        choices=[
                            ('draft', 'แบบร่าง'),
                            ('published', 'เผยแพร่แล้ว'),
                            ('archived', 'เก็บถาวร')
                        ],
                        default='draft')
    submit = SubmitField('บันทึก')
