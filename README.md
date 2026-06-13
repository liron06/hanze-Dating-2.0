#  Hanze-Dating

##  Over het project

Hanze-Dating is een datingwebapplicatie ontwikkeld Door Liron en Job als project voor de opleiding **HBO-ICT (Jaar 1)** aan de **Hanzehogeschool Groningen**.

Gebruikers kunnen een account aanmaken, een persoonlijk profiel beheren, andere gebruikers bekijken en likes geven. Het project is ontwikkeld om ervaring op te doen met webontwikkeling, databases en gebruikersauthenticatie binnen Python.

---

##  Functionaliteiten

###  Accountbeheer
- Registreren van een nieuw account
- Inloggen
- Uitloggen
- Account verwijderen

###  Profielbeheer
- Persoonlijk profiel aanmaken
- Profielgegevens bewerken
- Profielinformatie bekijken

###  Likesysteem
- Andere gebruikers liken
- Voorkomen van dubbele likes
- Opslaan van likes in de database

###  Beveiliging
- Wachtwoorden worden gehasht opgeslagen
- Beschermde pagina's met Flask-Login
- Sessiebeheer voor ingelogde gebruikers

---

##  Gebruikte technologieën

### Backend
- Python 3
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-Migrate

### Frontend
- HTML5
- CSS3
- Jinja2 Templates

### Database
- SQLite

### Overige Libraries
- Werkzeug Security
- Python Dotenv

---

##  Projectstructuur

```text
Hanze-Dating/
│
├── app.py
├── forms.py
├── models.py
├── database.sqlite
├── .env
│
├── templates/
│   ├── base.html
│   ├── homepage.html
│   ├── registreren.html
│   ├── inloggen.html
│   ├── profielen.html
│   ├── profiel_detail.html
│   ├── bewerk_profiel.html
│   └── over_ons.html
│
├── static/
│   ├── css/
│   ├── images/
│   └── uploads/
│
└── migrations/
```

---

##  Installatie

### 1. Clone de repository

```bash
git clone https://github.com/jouw-gebruikersnaam/Hanze-Dating.git
cd Hanze-Dating
```

### 2. Maak een virtuele omgeving aan

```bash
python -m venv venv
```

### 3. Activeer de virtuele omgeving

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 4. Installeer de benodigde packages

```bash
pip install -r requirements.txt
```

### 5. Maak een `.env` bestand aan

```env
SECRET_KEY=jouweigengeheimesleutel
```

### 6. Start de applicatie

```bash
python app.py
```

De applicatie is vervolgens bereikbaar via:

```text
http://127.0.0.1:5000
```

---

##  Database

De applicatie maakt gebruik van een SQLite-database.

Bij het opstarten van de applicatie worden de benodigde tabellen automatisch aangemaakt:

```python
with app.app_context():
    db.create_all()
```

---

##  Leerdoelen

Met dit project hebben wij de volgende vaardigheden ontwikkeld:

- Werken met Flask-routes
- Gebruikersauthenticatie implementeren
- Werken met databases via SQLAlchemy
- CRUD-functionaliteiten bouwen
- Templates gebruiken met Jinja2
- Veilig omgaan met gebruikersgegevens

---


---
