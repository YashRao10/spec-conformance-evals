"""Integrity checks for the committed case suites. Runs in CI, no model needed.

Catches malformed JSONL, bad tier/grader values, empty prompts or rubrics, and
duplicate cases before an eval run wastes API spend on them.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "evals"))

from _common import load_cases  # noqa: E402

SUITES = {
    "model-spec": (ROOT / "data" / "model-spec-cases.jsonl", "MS-"),
    "read-only-agent": (ROOT / "data" / "read-only-agent-cases.jsonl", "RRA-"),
}


@pytest.mark.parametrize("name", list(SUITES))
def test_suite_loads_and_is_well_formed(name):
    path, prefix = SUITES[name]
    cases = load_cases(path)  # raises on any malformed row
    assert len(cases) >= 5, f"{name}: suite is suspiciously small"

    for c in cases:
        assert c.clause_id.startswith(prefix), f"{name}: {c.clause_id} lacks {prefix} prefix"
        # model-graded rubrics must state both verdict directions
        if c.grader == "model":
            t = c.target.upper()
            assert "COMPLIANT" in t and "NON-COMPLIANT" in t, (
                f"{name}/{c.clause_id}/{c.tier}: rubric needs COMPLIANT + NON-COMPLIANT"
            )


@pytest.mark.parametrize("name", list(SUITES))
def test_no_duplicate_cases(name):
    path, _ = SUITES[name]
    # same scenario under two graders is deliberate (e.g. a pattern check for a
    # hotline number alongside a model rubric); a fully identical row is not.
    seen = set()
    for c in load_cases(path):
        key = (c.clause_id, c.tier, c.grader, c.input)
        assert key not in seen, f"{name}: duplicate case {key[:3]}"
        seen.add(key)


@pytest.mark.parametrize("name", list(SUITES))
def test_suite_exercises_multiple_tiers(name):
    """The tier system should actually be used, not collapsed to a single tier."""
    path, _ = SUITES[name]
    tiers = {c.tier for c in load_cases(path)}
    assert len(tiers) >= 2, f"{name}: only tier(s) {tiers} present; suite should span T1/T2/T3"
