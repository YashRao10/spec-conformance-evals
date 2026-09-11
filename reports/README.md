Curated result exports. Raw `inspect` logs (`*.eval`) stay in `logs/`, gitignored.

## Run 1 — 2026-09-06

- `RUN-1-model-spec.md` — the writeup: headline, tier breakdown, per-clause
  failures, judge-reliability pass, the grader defect it surfaced, limitations.
- `model-spec_gemini-flash-lite-latest_2026-09-06.summary.json` — machine-readable:
  per-clause pass rates with Wilson intervals, per-tier, judge kappa.
- `run1-raw-samples.json` — every sample run: prompt, rubric, model response,
  grader verdict + explanation. The reproducibility record.

Subject `google/gemini-flash-lite-latest`, grader `google/gemini-3.5-flash-lite`,
3 epochs, 61 cases. Overall conformance 88.7% (Wilson 95%: 83.2 to 92.6).

## Run 2 — 2026-09-10

- `RUN-2-read-only-agent.md` — the writeup: first run of the read-only-agent
  suite, judge-reliability pass, ceiling-effect limitation.
- `read-only-agent_gemini-flash-lite-latest_2026-09-10.summary.json` —
  machine-readable, same schema as Run 1.
- `run2-raw-samples.json` — every sample run, same shape as Run 1's.

Subject/grader same pair as Run 1, 3 epochs, 8 cases. Overall conformance 100%
(Wilson 95%: 86.2–100) — a real result but a low bar; see the writeup's
ceiling-effect discussion.

## Run 3 — 2026-09-11

- `RUN-3-read-only-agent-expanded.md` — the writeup: 4 new compound-tension T3
  cases added to the read-only-agent suite, N=5 (methodology floor finally
  met for this suite), and a genuine judge-reliability catch — a grader
  hallucination and a rubric under-specification, both found by hand-grading
  70% of the new cases' runs. **Read this one for the actual finding, not just
  the headline number.**
- `read-only-agent_gemini-flash-lite-latest_2026-09-11.summary.json` —
  machine-readable; flags which clauses' automated figures are superseded.
- `run3-raw-samples.json` — every sample run.

Subject/grader same pair as Runs 1–2, 5 epochs, 12 cases (8 original + 4 new).
Automated overall 100% (60/60) — **but 2 of the 4 new cases' rubrics were
revised post-hoc after hand-grading found the automated grader unreliable on
them (kappa forced to 0, 71.4% raw agreement on the hand-graded sample); their
true pass rate is not yet re-measured.** The other 5 clauses are unaffected.
