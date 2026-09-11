"""Check the case suites against the target clause registries. CI, no model."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "evals"))
sys.path.insert(0, str(ROOT / "tools"))

from _common import load_cases  # noqa: E402
from _targets import TARGETS  # noqa: E402
from coverage_report import SUITE_FILES, build  # noqa: E402


@pytest.mark.parametrize("name", list(TARGETS))
def test_no_case_cites_an_unregistered_clause(name):
    testable = set(TARGETS[name])
    bad = {c.clause_id for c in load_cases(SUITE_FILES[name]) if c.clause_id not in testable}
    assert not bad, f"{name}: cases cite clause ids missing from _targets.py: {sorted(bad)}"


def test_coverage_report_builds():
    report = build()
    assert set(report) == set(TARGETS)
    for name, cov in report.items():
        assert 0.0 <= cov["clause_coverage"] <= 1.0
        assert not cov["orphan_case_clause_ids"], name


def test_coverage_is_making_progress():
    """Guard against the suites silently emptying out."""
    report = build()
    assert report["model-spec"]["clause_coverage"] >= 0.25
    assert report["read-only-agent"]["clause_coverage"] >= 0.75
