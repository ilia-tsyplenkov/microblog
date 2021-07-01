from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_babel import Babel, lazy_gettext as _l, _

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(label=_l("Username"), validators=[DataRequired()])
    email = StringField(label=_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(label=_l("Password"), validators=[DataRequired()])
    password2 = PasswordField(label=_l("Confirm Password"), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_("Please use a different name."))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_("Please use a different email address."))


class LoginForm(FlaskForm):
    username = StringField(label=_l("Username"), validators=[DataRequired()])
    password = PasswordField(label=_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l('Sign In'))


class EditProfileForm(FlaskForm):
    username = StringField(label=_l("Username"), validators=[DataRequired()])
    about_me = TextAreaField(_l("About me"), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_username(self, username):
        if username.data != self.original_name:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different name.'))

class PostForm(FlaskForm):
    post = TextAreaField(label=_l('Say something'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(label=_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Reset Password Request'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label=_l("Password"), validators=[DataRequired()])
    password2 = PasswordField(label=_l("Confirm Password"), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
