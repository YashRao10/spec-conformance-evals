"""Smoke test for the dashboard generator. Runs in CI, no model needed.

Catches a broken template, a schema drift in the run export, or a missing
clause statement before the Pages site is regenerated from a stale build.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
spec = importlib.util.spec_from_file_location(
    "build_dashboard", ROOT / "tools" / "build_dashboard.py"
)
bd = importlib.util.module_from_spec(spec)
sys.modules["build_dashboard"] = bd
spec.loader.exec_module(bd)


def test_dashboard_builds_and_covers_every_scored_clause():
    import json

    html = bd.build()
    assert html.lstrip().startswith("<!doctype html>")
    assert "{" not in html.split("<style>")[0]  # no unfilled f-string braces in the head

    summary = json.loads(bd.SUMMARY.read_text(encoding="utf-8"))
    for cid in summary["by_clause"]:
        assert cid in html, f"{cid} missing from the per-clause table"

    # headline figure and the judge-reliability number must both render
    assert f'{summary["overall"]["rate"] * 100:.1f}%' in html
    assert "&kappa;" in html


def test_every_testable_clause_has_a_statement():
    clauses = bd.parse_spec_clauses(bd.SPEC.read_text(encoding="utf-8"))
    assert len(clauses) == 34
    for cid, meta in clauses.items():
        assert meta["statement"], f"{cid} has no statement text"
        assert meta["anchor"].startswith("#"), f"{cid} anchor looks wrong: {meta['anchor']}"
