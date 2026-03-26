from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class users(db.Model):
    __tablename__ = "gebruikers"

    id: Mapped[int] = mapped_column(primary_key=True)
    gebruikersnaam: Mapped[str] = mapped_column(unique=True, nullable=False)
    wachtwoord: Mapped[str] = mapped_column(nullable=False)

    profiel = relationship("profiles", back_populates="gebruiker", uselist=False)

    def __init__(self, gebruikersnaam, wachtwoord):
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord


class profiles(db.Model):
    __tablename__ = "profielen"

    id: Mapped[int] = mapped_column(primary_key=True)
    gebruiker_id: Mapped[int] = mapped_column(ForeignKey("gebruikers.id"), unique=True, nullable=False)
    naam: Mapped[str] = mapped_column(nullable=False)
    leeftijd: Mapped[int] = mapped_column(nullable=False)
    geslacht: Mapped[str] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(nullable=False)

    gebruiker = relationship("users", back_populates="profiel")

    def __init__(self, gebruiker_id, naam, leeftijd, geslacht, bio):
        self.gebruiker_id = gebruiker_id
        self.naam = naam
        self.leeftijd = leeftijd
        self.geslacht = geslacht
        self.bio = bio