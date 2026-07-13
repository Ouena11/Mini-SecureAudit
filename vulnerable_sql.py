# Ce fichier contient une vulnérabilité d'injection SQL
import sqlite3

def get_user(username):
    """Récupère un utilisateur par son nom (VULNÉRABLE À L'INJECTION SQL)."""
    conn = sqlite3.connect(":memory:")  # Base en mémoire pour l'exemple
    cursor = conn.cursor()

    # ❌ PROBLÈME : Concaténation directe de la variable dans la requête
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    return cursor.fetchall()

# Exemple d'utilisation
get_user("admin")  # Un attaquant pourrait passer : admin' OR '1'='1