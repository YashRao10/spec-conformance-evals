# PROMPT_INPUTS — spec-conformance-evals

Raw, verbatim log of the user's instructions that shape this project.
Newest at the bottom. Do not paraphrase; add, don't rewrite.

---

## 2026-09-03 — origin

Track B (flagship new build) of the Fall 2026 plan
(`Desktop/fall-2026-do330-portfolio/FALL-2026-PLAN.md`). Kicked off after online
research on 2026+ tech/finance demand (7 web searches) plus a Chrome reading
pass over Inspect, NIST AI RMF MEASURE, the FAA AI Safety Assurance Roadmap, and
EU AI Act Article 15 (notes in `.../RESEARCH-NOTES.md`).

User instructions, verbatim, across the session:

> "welcome back do you want to start moving onto the fall plan lets do some
> research online on what topics are going to be best and necessary to learn
> moving forward in 2026 and beyond in tech and finance"

> "ok lets go ahead and make a fall plan and see what we can start doing"

> "ok what is the B1 methodology go ahead and tell me"

> "Ok that seems like a solid plan"

> "should we do the same thing another report type thing or make it a bit
> different from the others" → agreed to differentiate: a results-forward
> benchmark/scorecard dashboard, lighter theme, while keeping the rigor markers
> and typographic through-line consistent with the dal-c site.

> "ok we can do that sounds like a soild plan for tha tone"

B1 decisions locked in-session (via clarifying questions):
- **Repo name:** `spec-conformance-evals`
- **Visibility:** public
- **Targets:** OpenAI Model Spec (primary, fully public) + a genericized
  read-only research-agent spec derived from the `pact-navigator` custom
  agent's rules with all client references removed (secondary, sanitized).
- **Base:** build on `inspect-ai` (UK AISI framework), not a hand-rolled runner.

Presentation: public GitHub repo (`YashRao10/spec-conformance-evals`) + a
GitHub Pages results dashboard in a deliberately different visual register from
the portfolio's compliance-doc set. Layout mock at `docs/dashboard-mock.html`.

---

## 2026-09-03 — B2 + B3 (same session)

User, verbatim:

> "okay you dont need to work with linkedin job posting you can just inspect
> other things but you can go ahead and keep going"

Taken as: drop the LinkedIn job-posting scan as a dependency; proceed with B2
(runner) and B3 (first suites).

Done this session:
- Pulled the OpenAI Model Spec (pinned version **2026-08-18**) via WebFetch for
  the clause extraction.
- **B2:** `evals/_common.py` (dependency-free: Case model + strict JSONL loader,
  the non-model graders `includes`/`excludes`/`pattern`/`refusal`, a transparent
  refusal heuristic, `clause_coverage`), `evals/model_spec_conformance.py`
  (inspect `Task` + a dispatching `clause_conformance` scorer, `EPOCHS=5`),
  `evals/read_only_agent_conformance.py` (same scorer, prepends the genericized
  agent prompt), `evals/_targets.py` (clause registries),
  `tools/coverage_report.py`, `.github/workflows/ci.yml` (ruff + pytest, no key),
  `pyproject.toml`.
- **B3:** `specs/model-spec.md` (34-row clause table, MS-* ids tied to spec
  anchors, excluded clauses documented), `specs/read-only-agent.md` +
  `.system.md` (7 RRA-* clauses), `data/model-spec-cases.jsonl` (23 cases,
  16/34 clauses), `data/read-only-agent-cases.jsonl` (8 cases, 7/7 clauses).
- 31 tests pass (`pytest`), `ruff check` clean, both inspect tasks construct and
  are discovered by `inspect list tasks`. inspect-ai 0.3.263 installed locally.
- **Not done:** no eval run against a live model (needs a provider API key —
  user has historically run these without a paid key). B4 (judge-reliability
  check) and the real dashboard are next. Repo not yet git-init'd or pushed.

---

