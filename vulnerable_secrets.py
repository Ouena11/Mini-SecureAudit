# Ce fichier contient des secrets codés en dur (VULNÉRABLE)
API_KEY = "sk-1234567890abcdef"  # ❌ Clé API en dur
DB_PASSWORD = "SuperSecret123!"  # ❌ Mot de passe en dur
SECRET_TOKEN = "xyz789"          # ❌ Token en dur

def call_api():
    """Appelle une API avec une clé en dur (DANGEREUX)."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    print("Appel API avec clé :", headers)
    return {"status": "success"}

call_api()