from flask_wtf import FlaskForm
from flask_wtf.csrf import validate_csrf
from flask_wtf.recaptcha import validators
from wtforms import (StringField, TextAreaField, TimeField, 
                     PasswordField, SubmitField)
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    name = StringField("Your name(English, Chinese, Arabic Numbers):",
                       validators=[DataRequired()])
    password = PasswordField("Upload Password", validators=[DataRequired()])
    time = TimeField("Date(yyyy-mm-dd)(2020-01-01)",
                     validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Upload")
