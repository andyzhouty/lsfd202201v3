from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class UploadForm(FlaskForm):
    name = StringField("Your name(English, Chinese, Arabic Numbers):",
                       validators=[DataRequired()])
    password = PasswordField("Upload Password", validators=[DataRequired()])
    date = DateField("Date(yyyy-mm-dd)(2020-01-01)",
                     validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Upload")


class AdminLoginForm(FlaskForm):
    admin_name = StringField("Your name: ", validators=[DataRequired()])
    password = PasswordField("ADMIN PASSWORD", validators=[DataRequired()])
    submit = SubmitField("Login")


class EditForm(FlaskForm):
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Publish", validators=[DataRequired()])
