import argparse
import json
import subprocess
import os
import re
from dotenv import load_dotenv
from mistralai.client import Mistral
from json_repair import repair_json

load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=MISTRAL_API_KEY)


def run_bandit(file_path):
    result = subprocess.run(
        ["bandit", "-r", file_path, "-f", "json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)


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
    code_snippet = get_code_snippet(filename, line_number)

    prompt = (
        "Tu es un expert en securite informatique. Analyse cette vulnerabilite.\n\n"
        f"Fichier : {filename}\n"
        f"Ligne : {line_number}\n"
        f"Probleme : {issue_text}\n"
        f"Code :\n{code_snippet}\n\n"
        "Reponds UNIQUEMENT avec un objet JSON valide, sans texte avant ni apres, "
        "sans blocs de code markdown, sur ce format exact :\n"
        '{"explication": "...", "correctif": "...", "criticite": "Critique|Elevee|Moyenne|Faible"}\n'
    )

    response = client.chat.complete(
        model="mistral-tiny",
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    result = {"explication": "Non disponible", "correctif": "Non disponible", "criticite": "Inconnu"}
    if match:
        try:
            repaired = repair_json(match.group(0))
            parsed = json.loads(repaired)
            if isinstance(parsed, dict):
                result.update(parsed)
        except Exception:
            pass
    return result


def main():
    parser = argparse.ArgumentParser(description="Mini-SecureAudit : audit de securite pour code Python")
    parser.add_argument("file", help="Fichier Python a auditer")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Erreur : le fichier {args.file} n'existe pas.")
        return

    print(f"Audit du fichier : {args.file}\n")
    bandit_results = run_bandit(args.file)
    vulnerabilities = bandit_results.get("results", [])

    if not vulnerabilities:
        print("Aucune vulnerabilite detectee par Bandit.")
        return

    print(f"{len(vulnerabilities)} vulnerabilite(s) detectee(s).\n")

    for vuln in vulnerabilities:
        try:
            enriched = explain_vulnerability(vuln)
        except Exception as e:
            enriched = {"explication": f"Erreur : {e}", "correctif": "Non disponible", "criticite": "Inconnu"}

        print(f"Fichier : {vuln['filename']}")
        print(f"Ligne {vuln['line_number']} : {vuln['issue_text']}")
        print(f"Explication : {enriched.get('explication', 'Non disponible')}")
        print(f"Correctif : {enriched.get('correctif', 'Non disponible')}")
        print(f"Criticite : {enriched.get('criticite', 'Inconnu')}")
        print("-" * 60)


if __name__ == "__main__":
    main()
