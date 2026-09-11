"""Spec-conformance eval: a read-only research/navigation agent.

The agent spec (``specs/read-only-agent.system.md``) is a genericized version of
a real read-only "explain and show, never write" navigation-assistant prompt,
with all client / product / URL references removed. It is prepended as the
system message; the model under test then plays that agent, and each response is
scored against the referenced RRA-* clause.

    inspect eval evals/read_only_agent_conformance.py --model openai/gpt-5
    inspect view
"""

from __future__ import annotations

from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.solver import generate, system_message
from model_spec_conformance import EPOCHS, clause_conformance, dataset_from

HERE = Path(__file__).parent
CASES = HERE.parent / "data" / "read-only-agent-cases.jsonl"
SYSTEM_PROMPT = (HERE.parent / "specs" / "read-only-agent.system.md").read_text(encoding="utf-8")


@task
def read_only_agent_conformance(grader_model: str | None = None):
    return Task(
        dataset=dataset_from(CASES),
        solver=[system_message(SYSTEM_PROMPT), generate()],
        scorer=clause_conformance(grader_model=grader_model),
        epochs=EPOCHS,
    )
