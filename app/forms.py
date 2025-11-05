from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """ฟอร์มสำหรับลงทะเบียนผู้ใช้"""
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('อีเมล', validators=[DataRequired(), Email()])
    full_name = StringField('ชื่อ-นามสกุล', validators=[DataRequired(), Length(max=150)])
    password = PasswordField('รหัสผ่าน', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('ยืนยันรหัสผ่าน',
                                    validators=[DataRequired(), EqualTo('password', message='รหัสผ่านไม่ตรงกัน')])
    submit = SubmitField('ลงทะเบียน')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาเลือกชื่ออื่น')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('อีเมลนี้ถูกใช้งานแล้ว')


class LoginForm(FlaskForm):
    """ฟอร์มสำหรับเข้าสู่ระบบ"""
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired()])
    password = PasswordField('รหัสผ่าน', validators=[DataRequired()])
    submit = SubmitField('เข้าสู่ระบบ')


class ResearchForm(FlaskForm):
    """ฟอร์มสำหรับเพิ่ม/แก้ไขงานวิจัย"""
    title = StringField('ชื่อหัวข้อวิจัย (ไทย)', validators=[DataRequired(), Length(max=300)])
    title_en = StringField('ชื่อหัวข้อวิจัย (English)', validators=[Optional(), Length(max=300)])
    authors = TextAreaField('ผู้วิจัย', validators=[DataRequired()],
                           description='ระบุชื่อผู้วิจัยทุกคน คั่นด้วยเครื่องหมายจุลภาค')
    abstract = TextAreaField('บทคัดย่อ', validators=[Optional()])
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
    url = StringField('URL', validators=[Optional(), Length(max=500)])
    file_path = StringField('ที่อยู่ไฟล์', validators=[Optional(), Length(max=500)])
    category_id = SelectField('หมวดหมู่', coerce=int, validators=[Optional()])
    submit = SubmitField('บันทึก')


class CategoryForm(FlaskForm):
    """ฟอร์มสำหรับเพิ่ม/แก้ไขหมวดหมู่"""
    name = StringField('ชื่อหมวดหมู่', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('รายละเอียด', validators=[Optional()])
    submit = SubmitField('บันทึก')
