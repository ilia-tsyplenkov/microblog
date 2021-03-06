from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from flask_babel import lazy_gettext as _l, _

from app.models import User


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
    post = TextAreaField(label=_l('Say something'),
                         validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False

        super().__init__(*args, **kwargs)
