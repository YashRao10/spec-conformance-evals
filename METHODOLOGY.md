# Methodology

**Project:** spec-conformance-evals
**Status:** draft, 2026-09-03 (B1 of the Fall 2026 plan). Written before any eval
has been run; numbers and target-specific detail land as the suites are built.
**Author:** Yash Rao

---

## 1. Purpose and scope

This harness measures whether an LLM or LLM-driven agent **behaves in accordance
with its own written specification**, under normal and mildly adverse
conditions, in a way that is repeatable and documented.

In scope:
- Behavioral conformance to normative clauses of a written spec (system prompt,
  policy document, published model behavior spec, agent instructions).
- Measurement under non-adversarial and mild-pressure conditions.

Out of scope:
- Adversarial robustness / jailbreak resistance (separate work).
- Capability or quality benchmarking (is the output *good*, vs. is it
  *compliant*).
- Any evaluation of a client or employer system.

## 2. Method

### 2.1 Spec ingestion and clause extraction

Take the target's specification **verbatim**. Decompose it into numbered
**normative clauses**, each discrete "must / must not / always / never / only /
should" statement. Record each in a clause table:

| clause_id | text (verbatim or tight paraphrase) | type | testable? | notes |
|---|---|---|---|---|
| MS-014 | "The assistant should not provide ..." | prohibition | yes | |
| MS-027 | "Be helpful" | aspiration | no | too broad to falsify with a bounded case |

`testable? = no` clauses are kept in the table with a reason. Clause extraction
is a documented judgment call, not a claim that the decomposition is complete or
canonical. The verbatim spec text and the table live in `specs/<target>.md`.

### 2.2 Case authoring: three difficulty tiers

For each testable clause, author cases at up to three tiers:

| Tier | Definition | Purpose |
|---|---|---|
| **T1: plain** | An unambiguous scenario that should obviously invoke the clause. | Baseline: does the model comply at all. |
| **T2: realistic** | A naturalistic prompt where the clause applies but is not signposted. | "Deployment-like conditions" (NIST MEASURE 2.3). |
| **T3: pressure** | A benign competing incentive, a distractor, mild time pressure, or a plausible reason to cut the corner. **Not** a jailbreak or injection. | Does the clause hold when something pulls against it. |

Target 2–4 cases per clause. Every case record carries `clause_id` and `tier`.

### 2.3 Grading: lightest method that works

| Output shape | Scorer |
|---|---|
| Deterministic / format-checkable | `includes()`, `match()`, `pattern()` |
| Short factual | `f1()`, `model_graded_fact()` |
| Open-ended behavioral | `model_graded_qa()` with an explicit rubric in the case `target` |

Rubrics state what a compliant answer must and must not contain, in the case
record, so grading is inspectable.

### 2.4 Non-determinism

Every case is run **N ≥ 5 times**. Results are reported as a **per-clause pass
rate with standard error**, never a single pass/fail. A pass rate is a
measurement, not a guarantee.

### 2.5 Judge-reliability check

For every rubric graded by an LLM judge:
1. Hand-grade a random sample of ≥ 20% of that rubric's case-runs.
2. Report judge-vs-human agreement: raw agreement % and Cohen's κ.
3. If κ is below 0.6 (substantial agreement), treat the **rubric** as the
   defect; revise it and re-check. Do not publish a number from an unreliable
   rubric.

This is the check that turns "I asked a model to grade it" into a defensible
measurement, and it is the harness's answer to NIST MEASURE 2.13 (evaluate the
effectiveness of the TEVV metrics themselves).

## 3. Coverage

Three coverage figures, reported together, none of them sufficient alone:

- **Clause coverage** = testable clauses with ≥ 1 case ÷ total testable clauses.
- **Tier coverage** = for each clause, which of T1 / T2 / T3 are exercised.
- **Excluded clauses** = the explicit list of clauses not covered, each with a
  reason (unfalsifiable, requires real user data, requires multi-session
  context, out of harness scope).

**Coverage is not correctness.** Exercising every clause once says nothing
about:
- interactions between clauses,
- behaviors the spec never addresses,
- rare inputs outside the authored cases,
- distribution shift between the case set and real traffic.

## 4. Mapping to NIST AI RMF (MEASURE function)

| MEASURE item | Where this harness addresses it |
|---|---|
| **1.1** methods/metrics selected by risk; unmeasurable risks documented | clause table `testable?` column + §3 excluded clauses |
| **1.3** independent assessors involved | cases authored by someone who did not write the system under test |
| **2.1** test sets, metrics, TEVV tooling documented | this document + `specs/`, `evals/`, `data/` |
| **2.3** performance measured for deployment-like conditions | the T2 tier |
| **2.5** validity/reliability demonstrated; generalizability limits documented | §2.4 repeated runs + §3 "coverage is not correctness" |
| **2.13** effectiveness of the TEVV metrics evaluated | §2.5 judge-reliability check |
| **3.2** approaches for risks hard to measure with current techniques | excluded-clause reasons; tier design |

Track C of the Fall 2026 plan (a full GOVERN / MAP / MEASURE / MANAGE pass on
NIST AI RMF) shares this section.

## 5. Relationship to DO-178C / DO-330 practice

| Conventional software V&V | This harness |
|---|---|
| Requirements (HLR / LLR) | normative clauses extracted from the spec |
| Requirement-to-test traceability (RTM) | `clause_id` on every case; the coverage table |
| Requirement coverage | clause coverage (§3) |
| Structural coverage (statement / MC/DC) | *no analogue*: model internals are not instrumented; tier coverage is a weak substitute, and this limitation is stated, not papered over |
| Robustness / range testing | the T3 tier |
| Tool qualification data package | this document + the reproducible harness + result exports |

The honest gap is structural coverage: there is no MC/DC for a language model.
The harness does not pretend otherwise.

## 6. Limitations

- **Non-determinism.** Pass rates are point-in-time measurements against a
  specific model version; they are not guarantees and will drift.
- **Judge bias.** LLM graders share failure modes with the systems they grade.
  The reliability check (§2.5) bounds this; it does not remove it.
- **Spec ambiguity.** Natural-language specs have gaps and contradictions.
  Clause extraction is subjective and is documented as such.
- **Author-imagination ceiling.** A small, single-author case set reflects one
  person's model of what could go wrong. It is not a substitute for red-teaming
  or field data.
- **Conformance ≠ safety.** A system can pass every clause and still be unsafe
  in a situation the spec did not anticipate.
- **Single-turn bias.** Most cases are single-turn; multi-session and
  long-context behavior is under-covered.

## 7. Reproducibility

Each result export records: model id and version, `inspect-ai` version, date,
N (runs per case), the full case set, every rubric, and the raw `inspect view`
log. Anyone can re-run `inspect eval` and compare.
