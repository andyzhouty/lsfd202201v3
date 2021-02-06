from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_ckeditor import CKEditorField


class ArticleForm(FlaskForm):
    name = StringField(
        "Your name(English, Chinese, Arabic Numbers):", validators=[DataRequired()]
    )
    password = PasswordField(
        "You will need a password to create an article", validators=[DataRequired()]
    )
    date = DateField("Date(yyyy-mm-dd)(2020-01-01)", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AdminLoginForm(FlaskForm):
    name = StringField("Your name: ", validators=[DataRequired()])
    password = PasswordField("ADMIN PASSWORD", validators=[DataRequired()])
    submit = SubmitField("Login")


class EditForm(FlaskForm):
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Publish")


class FeedbackForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField(
        "Feedback", validators=[DataRequired(), Length(1, 200)]
    )  # noqa
    submit = SubmitField("Submit")


class LoginCreatorField(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class LoginUserField(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterCreatorField(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 20)])
    email = StringField("Email", validators=[DataRequired(), Length(1, 200), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_again = PasswordField(
        "Password(Again)", validators=[DataRequired(), EqualTo(password)]
    )
    submit = SubmitField("Register")


class RegisterUserField(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("Password", validators=[DataRequired()])
    password_again = PasswordField(
        "Password(Again)", validators=[DataRequired(), EqualTo(password)]
    )
    submit = SubmitField("Register")
