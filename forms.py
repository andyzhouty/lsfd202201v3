from flask_wtf import FlaskForm
from wtforms import (StringField, TimeField, PasswordField, SubmitField,
                     IntegerField, DateField)
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField


class UploadForm(FlaskForm):
    name = StringField("Your name(English, Chinese, Arabic Numbers):",
                       validators=[DataRequired()])
    password = PasswordField("Upload Password", validators=[DataRequired()])
    date = DateField("Date(yyyy-mm-dd)(2020-01-01)",
                     validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    pagedown = PageDownField("Content", validators=[DataRequired()])
    submit = SubmitField("Upload")


class AdminLoginForm(FlaskForm):
    admin_name = StringField("Your name: ", validators=[DataRequired()])
    password = PasswordField("ADMIN PASSWORD", validators=[DataRequired()])
    submit = SubmitField("Login")


class AdminDeleteForm(FlaskForm):
    id = IntegerField("Article id to delete", validators=[DataRequired()])
    submit = SubmitField("DELETE", validators=[DataRequired()])


class EditForm(FlaskForm):
    pagedown = PageDownField("Content", validators=[DataRequired()])
    submit = SubmitField("Publish", validators=[DataRequired()])
