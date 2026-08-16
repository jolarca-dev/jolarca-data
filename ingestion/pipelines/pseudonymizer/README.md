# pseudonymizer — THE critical component

Strips or hashes identifiers **before** landing. Everything downstream
inherits its guarantees; a defect here is a breach of the whole
warehouse design (ADR-0001).

## Rules (`rules.yml`)

| Action | Meaning |
|--------|---------|
| drop | Field never leaves the source (names, emails, phones, registry codes) |
| hash | Deterministic salted hash (same scheme as warehouse `hash_id`) |
| generalize | Reduce precision (dates → month, geo → municipality) |
| pass | Non-personal field, on the contract allow-list |

## Hard requirements

1. **Unit tests mandatory** (`test_pseudonymizer.py`): drop rules must
   produce absent fields, hash rules must be deterministic and
   irreversible-without-salt, and any new field defaults to DROP
   (fail-closed) until explicitly classified in `rules.yml`.
2. Changes are critical-risk (CONTRIBUTING.md): DPO + data platform
   review, and `make anonymize-verify` evidence after deploy.
3. The salt is an environment secret (HASH_SALT), never in-repo.
