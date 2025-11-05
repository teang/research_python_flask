from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """ฟอร์มสำหรับลงทะเบียนผู้ใช้"""
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('อีเมล', validators=[DataRequired(), Email()])
    full_name = StringField('ชื่อ-นามสกุล', validators=[DataRequired(), Length(max=150)])
    phone = StringField('เบอร์โทรศัพท์', validators=[Length(max=20)])
    department = StringField('หน่วยงาน', validators=[Length(max=100)])
    position = StringField('ตำแหน่ง', validators=[Length(max=100)])
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
