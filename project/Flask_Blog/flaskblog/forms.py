# Formu klases izveide
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

# Reģistrēšanās formas klase
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                            validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    # Funkcija kas parbauda vai Username jau eksiste
    def validate_username(self, username):

        # Query, kas parbauda vai User tabula ir jau Username ar tadu pasu nosaukumu
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already in use!')

    # Funkcija kas parbauda vai Email jau eksiste
    def validate_email(self, email):

        # Query, kas parbauda vai User tabula Email jau eksiste ar tadu pasu nosaukumu
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in use!')

# Pieslēgšanās formas klase
class LoginForm(FlaskForm):  
    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                            validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign In')

# Reģistrēšanās formas klase
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    submit = SubmitField('Update')

    # Funkcija kas parbauda vai Username jau eksiste
    def validate_username(self, username):
        if username.data != current_user.username:
            # Query, kas parbauda vai User tabula ir jau Username ar tadu pasu nosaukumu
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already in use!')


    # Funkcija kas parbauda vai Email jau eksiste
    def validate_email(self, email):

        if email.data != current_user.email:
            # Query, kas parbauda vai User tabula Email jau eksiste ar tadu pasu nosaukumu
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already in use!')