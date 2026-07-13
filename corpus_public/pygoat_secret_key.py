# Extrait reel du projet OWASP PyGoat (source publique et documentee)
# Repo : https://github.com/adeyosemanputra/pygoat
# Fichier original : pygoat/settings.py (lignes 1-29)
# OWASP PyGoat est une application Django deliberement vulnerable,
# maintenue par l'OWASP pour l'apprentissage des vulnerabilites (OWASP Top 10).

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lr66%-a!$km5ed@n5ug!tya5bv!0(yqwa1tn!q%0%3m2nh%oml'

SENSITIVE_DATA = 'FLAGTHATNEEDSTOBEFOUND'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True