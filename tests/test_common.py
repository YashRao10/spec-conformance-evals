"""Unit tests for evals/_common.py — no model / network needed. This is what CI runs."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "evals"))

from _common import (  # noqa: E402
    Case,
    clause_coverage,
    grade_excludes,
    grade_includes,
    grade_pattern,
    is_platform_blocked,
    load_cases,
    looks_like_refusal,
)

# ---- Case.validate --------------------------------------------------------

def test_case_validate_accepts_good_row():
    c = Case(clause_id="MS-1", tier="T1", grader="model", input="hi", target="rubric")
    assert c.validate() == []


@pytest.mark.parametrize(
    "kwargs,expected_fragment",
    [
        (dict(clause_id="", tier="T1", grader="model", input="x", target="y"), "clause_id"),
        (dict(clause_id="c", tier="T9", grader="model", input="x", target="y"), "bad tier"),
        (dict(clause_id="c", tier="T1", grader="nope", input="x", target="y"), "bad grader"),
        (dict(clause_id="c", tier="T1", grader="model", input="  ", target="y"), "empty input"),
        (dict(clause_id="c", tier="T1", grader="model", input="x", target=""), "empty target"),
    ],
)
def test_case_validate_flags_bad_rows(kwargs, expected_fragment):
    problems = Case(**kwargs).validate()
    assert any(expected_fragment in p for p in problems), problems


# ---- load_cases ---------------------------------------------------------

def test_load_cases_roundtrip(tmp_path):
    f = tmp_path / "c.jsonl"
    f.write_text(
        '{"clause_id":"MS-1","tier":"T1","grader":"refusal","input":"in","target":"out"}\n'
        "\n"
        '// a comment line is skipped\n'
        '{"clause_id":"MS-2","tier":"T3","grader":"includes","input":"in2","target":"out2"}\n',
        encoding="utf-8",
    )
    cases = load_cases(f)
    assert [c.clause_id for c in cases] == ["MS-1", "MS-2"]
    assert cases[1].tier == "T3"


def test_load_cases_raises_on_bad_json(tmp_path):
    f = tmp_path / "c.jsonl"
    f.write_text('{"clause_id": "MS-1", oops}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="invalid JSON"):
        load_cases(f)


def test_load_cases_raises_on_bad_row(tmp_path):
    f = tmp_path / "c.jsonl"
    row = '{"clause_id":"MS-1","tier":"T7","grader":"model","input":"i","target":"t"}\n'
    f.write_text(row, encoding="utf-8")
    with pytest.raises(ValueError, match="bad tier"):
        load_cases(f)


# ---- non-model graders --------------------------------------------------

def test_grade_includes_case_insensitive_by_default():
    assert grade_includes("The CRISIS line is 988", "crisis line")[0] is True
    assert grade_includes("no match here", "988")[0] is False


def test_grade_excludes_is_the_negation():
    assert grade_excludes("a clean response", "slur")[0] is True
    assert grade_excludes("contains the slur word", "slur")[0] is False


def test_grade_pattern_matches_regex_and_handles_bad_regex():
    assert grade_pattern("call 988 now", r"\b\d{3}\b")[0] is True
    ok, msg = grade_pattern("x", r"(unclosed")
    assert ok is False and "invalid regex" in msg


# ---- refusal heuristic ------------------------------------------------

@pytest.mark.parametrize(
    "text,expected",
    [
        ("I can't help with that. Here's why...", True),
        ("Sorry, but I can't provide instructions for that.", True),
        ("I must decline this request.", True),
        ("Sure, here is how you do it: step 1...", False),
        ("That's a great question! Let me explain the history.", False),
        # refusal buried deep should NOT trip the opening-window heuristic
        ("x" * 900 + " i can't provide that", False),
    ],
)
def test_looks_like_refusal(text, expected):
    assert looks_like_refusal(text)[0] is expected


# ---- platform-block sentinel --------------------------------------------

@pytest.mark.parametrize(
    "text,expected",
    [
        ("BLOCKED: BlockedReason.PROHIBITED_CONTENT", True),
        ("blocked: blockedreason.prohibited_content", True),
        ("  BlockedReason.OTHER  ", True),
        ("Sure, here is how you do it: step 1...", False),
        ("I can't help with that. Here's why...", False),
        ("", False),
    ],
)
def test_is_platform_blocked(text, expected):
    assert is_platform_blocked(text)[0] is expected


# ---- coverage ----------------------------------------------------------

def _c(clause_id, tier):
    return Case(clause_id=clause_id, tier=tier, grader="model", input="i", target="t")


def test_clause_coverage_basic():
    cases = [_c("A", "T1"), _c("A", "T2"), _c("B", "T1")]
    cov = clause_coverage(cases, ["A", "B", "C"])
    assert cov["clause_coverage"] == pytest.approx(2 / 3)
    assert cov["covered"] == ["A", "B"]
    assert cov["uncovered"] == ["C"]
    assert cov["tiers_by_clause"]["A"] == ["T1", "T2"]


def test_clause_coverage_flags_orphan_cases():
    cov = clause_coverage([_c("A", "T1"), _c("ZZZ", "T1")], ["A"])
    assert cov["orphan_case_clause_ids"] == ["ZZZ"]


def test_clause_coverage_empty_testable_list():
    assert clause_coverage([], [])["clause_coverage"] == 0.0
