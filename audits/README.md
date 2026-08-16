# Audits — jol-m-data

Internal audit records for this repository.

- `internal/` — audit workpapers, findings, and remediation tracking
  for audits scoped to this repository (catalog reconciliation,
  retention execution evidence reviews, scanner effectiveness).
- Cross-repo audit evidence (GDPR records, SOC 2 evidence) is owned by
  `jol-m-compliance`; this directory holds only what was produced by or
  about this repository's controls.

Rules:

1. Audit records are append-only; findings are closed with evidence,
   not deleted.
2. No personal data in audit workpapers — counts, key prefixes, and
   references only.
3. Warehouse rebuild proofs and adversarial verification results land
   here with a pointer to the durable copy in `jol-m-compliance`.
