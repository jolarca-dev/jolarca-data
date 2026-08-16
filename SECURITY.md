# Security Policy — jol-m-data

## Severity doctrine

**Any incident involving personal data in this repository or in the
warehouse it manages is the highest severity class.** The entire design
of this repository (pseudonymize-at-ingestion, field allow-lists,
aggregate-only compliance marts) exists so that a warehouse compromise
cannot become a personal-data breach. Finding cleartext PII downstream
of ingestion means that boundary failed — treat it as such.

Order of notification:

1. DPO (`jol-m-compliance`) — immediately; GDPR 72h assessment clock is
   the DPO's, and the PII runbook is DPO-controlled.
2. Data platform owner (repo owner) — immediately, in parallel.
3. Security function / incident commander (`jol-m-infrastructure`
   runbooks).
4. General counsel (`jol-m-legal`) if regulatory notification becomes
   likely.

## Reporting

Report vulnerabilities and data incidents privately. **Never** open a
public issue, paste credentials into chat, or describe affected records
in a tracker.

- Security function contact: per `jol-m-infrastructure/SECURITY.md`.
- DPO contact: per `jol-m-compliance` (RoPA point of contact).
- Use the `pii_incident` issue template only for **non-sensitive**
  metadata (where, when, which pipeline) — never the data itself.

## Scope-specific risks

| Risk | Control |
|------|---------|
| Warehouse credentials committed | gitleaks pre-commit + CI; `.env*` gitignored; profiles.yml.example documents env vars only |
| Cleartext PII lands in warehouse | pseudonymizer at ingestion boundary (unit-tested); field allow-list contracts; scheduled `pii-scan.yml` |
| Cleartext PII committed to seed/fixtures | fixtures are faker-seeded synthetic; pre-commit PII pattern scan; `validate-seed.py` |
| Re-identification via join of marts | compliance marts are aggregates only; `verify-anonymization.py` adversarial sampling |
| Retention bypassed | retention jobs driven by `governance/retention-map.md`; legal holds suspend, not delete |
| SAQ-A boundary erosion | Stripe extract takes charge/payout metadata only — never PAN or full card data |

## Do not

- Do not connect extraction jobs to production with write privileges —
  read-replica, read-only role, least privilege (ADR-0002).
- Do not copy production dumps, `*.dump`, or CSV extracts into this
  repository — they are gitignored for a reason.
- Do not "fix" a PII finding by quietly deleting history; follow
  [docs/runbooks/pii-detected-in-warehouse.md](docs/runbooks/pii-detected-in-warehouse.md)
  so the DPO can assess notification duty.
