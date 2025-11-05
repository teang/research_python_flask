from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError
from app.models import User


class UserForm(FlaskForm):
    """ฟอร์มสำหรับเพิ่มผู้ใช้ (Admin)"""
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('อีเมล', validators=[DataRequired(), Email()])
    full_name = StringField('ชื่อ-นามสกุล', validators=[DataRequired(), Length(max=150)])
    phone = StringField('เบอร์โทรศัพท์', validators=[Optional(), Length(max=20)])
    department = StringField('หน่วยงาน', validators=[Optional(), Length(max=100)])
    position = StringField('ตำแหน่ง', validators=[Optional(), Length(max=100)])
    password = PasswordField('รหัสผ่าน', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('ยืนยันรหัสผ่าน',
                                    validators=[DataRequired(), EqualTo('password', message='รหัสผ่านไม่ตรงกัน')])
    roles = SelectMultipleField('บทบาท', coerce=int, validators=[Optional()])
    is_active = BooleanField('เปิดใช้งาน', default=True)
    submit = SubmitField('บันทึก')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ชื่อผู้ใช้นี้มีอยู่แล้ว')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('อีเมลนี้ถูกใช้งานแล้ว')


class UserEditForm(FlaskForm):
    """ฟอร์มสำหรับแก้ไขผู้ใช้ (Admin)"""
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('อีเมล', validators=[DataRequired(), Email()])
    full_name = StringField('ชื่อ-นามสกุล', validators=[DataRequired(), Length(max=150)])
    phone = StringField('เบอร์โทรศัพท์', validators=[Optional(), Length(max=20)])
    department = StringField('หน่วยงาน', validators=[Optional(), Length(max=100)])
    position = StringField('ตำแหน่ง', validators=[Optional(), Length(max=100)])
    password = PasswordField('รหัสผ่านใหม่', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('ยืนยันรหัสผ่าน',
                                    validators=[EqualTo('password', message='รหัสผ่านไม่ตรงกัน')])
    roles = SelectMultipleField('บทบาท', coerce=int, validators=[Optional()])
    is_active = BooleanField('เปิดใช้งาน')
    submit = SubmitField('บันทึก')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('ชื่อผู้ใช้นี้มีอยู่แล้ว')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('อีเมลนี้ถูกใช้งานแล้ว')
