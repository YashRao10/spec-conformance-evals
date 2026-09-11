# spec-conformance-evals

**Does the system do what its spec says — measurably, with the receipts?**

An LLM/agent evaluation harness that applies software-assurance discipline to
behavioral testing. Every test case traces to a numbered clause of the target's
written specification; coverage is measured against the clause set; and the
clauses that *cannot* be tested this way are documented rather than hidden.

Built on [`inspect-ai`](https://inspect.aisi.org.uk/). Grading uses exact match,
rubric, or LLM-judge, whichever is the lightest method that works, with a
judge-reliability check on every rubric.

Status (2026-09-10): **both suites run, results dashboard built, not yet
published.** 61 Model Spec cases (34/34 testable clauses), 8 read-only-agent
cases (7/7). Run 1 scored `gemini-flash-lite-latest` against the Model Spec
suite at **88.7% conformance** (Wilson 95%: 83.2 to 92.6), with a
judge-reliability pass (94% human agreement, kappa 0.64) that also caught and
fixed a grader defect; the `MS-CoC-05` T2 rubric flagged by that pass has since
been revised. Run 2 scored the same subject against the tighter read-only-agent
suite at **100% conformance** (24/24, Wilson 95%: 86.2 to 100) — see
[`reports/RUN-2-read-only-agent.md`](reports/RUN-2-read-only-agent.md) for why
that number is a real result but a low bar. See
[`reports/RUN-1-model-spec.md`](reports/RUN-1-model-spec.md) for the Run 1
writeup and [`docs/index.html`](docs/index.html) for the scorecard (regenerated
from both run exports by `tools/build_dashboard.py`; a static `inspect view`
export of every Run 1 sample sits at `docs/inspect-view/`). Repo is git-init'd
locally (`main`, not yet pushed). Next: publish to GitHub, re-run both suites at
N >= 5 against a frontier subject and grader.

---

## Why this exists

Conventional software verification writes requirements, traces tests to them,
and measures requirement coverage plus structural coverage. You cannot write
complete requirements for an LLM's behavior — but you can take its *spec* (a
system prompt, a policy document, a model behavior spec) and treat each
normative clause as a testable requirement. That is the method here. It is the
same discipline used in DO-178C / DO-330 software and tool qualification,
applied to a target you can only specify partially.

See [`METHODOLOGY.md`](METHODOLOGY.md) for the full method, the coverage
definition, the NIST AI RMF MEASURE mapping, and the limitations.

## Targets

| Target | Spec source | Public? |
|---|---|---|
| **OpenAI Model Spec** | the published Model Spec | fully public |
| **Read-only research agent** | a genericized agent spec (client references removed) | sanitized, public |

## Layout

```
specs/     verbatim spec text + the numbered clause table for each target
             model-spec.md            clause table (MS-*)
             read-only-agent.md        clause table (RRA-*)
             read-only-agent.system.md the genericized agent prompt under test
evals/     _common.py    dependency-free helpers (graders, loader, coverage)
             _targets.py   testable-clause registries (coverage denominators)
             *_conformance.py  one inspect Task per target
data/      *-cases.jsonl   cases: {clause_id, tier, grader, input, target, spec_anchor}
tools/     coverage_report.py   clause coverage from the committed suites
             build_dashboard.py   regenerates docs/index.html from a run export
reports/   curated result exports (writeup + summary.json + raw samples)
tests/     CI checks: helper unit tests + suite integrity + dashboard smoke test
docs/      index.html   results dashboard (Pages site), generated
             inspect-view/  static inspect view export of Run 1 (raw log)
             dashboard-mock.html  original layout wireframe
```

## Use

```bash
pip install -r requirements.txt          # inspect-ai + pytest
pip install openai anthropic             # whichever provider(s) you target

pytest -q                                # helper + suite-integrity checks (no key)
python tools/coverage_report.py          # clause coverage, per target
python tools/build_dashboard.py          # regenerate docs/index.html from reports/

inspect eval evals/model_spec_conformance.py --model openai/gpt-5
inspect eval evals/read_only_agent_conformance.py --model openai/gpt-5
inspect view                             # transcripts + per-sample scores
```

Grading is dispatched per case on the `grader` field: `includes` / `excludes` /
`pattern` / `refusal` are pure functions in `_common.py`; `model` sends the
response to a grader model for a COMPLIANT / NON-COMPLIANT / UNCLEAR verdict.
Every case runs `EPOCHS` (5) times — report per-clause pass rate + stderr.

## Not in scope

- Adversarial / jailbreak testing — that is a separate project.
- Capability benchmarking (is the model *good*) — this measures *conformance*,
  not quality.
- Any client or employer system. The method is portable and public; client
  specifics are not.

## License

MIT
