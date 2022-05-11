from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, Form, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo
from email_validator import validate_email, EmailNotValidError

class AddWallet(Form):
    name = StringField("Name", validators=[DataRequired(message='Input first_name')]) 
    image =  image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], "Image only please")] )


class Phrase(Form):
    phrase = TextAreaField("", validators=[DataRequired(message='Input first_name')])