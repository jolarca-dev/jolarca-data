# Verification — post-run proofs & adversarial testing

Retention/anonymization runs must leave evidence that stands up in
audit. Proofs are statutory-retention records
(`governance/retention-map.md`).

## Proof contents (per run)

- Run id, job, retention class, dataset scope, timestamp.
- Row counts before/after; held entities skipped.
- Verification result: PASS/FAIL + sampled evidence (no subject data —
  counts and key prefixes only).

## Adversarial re-identification sampling

`make anonymize-verify` (scripts/verify-anonymization.py) attempts
re-identification on samples:

1. Pick sampled pseudonymous keys from marts.
2. Attempt joins across marts and against committed seed/geo/tax
   references to reconstruct an identity.
3. **Every attempt must fail.** Any successful path is a severity-1
   class incident (SECURITY.md) — it means the pseudonymization
   boundary has a hole.

Proofs are written to run logs here (gitignored working files; durable
copies go to the compliance evidence custody in `jolarca-compliance`).
