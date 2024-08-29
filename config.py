from os import environ, path

# Osnovna mapa aplikacije
BASE_DIR = path.abspath(path.dirname(__file__))

# Osnovne nastavitve Flask aplikacije
SECRET_KEY = environ.get('SECRET_KEY') or 'long and hard to guess string'  # Skrivni ključ za aplikacijo
FLASK_APP = 'app.py'  # Ime glavne datoteke aplikacije
FLASK_DEBUG = 1  # Omogočimo debug način

# Nastavitve baze podatkov
SQLITE_DB = 'sqlite:///' + path.join(BASE_DIR, 'naloge.sqlite')  # Pot do SQLite baze
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or SQLITE_DB  # URL baze podatkov
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Onemogočimo sledenje spremembam v SQLAlchemy