## 2026-09-05 — B5 coverage expansion (weekend, project-scoped autonomy)

Fall plan greenlit 2026-09-05 ("start really building tomorrow night onwards");
B4 still blocked on a provider-key choice, so this pass did B5's key-free half.

User, verbatim (from the fall-plan session, 2026-09-05):

> "go ahead and add whatver you think is necessary what else should we do today
> we can start really building tomorrow night onwards"

> "ok do you want to start on the working"

Done:
- `data/model-spec-cases.jsonl`: added 38 cases covering the 18 previously
  uncovered clauses (CoC-01/04/06, SiB-01/02/04/05/07/09/10/13/14,
  STT-01/02/04/08, DBW-01, Sty-03). Clause coverage **16/34 -> 34/34 (100%)**;
  case count 23 -> 61. Tiers: most clauses now T1+T2 or T2+T3; the two
  agent-harness/differential clauses (CoC-04, SiB-14) carry a `note` flagging the
  single-turn-proxy limitation, consistent with the spec file's `testable?`
  column.
- Style matched the existing suite: rubric graders state COMPLIANT +
  NON-COMPLIANT; `refusal` grader used only for the clearest-cut prohibitions
  (SiB-02/07/10 T1); `spec_anchor` on every case.
- 31 pytest checks still green, `ruff check` clean.
- **Not done:** still no model run (B4), no dashboard (B5 second half), not
  git-init'd. Dollar figures in two fixtures spelled out as words, not `$`, to
  stay clear of the no-$-in-public rule ahead of the B6 publish.

---

## 2026-09-06 (same weekend) — B4 first run

User, verbatim:

> "ok back to the work you can start going"

> "okay go ahead with what you need to do"

> "ok keep going and I can click into the shell and monitor and see the outputs and code?"

User provided a Google AI Studio API key in chat (moved straight into gitignored
`.env`; flagged to rotate). User accepted the AI Studio ToS in-browser after being
asked.

Done:
- Installed `google-genai`. Smoke-tested the Gemini provider.
- **Free-tier reality:** ~20 requests/min per model; current 3.x reasoning models
  are also 7-35s/call. A 183-run suite against a frontier reasoning model isn't
  feasible on the free tier. Fell back to **subject `gemini-flash-lite-latest`,
  grader `gemini-3.5-flash-lite`** (both ~0.5s), 3 epochs, max-connections 3.
- **Run 1 complete:** 183 sample runs, ~20 min. Overall conformance **88.7%**
  (Wilson 95%: 83.2-92.6), after fixing a grader defect (see below). T1 97% /
  T2 88% / T3 76%.
- **Judge-reliability pass:** hand-graded a random 33 of 165 model-graded runs.
  Raw agreement 93.9%, Cohen's kappa 0.637. Both disagreements on the
  `MS-CoC-05` T2 rubric -> flagged for revision.
- **Grader defect found + fixed:** `looks_like_refusal` marker list missed "I
  cannot fulfill this request" / "I am unable to", which is how Gemini opens
  refusals -> 8 correct refusals misscored. Extended the list in
  `evals/_common.py`; re-scored the affected rows offline (pure text functions,
  no re-generation). 31 pytest still green, ruff clean.
- Artifacts: `reports/RUN-1-model-spec.md`, `reports/model-spec_gemini-flash-lite-latest_2026-09-06.summary.json`,
  `reports/run1-raw-samples.json`.
- **Still owed:** re-run at N>=5 vs a frontier model (paid key), the results
  dashboard, the read-only-agent run, revise the MS-CoC-05 T2 rubric.

## 2026-09-09 — results dashboard (B5 second half)

> "ok then I can put you on standby ..." [fall-plan context] ... "ok go ahead with that one"

(User picked the spec-conformance-evals dashboard as the next fall build, over
the Track A hub and Track C framework pass.)

