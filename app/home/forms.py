from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from ..home import photos


class BayOwnerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    national_id = StringField('National ID', validators=[DataRequired()])
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(photos, 'Images only!')])
    submit = SubmitField('Save')
