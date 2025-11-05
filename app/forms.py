from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError, NumberRange
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
    # ข้อมูลพื้นฐาน
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
    pdf_file = FileField('อัพโหลดไฟล์ PDF', validators=[Optional(), FileAllowed(['pdf'], 'รองรับเฉพาะไฟล์ PDF เท่านั้น!')])
    tags = StringField('แท็ก', validators=[Optional(), Length(max=200)],
                      description='คั่นด้วยเครื่องหมายจุลภาค')
    category_id = SelectField('หมวดหมู่', coerce=int, validators=[Optional()])

    # Dublin Core Metadata Fields
    publisher = StringField('ผู้เผยแพร่', validators=[Optional(), Length(max=200)],
                           description='องค์กร/สำนักพิมพ์ที่เผยแพร่งานวิจัย')
    contributor = TextAreaField('ผู้มีส่วนร่วม', validators=[Optional()],
                               description='ที่ปรึกษา, บรรณาธิการ หรือผู้มีส่วนร่วมอื่นๆ คั่นด้วยเครื่องหมายจุลภาค')
    source = StringField('แหล่งที่มา', validators=[Optional(), Length(max=500)],
                        description='งานหรือทรัพยากรที่เป็นที่มาของงานนี้')
    language = SelectField('ภาษา',
                          choices=[
                              ('th', 'ไทย (th)'),
                              ('en', 'อังกฤษ (en)'),
                              ('th,en', 'ไทยและอังกฤษ (th,en)'),
                              ('other', 'อื่นๆ')
                          ],
                          default='th',
                          validators=[Optional()])
    relation = TextAreaField('ความสัมพันธ์', validators=[Optional()],
                            description='ความสัมพันธ์กับทรัพยากรอื่น เช่น "เป็นส่วนหนึ่งของโครงการ..."')
    coverage = StringField('ขอบเขต', validators=[Optional(), Length(max=200)],
                          description='ขอบเขตภูมิศาสตร์หรือช่วงเวลา เช่น "ประเทศไทย", "2020-2023"')
    rights = SelectField('สิทธิ์/ลิขสิทธิ์',
                        choices=[
                            ('', 'ไม่ระบุ'),
                            ('CC0', 'CC0 - สาธารณสมบัติ'),
                            ('CC-BY', 'CC BY - แสดงที่มา'),
                            ('CC-BY-SA', 'CC BY-SA - แสดงที่มา-อนุญาตแบบเดียวกัน'),
                            ('CC-BY-ND', 'CC BY-ND - แสดงที่มา-ห้ามดัดแปลง'),
                            ('CC-BY-NC', 'CC BY-NC - แสดงที่มา-ไม่ใช้เชิงพาณิชย์'),
                            ('CC-BY-NC-SA', 'CC BY-NC-SA - แสดงที่มา-ไม่ใช้เชิงพาณิชย์-อนุญาตแบบเดียวกัน'),
                            ('CC-BY-NC-ND', 'CC BY-NC-ND - แสดงที่มา-ไม่ใช้เชิงพาณิชย์-ห้ามดัดแปลง'),
                            ('All Rights Reserved', 'All Rights Reserved - ลิขสิทธิ์สงวนไว้'),
                            ('Custom', 'กำหนดเอง')
                        ],
                        validators=[Optional()])

    submit = SubmitField('บันทึก')


class CategoryForm(FlaskForm):
    """ฟอร์มสำหรับเพิ่ม/แก้ไขหมวดหมู่"""
    name = StringField('ชื่อหมวดหมู่', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('รายละเอียด', validators=[Optional()])
    submit = SubmitField('บันทึก')


class CommentForm(FlaskForm):
    """ฟอร์มสำหรับแสดงความคิดเห็น"""
    content = TextAreaField('ความคิดเห็น', validators=[DataRequired(), Length(min=3, max=1000)])
    rating = SelectField('คะแนน',
                        choices=[(0, 'ไม่ให้คะแนน'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                        coerce=int,
                        validators=[Optional()])
    submit = SubmitField('ส่งความคิดเห็น')


class ProfileForm(FlaskForm):
    """ฟอร์มสำหรับแก้ไขโปรไฟล์"""
    full_name = StringField('ชื่อ-นามสกุล', validators=[DataRequired(), Length(max=150)])
    email = StringField('อีเมล', validators=[DataRequired(), Email()])
    bio = TextAreaField('ประวัติส่วนตัว', validators=[Optional(), Length(max=500)])
    avatar = FileField('รูปโปรไฟล์', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'รองรับเฉพาะไฟล์รูปภาพ!')])
    email_notifications = BooleanField('รับการแจ้งเตือนทางอีเมล')
    submit = SubmitField('บันทึก')

    def __init__(self, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('อีเมลนี้ถูกใช้งานแล้ว')


class AdvancedSearchForm(FlaskForm):
    """ฟอร์มสำหรับค้นหาขั้นสูง"""
    search = StringField('คำค้นหา', validators=[Optional()])
    category_id = SelectField('หมวดหมู่', coerce=int, validators=[Optional()])
    publication_type = SelectField('ประเภทการตีพิมพ์',
                                  choices=[
                                      ('', 'ทั้งหมด'),
                                      ('journal', 'วารสารวิชาการ'),
                                      ('conference', 'การประชุมวิชาการ'),
                                      ('thesis', 'วิทยานิพนธ์'),
                                      ('report', 'รายงานวิจัย'),
                                      ('other', 'อื่นๆ')
                                  ],
                                  validators=[Optional()])
    year_from = IntegerField('ปีเริ่มต้น', validators=[Optional()])
    year_to = IntegerField('ปีสิ้นสุด', validators=[Optional()])
    tags = StringField('แท็ก', validators=[Optional()])
    sort_by = SelectField('เรียงลำดับตาม',
                         choices=[
                             ('created_at', 'วันที่สร้าง (ใหม่-เก่า)'),
                             ('created_at_asc', 'วันที่สร้าง (เก่า-ใหม่)'),
                             ('title', 'ชื่อ (ก-ฮ)'),
                             ('year', 'ปี (มาก-น้อย)'),
                             ('year_asc', 'ปี (น้อย-มาก)'),
                             ('view_count', 'ความนิยม')
                         ],
                         default='created_at')
    submit = SubmitField('ค้นหา')


class AdminUserForm(FlaskForm):
    """ฟอร์มสำหรับ Admin จัดการผู้ใช้"""
    username = StringField('ชื่อผู้ใช้', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('อีเมล', validators=[DataRequired(), Email()])
    full_name = StringField('ชื่อ-นามสกุล', validators=[Optional(), Length(max=150)])
    password = PasswordField('รหัสผ่าน', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('ยืนยันรหัสผ่าน',
                                    validators=[Optional(), EqualTo('password', message='รหัสผ่านไม่ตรงกัน')])
    bio = TextAreaField('ประวัติส่วนตัว', validators=[Optional()])
    is_admin = BooleanField('ผู้ดูแลระบบ')
    email_notifications = BooleanField('รับการแจ้งเตือนทางอีเมล')
    submit = SubmitField('บันทึก')


class PasswordChangeForm(FlaskForm):
    """ฟอร์มสำหรับเปลี่ยนรหัสผ่าน"""
    new_password = PasswordField('รหัสผ่านใหม่', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('ยืนยันรหัสผ่านใหม่',
                                        validators=[DataRequired(), EqualTo('new_password', message='รหัสผ่านไม่ตรงกัน')])
    submit = SubmitField('เปลี่ยนรหัสผ่าน')
