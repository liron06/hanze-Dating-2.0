from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField, StringField
from wtforms.validators import InputRequired, Length, EqualTo, number_range

class LoginForm(FlaskForm):
    email = EmailField('Email')
    password = PasswordField('Wachtwoord')
    submit = SubmitField('Inloggen', render_kw={"class":"btn btn-primary"})

class RegistratieForm(FlaskForm):
    naam = StringField('Volledige naam', validators=[InputRequired(), Length(min=2, max=100)])
    email = EmailField('Email')
    password = PasswordField('Wachtwoord')
    confirm_password = PasswordField('Herhaal wachtwoord', validators=[EqualTo('password', message='Wachtwoorden moeten overeenkomen!')])
    leeftijd = IntegerField('Leeftijd', validators=[InputRequired(), number_range(min=18, max=100)])
    geslacht = SelectField(
        'Geslacht',
        choices=[ #je hebt maar 2 keuzes natuurlijk
            ('man', 'Man'),
            ('vrouw', 'Vrouw'),
            ('anders', 'Anders')
        ]
    )
    bio = TextAreaField('Bio', validators=[Length(min=10, max=251)])

    submit = SubmitField('Registreren', render_kw={"class":"btn btn-success"})



