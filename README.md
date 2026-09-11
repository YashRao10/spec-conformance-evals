# spec-conformance-evals

**Does the system do what its spec says — measurably, with the receipts?**

An LLM/agent evaluation harness that applies software-assurance discipline to
behavioral testing. Every test case traces to a numbered clause of the target's
written specification; coverage is measured against the clause set; and the
clauses that *cannot* be tested this way are documented rather than hidden.

Built on [`inspect-ai`](https://inspect.aisi.org.uk/). Grading uses exact match,
rubric, or LLM-judge, whichever is the lightest method that works, with a
judge-reliability check on every rubric.

Status (2026-09-11): **both suites run, results dashboard built, not yet
published.** 61 Model Spec cases (34/34 testable clauses), 12 read-only-agent
cases (7/7 clauses — 8 original + 4 new compound-tension T3 cases). Run 1
scored `gemini-flash-lite-latest` against the Model Spec suite at **88.7%
conformance** (Wilson 95%: 83.2 to 92.6), with a judge-reliability pass (94%
human agreement, kappa 0.64) that also caught and fixed a grader defect; the
`MS-CoC-05` T2 rubric flagged by that pass has since been revised. Run 2 scored
the same subject against the read-only-agent suite at **100% conformance**
(24/24, Wilson 95%: 86.2 to 100) — a real result but a low bar (N=3, economy
model, no monotonic tier drop). Run 3 (2026-09-11) expanded that suite with 4
new cases that each combine two rules under one tension, re-ran the whole
suite at **N=5** (60/60, 100% automated), and this time the judge-reliability
pass — hand-grading 70% of the new cases' runs — found the ceiling effect
crack: a real grader hallucination (a false "the model hedged" justification
for a response that had, in fact, confidently invented a specific button name)
and a rubric under-specification (a "closes the form" requirement satisfied by
responses that never closed the form). Raw hand-grade agreement came in at
71.4%, not the 100% the automated score implied. Both rubrics have been
revised; a re-run against them is the immediate next step. See
[`reports/RUN-3-read-only-agent-expanded.md`](reports/RUN-3-read-only-agent-expanded.md)
for the full finding, [`reports/RUN-2-read-only-agent.md`](reports/RUN-2-read-only-agent.md)
and [`reports/RUN-1-model-spec.md`](reports/RUN-1-model-spec.md) for the earlier
runs, and [`docs/index.html`](docs/index.html) for the scorecard (regenerated
from all three run exports by `tools/build_dashboard.py`; a static `inspect view`
export of every Run 1 sample sits at `docs/inspect-view/`). Repo is git-init'd
locally (`main`, not yet pushed). Next: re-run the 2 flagged compound cases
against their revised rubrics, publish to GitHub, re-run both suites at N >= 5
against a frontier subject *and grader* (Run 3 raises the stakes on the grader
half of that).

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
