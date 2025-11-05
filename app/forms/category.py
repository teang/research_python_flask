from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class CategoryForm(FlaskForm):
    """ฟอร์มสำหรับเพิ่ม/แก้ไขหมวดหมู่"""
    name = StringField('ชื่อหมวดหมู่ (ไทย)', validators=[DataRequired(), Length(max=100)])
    name_en = StringField('ชื่อหมวดหมู่ (English)', validators=[Optional(), Length(max=100)])
    description = TextAreaField('รายละเอียด', validators=[Optional()])
    icon = StringField('ไอคอน', validators=[Optional(), Length(max=50)],
                      description='ชื่อไอคอน FontAwesome เช่น fa-book')
    color = StringField('สี', validators=[Optional(), Length(max=20)],
                       description='รหัสสี เช่น #3B82F6')
    display_order = IntegerField('ลำดับการแสดง', validators=[Optional()], default=0)
    is_active = BooleanField('เปิดใช้งาน', default=True)
    submit = SubmitField('บันทึก')
