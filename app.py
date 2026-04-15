from flask import Flask, render_template, session, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistratieForm
from models import db, migrate, users, profiles, Like
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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'inloggen'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.context_processor
def inject_models():
    return dict(Like=Like)


@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/over_ons")
def over_ons():
    return render_template("over_ons.html")

@app.route("/profielen")
@login_required
def profielen():

    alle_profielen = profiles.query.all()

    return render_template("profielen.html", profielen=alle_profielen)

@app.route("/profiel/<int:user_id>")
@login_required
def profiel_detail(user_id):
    gekozen_profiel = profiles.query.filter_by(gebruiker_id=user_id).first_or_404()
    
    return render_template("profiel_detail.html", profiel=gekozen_profiel)

@app.route("/like/<int:profile_id>", methods=["POST"])
@login_required
def like_profiel(profile_id):
    bestaande_like = Like.query.filter_by(user_id=current_user.id, profile_id=profile_id).first()
    
    if bestaande_like:
        flash("Je hebt dit profiel al een hartje gegeven!", "info")
    else:
        nieuwe_like = Like(user_id=current_user.id, profile_id=profile_id)
        db.session.add(nieuwe_like)
        db.session.commit()
        flash("Like verstuurd! ❤️", "success")
    
    return redirect(url_for('profiel_detail', user_id=profiles.query.get(profile_id).gebruiker_id))   

@app.route("/profiel/bewerken", methods=["GET", "POST"])
@login_required
def bewerk_profiel():
    profiel = profiles.query.filter_by(gebruiker_id=current_user.id).first_or_404()
    form = RegistratieForm(obj=profiel)

    if form.validate_on_submit():
        profiel.naam = form.naam.data
        profiel.leeftijd = form.leeftijd.data
        profiel.geslacht = form.geslacht.data
        profiel.bio = form.bio.data
        
        db.session.commit()
        flash("Je profiel is bijgewerkt!", "success")
        return redirect(url_for('profiel_detail', user_id=current_user.id))

    return render_template("bewerk_profiel.html", form=form)

@app.route("/account/verwijderen", methods=["POST"])
@login_required
def verwijder_account():
    user = users.query.get(current_user.id)
    profiel = profiles.query.filter_by(gebruiker_id=current_user.id).first()

    if profiel:
        db.session.delete(profiel)
    db.session.delete(user)
    db.session.commit()

    logout_user()
    flash("Je account is succesvol verwijderd. Jammer dat je weggaat!", "info")
    return redirect(url_for('home'))

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
            login_user(gebruiker) 
            flash('Succesvol ingelogd!', 'success')
            return redirect(url_for("home"))
        else:
            flash('Verkeerd e-mailadres of wachtwoord', 'danger')

    return render_template("inloggen.html", form=form)

@app.route("/logout")
@login_required
def uitloggen():
    logout_user()
    flash("Je bent nu uitgelogd.", "info")
    return redirect(url_for("home"))