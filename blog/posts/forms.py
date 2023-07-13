from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Post')

