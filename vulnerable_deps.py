# Ce fichier utilise une version vulnérable de la bibliothèque 'requests'
# ❌ requests==2.18.0 est vulnérable à CVE-2018-18074
import requests

def fetch_data(url):
    """Récupère des données depuis une URL (VULNÉRABLE)."""
    response = requests.get(url)  # ❌ Version obsolète
    return response.json()

# Exemple d'utilisation
fetch_data("https://api.example.com/data")