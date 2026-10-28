"""
CLI Runner for KAVACH Genetic Adversarial Red-Team Fuzzer.
Generates 500 mutated zero-day adversarial attacks and evaluates defense resilience.
Saves comprehensive results to docs/ADVERSARIAL_ROBUSTNESS.json.
"""

import os
import sys
import json

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs"))

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.security.adversarial_fuzzer import AdversarialFuzzer


def main():
    print("=" * 76)
    print("  KAVACH ADVERSARIAL RED-TEAM GENETIC FUZZING HARNESS")
    print("  Evaluating Zero-Day Mutation Robustness over 500 Adversarial Attacks")
    print("=" * 76)

    fuzzer = AdversarialFuzzer(seed=1337)
    print("\n[1/3] Synthesizing 500 mutated adversarial attack vectors...")
    mutations = fuzzer.generate_mutations(count=500)
    print(f"      Generated {len(mutations)} unique adversarial variants.")

    print("\n[2/3] Executing multi-stage security pipeline inspection...")
    report = fuzzer.evaluate_resilience(mutations)

    print("\n[3/3] Mutation Robustness Evaluation Summary:")
    print(f"      - Total Mutations Tested:     {report['total_mutations_tested']}")
    print(f"      - Total Threats Caught:       {report['total_threats_caught']}")
    print(f"      - Overall Mutation Catch:     {report['overall_mutation_resilience_pct']}%")
    print(f"      - Average Latency per Check:  {report['average_inspection_latency_ms']} ms")
    print(f"      - Operational Verdict:        {report['verdict']}")

    print("\n  [Category Breakdown]:")
    for cat, data in report["category_breakdown"].items():
        print(f"    * {cat:<15}: {data['caught']}/{data['total']} caught ({data['catch_rate_pct']}%)")

    # Persist report to docs/ADVERSARIAL_ROBUSTNESS.json
    os.makedirs(DOCS_DIR, exist_ok=True)
    out_file = os.path.join(DOCS_DIR, "ADVERSARIAL_ROBUSTNESS.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n[OK] Full adversarial robustness dossier saved to:")
    print(f"     file:///{out_file.replace(os.sep, '/')}")
    print("=" * 76)


if __name__ == "__main__":
    main()
