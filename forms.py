from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    email = EmailField('email')
    password = PasswordField('Wachtwoord')
    submit = SubmitField('Inloggen', render_kw={"class":"btn btn-primary"})