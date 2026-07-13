# Extrait reel du projet OWASP PyGoat (source publique et documentee)
# Repo : https://github.com/adeyosemanputra/pygoat
# Fichier original : introduction/views.py (fonction sql_lab, ligne 158)
# OWASP PyGoat est une application Django deliberement vulnerable,
# maintenue par l'OWASP pour l'apprentissage des vulnerabilites (OWASP Top 10).

def sql_lab(request):
    name = request.POST.get('name')
    password = request.POST.get('pass')

    if name:
        sql_query = "SELECT * FROM introduction_login WHERE user='" + name + "' AND password='" + password + "'"
        print(sql_query)
        try:
            val = login.objects.raw(sql_query)
        except Exception:
            return None
        if val:
            user = val[0].user
            return user