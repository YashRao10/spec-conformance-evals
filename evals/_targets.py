"""Registry of targets: the testable-clause list is the coverage denominator.

Keep this in sync with the clause tables in specs/<target>.md. The
`test_targets.py` check fails if a case references a clause id not listed here.
"""

from __future__ import annotations

# OpenAI Model Spec 2026-08-18 -- see specs/model-spec.md.
# `partial`-testability clauses are included; voice/minor/agent-only and
# aspirational-style clauses are excluded and listed in the spec file.
MODEL_SPEC_TESTABLE = [
    "MS-CoC-01", "MS-CoC-02", "MS-CoC-03", "MS-CoC-04", "MS-CoC-05", "MS-CoC-06", "MS-CoC-07",
    "MS-SiB-01", "MS-SiB-02", "MS-SiB-03", "MS-SiB-04", "MS-SiB-05", "MS-SiB-06", "MS-SiB-07",
    "MS-SiB-08", "MS-SiB-09", "MS-SiB-10", "MS-SiB-11", "MS-SiB-12", "MS-SiB-13", "MS-SiB-14",
    "MS-STT-01", "MS-STT-02", "MS-STT-03", "MS-STT-04", "MS-STT-05", "MS-STT-06", "MS-STT-07",
    "MS-STT-08",
    "MS-DBW-01", "MS-DBW-02",
    "MS-Sty-01", "MS-Sty-02", "MS-Sty-03",
]

READ_ONLY_AGENT_TESTABLE = [
    "RRA-01", "RRA-02", "RRA-03", "RRA-04", "RRA-05", "RRA-06", "RRA-07",
]

TARGETS = {
    "model-spec": MODEL_SPEC_TESTABLE,
    "read-only-agent": READ_ONLY_AGENT_TESTABLE,
}
