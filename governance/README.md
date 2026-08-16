# Governance — data governance operating model

The catalog is the heart of this repository. If a dataset is not in the
catalog, it does not exist; if it exists but is not in the catalog, CI
blocks it (`scripts/catalog-lint.py` — no orphan datasets).

## Operating model

| Role | Responsibility |
|------|----------------|
| Data platform owner | Catalog accuracy, pipeline ownership, this repo |
| Business owner (per dataset) | Purpose, classification, retention decisions |
| Technical steward (per dataset) | Schema, quality, lineage maintenance |
| DPO (`jol-m-compliance`) | RESTRICTED tier approval, retention classes, RoPA linkage |

## Review cadence

- **Weekly:** quality scorecards (`quality/scorecards/`) reviewed by the
  data platform owner.
- **Monthly:** ownership register reconciliation — every dataset has a
  living owner and steward; orphans escalate.
- **Quarterly:** retention-map review with the DPO; classification
  re-attestation for CONFIDENTIAL/RESTRICTED datasets.
- **On change:** every dataset PR carries classification + RoPA purpose
  + retention class (PR template enforces).

## Files

| File | Role |
|------|------|
| [data-catalog.md](data-catalog.md) | Master index — every dataset with owner, classification, purpose, retention |
| [classification.md](classification.md) | The 4 tiers and per-tier handling rules |
| [ownership-register.csv](ownership-register.csv) | Machine-readable ownership (parsed by catalog-lint) |
| [retention-map.md](retention-map.md) | Dataset → retention class → enforcement mechanism |
| [lineage.md](lineage.md) | Source → ingestion → warehouse → consumer per critical dataset |

Rules for registering a dataset: open a `dataset_request` issue first —
purpose, classification, retention, and ownership are declared before
any pipeline or model code lands.
