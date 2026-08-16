# DPIA template — GDPR Art. 35 (template-inherited, data-platform copy)

**When required:** any change introducing or altering processing of personal
data in the warehouse or pipelines (new source, new field on an allow-list,
new mart over pseudonymous keys, new retention class, new ML dataset). Attach
the completed DPIA to the change request BEFORE implementation.

---

## 1. Processing description

- Purpose of processing (RoPA reference in `jol-m-compliance`):
- Categories of data subjects (buyers/sellers/visitors):
- Categories of personal data (flag special categories Art. 9):
- Data flows (source → pseudonymizer → landing → models → consumers):
- Legal basis (Art. 6):
- Retention period & deletion mechanism (retention class + job):

## 2. Necessity & proportionality

- Why is each field on the ingestion allow-list necessary?
- Minimization measures (hash at boundary, generalization, aggregation):
- Alternatives considered and rejected:

## 3. Risk assessment (to rights & freedoms)

| Risk scenario | Likelihood | Impact | Mitigation |
|---------------|------------|--------|------------|
| re-identification via mart join | | | aggregates-only rule, adversarial verification |
| cleartext PII landing | | | fail-closed pseudonymizer, pii-scan |
| retention bypass | | | legal-hold aware jobs, DPO release |

## 4. Technical & organizational measures

- Encryption at rest / in transit (keys per `jol-m-infrastructure` custody):
- Access control (warehouse roles, review cadence):
- Residency: EU-only (no cross-region replication):
- Breach detection & notification path (72h, Art. 33 — DPO owns the clock):

## 5. Processor/sub-processor check

- New third parties introduced (embedding providers, label platforms)?
  List, DPA status, location:

## 6. Sign-off

- DPO:
- Data platform owner:
- Date:
