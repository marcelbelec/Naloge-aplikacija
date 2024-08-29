#!/bin/sh

# Spremenljivke
export FLASK_APP=app.py
export FLASK_ENV=development

# Zagon Flask aplikacije
python -m flask run  # Uporabi ta ukaz, ker deluje ne glede na pot
