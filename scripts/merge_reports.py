import json
import glob

all_vulnerabilities = []
for file in glob.glob("results/bandit_*.json"):
    with open(file, "r") as f:
        data = json.load(f)
        all_vulnerabilities.extend(data.get("results", []))

with open("results/bandit_report.json", "w") as f:
    json.dump({"vulnerabilities": all_vulnerabilities}, f, indent=2)

print(f"✅ Fusion terminée : {len(all_vulnerabilities)} vulnérabilités détectées.")