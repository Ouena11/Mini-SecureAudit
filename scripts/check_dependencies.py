import sys
import json
import urllib.request

def check_package(name, version):
    url = f"https://pypi.org/pypi/{name}/{version}/json"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.load(resp)
    except Exception as e:
        return {"package": name, "version": version, "error": str(e), "vulnerabilities": []}

    vulns = data.get("vulnerabilities", [])
    ids = []
    for v in vulns:
        aliases = v.get("aliases", [])
        cve = next((a for a in aliases if a.startswith("CVE-")), v.get("id", "N/A"))
        if cve not in ids:
            ids.append(cve)
    return {"package": name, "version": version, "vulnerabilities": ids}


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_dependencies.py requirements.txt")
        return

    req_file = sys.argv[1]
    results = []

    with open(req_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "==" not in line:
                continue
            name, version = line.split("==")
            name = name.strip()
            version = version.strip()
            print(f"Verification de {name}=={version}...")
            result = check_package(name, version)
            results.append(result)

    print("\n" + "=" * 60)
    print("RAPPORT DE DEPENDANCES VULNERABLES")
    print("=" * 60)

    total_vulns = 0
    for r in results:
        if r.get("vulnerabilities"):
            total_vulns += len(r["vulnerabilities"])
            print(f"\n{r['package']}=={r['version']} — {len(r['vulnerabilities'])} CVE(s) :")
            for cve in r["vulnerabilities"][:5]:
                print(f"  - {cve}")

    print(f"\nTotal : {total_vulns} vulnerabilite(s) trouvee(s) sur {len(results)} dependance(s) analysee(s).")

    with open("results/dependency_scan.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()