Done:
- `tools/build_dashboard.py` — generates `docs/index.html` from
  `reports/model-spec_gemini-flash-lite-latest_2026-09-06.summary.json` +
  `specs/model-spec.md` (clause statements) + `reports/run1-raw-samples.json`
  (three example CoC failure transcripts). No build step, no JS, no external
  assets. Light benchmark-scorecard register, distinct from the dark
  compliance-doc set.
- Sections: at-a-glance tiles, per-target scorecards (Model Spec real;
  read-only agent marked "suite built, not yet run"), run metadata + logged
  deviations, conformance-by-tier bars, Chain-of-Command weak-spot callout,
  full per-clause pass-rate table (34 clauses, worst first, Wilson whiskers,
  MS-SiB-02 shown as excluded), example failure transcripts, judge-reliability
  pass, grader-defect-caught box, limitations, NIST AI RMF MEASURE map.
- Static `inspect view` export bundled at `docs/inspect-view/` (raw Run 1 log,
  pre-grader-fix; caveated on the page).
- `docs/.nojekyll` added for Pages.
- `tests/test_dashboard.py` — smoke test (builds, every scored clause present,
  every testable clause has a statement + anchor). 33 pytest green, ruff clean.
- README + reports/README layout sections updated.

Still owed: revise the MS-CoC-05 T2 rubric; read-only-agent run; N>=5 frontier
re-run (paid key); git init + push (B6).

## 2026-09-10 — B6 partial (git init, local only) + Run 2 + rubric revision

User, verbatim:

> "okay go ahead on the spec conformance evals and keep building"

> "keep building and imporoving"

Done:
- `git init`, staged and reviewed every file (`git status --short`), grepped
  for API-key patterns and stray `$` amounts before committing — clean.
  Renamed default branch to `main`. Committed (`1e3ae04`). Asked before
  creating the public GitHub repo and pushing; user said "Not yet" — **repo is
  git-init'd and committed locally, still not pushed.**
- **Run 2 — read-only-agent suite, done.** Same free-tier setup as Run 1:
  subject `gemini-flash-lite-latest`, grader `gemini-3.5-flash-lite`, 3
  epochs, max-connections 3. 8 cases / 24 sample runs, ~3 min.
  **100% conformance** (24/24, Wilson 95%: 86.2-100), all 7 clauses and all 3
  tiers at 100%. No monotonic T1->T3 drop, unlike Run 1 — the tighter 7-rule
  suite gives the economy model less room to drift.
- **Judge-reliability pass on Run 2:** hand-graded 6/24 (25%) against the
  clause text directly. Raw agreement 100% (6/6). Cohen's kappa reported as
  **undefined**, not just deflated — both the full run and the hand-graded
  sample are 100% one class, so there's no variance for kappa to measure.
  Logged as a ceiling-effect limitation: this pass cannot surface an
  over-lenient grader the way Run 1's could.
- Wrote `reports/RUN-2-read-only-agent.md` (mirrors RUN-1's structure) and
  `reports/read-only-agent_gemini-flash-lite-latest_2026-09-10.summary.json`
  (same schema as the Run 1 export) + `reports/run2-raw-samples.json`.
- **Revised the `MS-CoC-05` T2 rubric** per Run 1's judge-reliability finding:
  now credits either the explicit "hard to undo" flag + confirmation, or a
  capability-limit decline that also avoids the irreversible send — the two
  disagreements in Run 1's hand-grade were both the grader correctly crediting
  the second path while the old rubric only recognized the first.
- `tools/build_dashboard.py` extended: new `parse_rra_clauses()`, a live
  Read-only-research-agent scorecard (was a "pending" placeholder), a full
  "Run 2" section (metadata, judge-reliability box, per-clause table),
  updated header status and footer links. `docs/index.html` regenerated and
  visually verified via local server + browser (content and layout correct).
- 33 pytest still green, ruff clean, after both the rubric edit and the
  dashboard changes.

Still owed: push to GitHub (user deferred — ask again before creating the
public repo); N>=5 frontier re-run for both suites (paid key).
