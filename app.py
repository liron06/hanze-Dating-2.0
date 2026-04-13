from flask import Flask, render_template, session, redirect, flash
from forms import LoginForm, RegistratieForm
from models import db, migrate, users, profiles
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/over_ons")
def over_ons():
    return render_template("over_ons.html")

@app.route("/profielen")
def profielen():

    alle_profielen = profiles.query.all()

    return render_template("profielen.html", profielen=alle_profielen)    

@app.route("/registreren", methods=["GET", "POST"])
def registreren():
    form = RegistratieForm()

    if form.validate_on_submit():
        bestaande_gebruiker = users.query.filter_by(gebruikersnaam=form.email.data).first()
        
        if bestaande_gebruiker:
            flash('Deze gebruiker bestaat al! Probeer in te loggen', 'warning')
            return redirect("/registreren")

        gehasht_wachtwoord = generate_password_hash(form.password.data)

        nieuwe_gebruiker = users(gebruikersnaam=form.email.data, wachtwoord=gehasht_wachtwoord)

        db.session.add(nieuwe_gebruiker)
        db.session.commit()

        nieuwe_profiel = profiles(
            gebruiker_id=nieuwe_gebruiker.id,
            naam=form.naam.data,
            leeftijd=form.leeftijd.data,
            geslacht=form.geslacht.data,
            bio=form.bio.data
        )

        db.session.add(nieuwe_profiel)
        db.session.commit()

        return redirect("/inloggen")

    return render_template("registreren.html", form=form)




@app.route("/inloggen", methods=["GET", "POST"])
def inloggen():
    form = LoginForm()

    if form.validate_on_submit():
        gebruiker = users.query.filter_by(gebruikersnaam=form.email.data).first()

        if gebruiker and check_password_hash(gebruiker.wachtwoord, form.password.data):
            
            session["user_id"] = gebruiker.id
            #session["user"] = gebruiker.gebruikersnaam
            
            return redirect("/")
        else:
            flash('Verkeerd e-mailadres of wachtwoord', 'danger')

    return render_template("inloggen.html", form=form)


@app.route("/logout")
def uitloggen():
    session.pop("user", None)
    return redirect("/")