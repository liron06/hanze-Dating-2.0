from flask import Flask, render_template, session, redirect, flash
from forms import LoginForm, RegistratieForm
from models import db, migrate, users, profiles
from werkzeug.security import generate_password_hash, check_password_hash
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SECRET_KEY"] = "Ditissupergeheim"
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
    return render_template("profielen.html")    

@app.route("/registreren", methods=["GET", "POST"])
def registreren():
    form = RegistratieForm()

    if form.validate_on_submit():
        # 1. Kijk of de gebruiker (email) al bestaat in de database
        bestaande_gebruiker = users.query.filter_by(gebruikersnaam=form.email.data).first()
        
        if bestaande_gebruiker:
            flash('Deze gebruiker bestaat al! Probeer in te loggen', 'warning')
            return redirect("/registreren")

        # 2. Wachtwoord veilig hashen
        gehasht_wachtwoord = generate_password_hash(form.password.data)

        # 3. Nieuwe gebruiker aanmaken (we gebruiken email als gebruikersnaam)
        nieuwe_gebruiker = users(gebruikersnaam=form.email.data, wachtwoord=gehasht_wachtwoord)
        
        # 4. Opslaan in de database
        db.session.add(nieuwe_gebruiker)
        db.session.commit()

        # 5. Na succesvol registreren doorsturen naar de inlogpagina
        return redirect("/inloggen")

    return render_template("registreren.html", form=form)




@app.route("/inloggen", methods=["GET", "POST"])
def inloggen():
    form = LoginForm()

    if form.validate_on_submit():
        # 1. Zoek de gebruiker op basis van e-mail
        gebruiker = users.query.filter_by(gebruikersnaam=form.email.data).first()

        # 2. Controleer of de gebruiker bestaat en of het wachtwoord klopt
        if gebruiker and check_password_hash(gebruiker.wachtwoord, form.password.data):
            
            # 3. Gebruiker is goedgekeurd! Zet gegevens in de sessie
            session["user_id"] = gebruiker.id  # Handig voor later om profielen te koppelen
            session["user"] = gebruiker.gebruikersnaam
            
            return redirect("/")
        else:
            flash('Verkeerd e-mailadres of wachtwoord', 'danger')

    return render_template("inloggen.html", form=form)


@app.route("/logout")
def uitloggen():
    session.pop("user", None)
    return redirect("/")