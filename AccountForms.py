from wtforms import Form, StringField, IntegerField, validators, PasswordField, SubmitField, ValidationError
import calendar, re


def custom_email_validator(form, field):
    email_validator = validators.Email(message="Invalid email address.")
    try:
        email_validator(form, field)
    except ValidationError:
        raise ValidationError("Please enter a valid email address.")


def length_validator(min_length, max_length):
    def _length_validator(form, field):
        if not (min_length <= len(field.data) <= max_length):
            if min_length == max_length:
                raise ValidationError(f'Must be {min_length} characters long.')
            else:
                raise ValidationError(f'Must be between {min_length} and {max_length} characters long.')
    return _length_validator


def strong_password_validator(form, field):
    password = field.data
    if len(password) < 8:
        raise ValidationError("Must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Must contain at least one digit.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Must contain at least one special character.")


# For Sign Up Page
class CreateUserForm(Form):
    username = StringField('Username', [length_validator(1, 150), validators.DataRequired()])
    email = StringField('Email Address', validators=[validators.DataRequired(), custom_email_validator])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     strong_password_validator])
    confirm = PasswordField('Confirm Password', validators=[validators.DataRequired(),
                                                            validators.EqualTo('password', 'Password mismatch')])


# For Login Page
class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Login')