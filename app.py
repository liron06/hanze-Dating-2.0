from flask import Flask, render_template, session, redirect
from forms import LoginForm
from models import db, migrate, users, profiles
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


@app.route("/registreren", methods=["GET", "POST"])
def registreren():
    form = LoginForm()

    if form.validate_on_submit():
        session["user"] = form.email.data
        return redirect("/")

    return render_template("registreren.html", form=form)




@app.route("/inloggen", methods=["GET", "POST"])
def inloggen():
    form = LoginForm()

    if form.validate_on_submit():
        session["user"] = form.email.data
        return redirect("/")

    return render_template("inloggen.html", form=form)


@app.route("/logout")
def uitloggen():
    session.pop("user", None)
    return redirect("/")