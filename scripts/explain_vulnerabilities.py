import json
import os
import re
from dotenv import load_dotenv
from mistralai.client import Mistral
from json_repair import repair_json

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)


def get_code_snippet(filename, line_number, window=3):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    start = max(0, line_number - window - 1)
    end = min(len(lines), line_number + window)
    return "".join(lines[start:end])


def explain_vulnerability(vuln):
    filename = vuln["filename"]
    line_number = vuln["line_number"]
    issue_text = vuln["issue_text"]

    try:
        code_snippet = get_code_snippet(filename, line_number)
    except FileNotFoundError:
        code_snippet = "# [Fichier non trouve]"

    prompt = (
        "Tu es un expert en securite informatique. Analyse cette vulnerabilite detectee par Bandit :\n\n"
        f"Fichier : {filename}\n"
        f"Ligne : {line_number}\n"
        f"Probleme : {issue_text}\n"
        f"Code :\n{code_snippet}\n\n"
        "Reponds UNIQUEMENT en JSON avec ce format :\n"
        "{\n"
        '  "explication": "Explication claire en francais...",\n'
        '  "correctif": "code corrige ici",\n'
        '  "criticite": "Critique|Elevee|Moyenne|Faible",\n'
        '  "faux_positif": false,\n'
        '  "raison_faux_positif": null\n'
        "}\n"
    )

    response = client.chat.complete(
        model="mistral-tiny",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def main():
    with open("results/bandit_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)

    enriched_vulns = []
    for vuln in report["vulnerabilities"]:
        print(f"Traitement de {vuln['filename']}:{vuln['line_number']}...")
        try:
            raw = explain_vulnerability(vuln)
            match = re.search(r'\{.*\}', raw, re.DOTALL)
            if match:
                repaired = repair_json(match.group(0))
                enriched = json.loads(repaired)
            else:
                enriched = {
                    "explication": "Erreur de parsing.",
                    "correctif": "Non disponible",
                    "criticite": "Inconnu",
                    "faux_positif": False,
                    "raison_faux_positif": None
                }
            enriched.update(vuln)
            enriched_vulns.append(enriched)
        except Exception as e:
            print(f"Erreur : {e}")
            enriched_vulns.append(vuln)

    with open("results/enriched_report.json", "w", encoding="utf-8") as f:
        json.dump({"vulnerabilities": enriched_vulns}, f, indent=2, ensure_ascii=False)

    print("Rapport enrichi sauvegarde dans results/enriched_report.json")


if __name__ == "__main__":
    main()