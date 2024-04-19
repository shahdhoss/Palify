from wtforms import Form, StringField, PasswordField, validators
from flask import session

def validate_email1(form, field):
    if '@' not in field.data:
        raise validators.ValidationError('Email address must contain @ symbol.')
def validate_email2(form, field):
    if '@' not in field.data:
        raise validators.ValidationError('Email address must contain @ symbol.')
class RegistrationForm(Form):
    firstName = StringField('Enter your first name', [validators.InputRequired(message='Please enter your first name')])
    lastName = StringField('Enter your last name', [validators.InputRequired(message='Please enter your last name')])
    email = StringField('Enter your Email Address', [validators.InputRequired(message='Please enter an email'),validators.Length(min=6, max=35), validate_email1])
    password1 = PasswordField('New Password', [
        validators.DataRequired()
    ])
    password2 = PasswordField('Repeat Password',[validators.EqualTo('password1', message='Passwords must match')])

class loginform(Form):
    email = StringField('Enter your Email Address', [validators.InputRequired(message='Please enter an email'),validators.Length(min=6, max=35), validate_email2])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])