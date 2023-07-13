from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from blog.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                EqualTo('pass_confirm', message='Passwords must match')])
    pass_confirm = PasswordField('Confirm Password',
                               validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self, field):
        if User.email == field.data:
            raise ValidationError('Your email has already been registered')

    def check_name(self, field):
        if User.name == field.data:
            raise ValidationError('Username already taken')

class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def check_email(self, field):
        if User.email == field.data:
            raise ValidationError('Your email has already been registered')

    def check_name(self, field):
        if User.name == field.data:
            raise ValidationError('Username already taken')


