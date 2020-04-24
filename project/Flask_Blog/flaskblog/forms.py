# Formu klases izveide
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    # Klase, kura nosaka kādi parametri būs jaievada Reģistrēšanās formā

    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                            validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        # Funkcija kas parbaudīs vai lietotajvārds datubāzē jau eksistē

        user = User.query.filter_by(username=username.data).first()
        # Query, kas meklēs ievadīto lietotājvardu datubāzē.
        if user:
            raise ValidationError('This username is already in use!')

    def validate_email(self, email):
        # Funkcija kas parbaudīs vai e-pasts datubāzē jau eksistē

        user = User.query.filter_by(email=email.data).first()
        # Query, kas meklēs ievadīto e-pastu datubāzē.
        if user:
            raise ValidationError('This email is already in use!')

class LoginForm(FlaskForm): 
    # Klase, kura nosaka kādi parametri būs jaievada Pieslēgšanās formā

    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    password = PasswordField('Password',
                            validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
    # Klase, kura nosaka kādi parametri būs jaievada Porfilu Atjaunošanas formā

    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture',
                         validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        # Funkcija, kas pārbauda vai ievadītais lietotājvārds ir derīgs.

        if username.data != current_user.username:
            # Pārbaude, vai ievadītais lietotājvards nav vienāds ar pašreizējo lietotājvārdu
            user = User.query.filter_by(username=username.data).first()
            # Query, kas meklēs ievadīto lietotājvardu datubāzē.
            if user:
                raise ValidationError('This username is already in use!')


    def validate_email(self, email):
        # Funkcija, kas pārbauda vai ievadītais e-pasts ir derīgs.

        if email.data != current_user.email:
            # Pārbaude, vai ievadītais e-pasts nav vienāds ar pašreizējo e-pastu
            user = User.query.filter_by(email=email.data).first()
            # Query, kas meklēs ievadīto e-pastu datubāzē.
            if user:
                raise ValidationError('This email is already in use!')

class PostForm(FlaskForm):
    # Klase, kura nosaka kādi parametri būs jaievada Rakstu Publicēšanas formā

    title = StringField('Title', validators=[DataRequired()])

    content = TextAreaField('Content', validators=[DataRequired()])

    submit = SubmitField('Post')
