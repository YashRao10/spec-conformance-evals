#!/usr/bin/env python3
"""Print spec-clause coverage for each target, from the committed case suites.

    python tools/coverage_report.py            # text table
    python tools/coverage_report.py --json     # machine-readable

Coverage here is *case coverage of the clause set*, not correctness. It says
which clauses have at least one case and at which tiers -- nothing about whether
the model passes. See METHODOLOGY.md 3.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "evals"))

from _common import clause_coverage, load_cases  # noqa: E402
from _targets import TARGETS  # noqa: E402

SUITE_FILES = {
    "model-spec": ROOT / "data" / "model-spec-cases.jsonl",
    "read-only-agent": ROOT / "data" / "read-only-agent-cases.jsonl",
}


def build() -> dict:
    out = {}
    for name, testable in TARGETS.items():
        cases = load_cases(SUITE_FILES[name])
        cov = clause_coverage(cases, testable)
        cov["n_cases"] = len(cases)
        cov["n_testable_clauses"] = len(testable)
        out[name] = cov
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    report = build()

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    for name, cov in report.items():
        print(f"\n=== {name} ===")
        print(f"  cases:            {cov['n_cases']}")
        print(f"  testable clauses: {cov['n_testable_clauses']}")
        print(f"  clause coverage:  {cov['clause_coverage']:.0%}  "
              f"({len(cov['covered'])}/{cov['n_testable_clauses']})")
        if cov["uncovered"]:
            print(f"  not yet covered:  {', '.join(cov['uncovered'])}")
        if cov["orphan_case_clause_ids"]:
            print(f"  !! cases cite unknown clause ids: {', '.join(cov['orphan_case_clause_ids'])}")
        print("  tiers per covered clause:")
        for cid, tiers in cov["tiers_by_clause"].items():
            print(f"    {cid:<12} {' '.join(tiers)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
