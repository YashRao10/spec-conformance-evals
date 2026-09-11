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
