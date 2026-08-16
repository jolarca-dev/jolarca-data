# Lifecycle — retention & anonymization machinery

**This code executes the retention schedule; the policy text lives in
`jol-m-compliance`.** Nothing here re-states policy — every job points
at the retention class it implements (`governance/retention-map.md`).

| Path | Content |
|------|---------|
| `anonymization/` | Erasure-support jobs: verify product-DB anonymization propagated to the warehouse |
| `retention-jobs/` | Scheduled purge/anonymize per retention-map (warehouse only; production tables are owned by jol-m-marketplace) |
| `legal-hold/` | Hold flags that suspend retention jobs for specific entities (counsel-controlled) |
| `verification/` | Post-run proofs: sampled re-identification attempts must fail (adversarial test) |

## Hard rules

1. **Scope: warehouse only.** Production erasure happens in
   `jol-m-marketplace`; this machinery verifies propagation and purges
   analytics copies.
2. **Legal holds suspend, never delete.** A hold pauses the applicable
   retention job for the held entities; release is counsel/DPO
   controlled and logged.
3. **Every run leaves a proof.** Execution + verification results are
   evidence (statutory retention per `governance/retention-map.md`).
4. **Adversarial verification is mandatory** after anonymization runs:
   `make anonymize-verify` (scripts/verify-anonymization.py) — sampled
   re-identification attempts must fail.
