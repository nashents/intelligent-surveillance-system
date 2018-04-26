from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from ..models import Patient


class BayOwnerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    national_id = StringField('National ID', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    upload_your_photo = FileField(FileRequired(u'File was empty!'))
    submit = SubmitField('Save')
