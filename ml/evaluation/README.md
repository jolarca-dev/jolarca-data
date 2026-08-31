# Evaluation — search relevance eval sets

Relevance judgments for the semantic search stack. Two families:

1. **Synthetic sets** — generated query/listing pairs from
   `seed/fixtures` + taxonomy; deterministic, committed, used in CI.
2. **Human-labeled sets** — relevance grades by reviewers. Labels are
   anonymized before commit: reviewer ids are roles, query logs are
   hashed, and no session identifiers travel with labels.

## Rules

- Eval sets are versioned; a model comparison is only valid within one
  eval-set version.
- Language coverage: lt/lv/et/en queries each — Baltic-locale relevance
  is the product differentiator and must be measured per locale.
- PII gate applies: committed eval files run through the same scanners
  as seed data (`make check`).
- Label governance: contributors covered by the CLA
  (`jolarca-legal/intellectual-property/copyright/`).
