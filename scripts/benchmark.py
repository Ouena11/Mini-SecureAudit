import json

def main():
    with open("data/expected_results.json", "r", encoding="utf-8") as f:
        expected = json.load(f)["vulnerabilities"]

    with open("results/enriched_report.json", "r", encoding="utf-8") as f:
        detected = json.load(f)["vulnerabilities"]

    expected_keys = {f"{v['file']}:{v['line']}" for v in expected}
    detected_keys = {f"{v['filename'].lstrip('.').lstrip('\\').lstrip('/')}:{v['line_number']}" for v in detected}

    vrais_positifs = len(expected_keys & detected_keys)
    faux_negatifs = len(expected_keys - detected_keys)
    faux_positifs = len(detected_keys - expected_keys)

    print("Rapport de Benchmark")
    print("=" * 40)
    print(f"Vulnerabilites attendues : {len(expected_keys)}")
    print(f"Vulnerabilites detectees : {len(detected_keys)}")
    print(f"Vrais positifs : {vrais_positifs}")
    print(f"Faux negatifs : {faux_negatifs}")
    print(f"Faux positifs : {faux_positifs}")

    taux_detection = vrais_positifs / len(expected_keys) if expected_keys else 0
    taux_fp = faux_positifs / len(detected_keys) if detected_keys else 0

    print(f"\nTaux de detection : {taux_detection * 100:.1f}%")
    print(f"Taux de faux positifs : {taux_fp * 100:.1f}%")

    metrics = {
        "vrais_positifs": vrais_positifs,
        "faux_negatifs": faux_negatifs,
        "faux_positifs": faux_positifs,
        "taux_detection": taux_detection,
        "taux_faux_positifs": taux_fp
    }

    with open("results/benchmark_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    main()