# QODER.md

Behavioral guidelines to reduce common LLM coding mistakes when using Qoder in PyCharm. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.
- Prefer PyCharm's built-in refactoring tools (Rename, Extract, Move, etc.) over manual text manipulation when the IDE can do it safely.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions happen before implementation rather than after mistakes.

---

## Project-Specific Guidelines — jol-m-data

This repository governs pseudonymous analytics over marketplace data;
every merge either changes the governance record or transforms data that
was personal. The full rules live in `CONTRIBUTING.md`; these constrain
AI-assisted changes:

### Personal data boundaries

- Never generate, fetch, or commit personal data — real or plausibly
  real. Fixtures come from `synthetic/generators/` and are faker-seeded.
- Never re-introduce identifiers into warehouse models: staging hashes
  IDs and drops names/emails; any model that joins them back is a
  critical defect.
- Compliance marts stay aggregates-only; never emit per-subject rows.

### Pseudonymization & retention

- Changes to `ingestion/pipelines/pseudonymizer/` or
  `lifecycle/` are critical-risk: require DPO review and
  `make anonymize-verify` evidence before merge.
- Retention jobs execute the schedule defined in
  `governance/retention-map.md`; policy text lives in `jol-m-compliance`
  — do not duplicate or reword policy here.
- Legal holds suspend retention; they never delete.

### Governance gates

- New datasets must land with catalog entry + ownership row +
  classification + retention class; `scripts/catalog-lint.py` enforces.
- `make check` (seed schema + catalog lint + PII tripwire) must pass
  before proposing a change as complete.
- Never suggest bypassing pre-commit (`--no-verify`) or loosening the
  PII scan patterns to make a commit pass.

### Secrets & access

- No warehouse credentials, connection strings, or API keys in any
  file; `profiles.yml.example`/`.envrc.example` document env vars only.
- Extraction connects to the read replica with a read-only role — never
  propose production credentials for analytics (ADR-0002).
