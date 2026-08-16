# PII canaries — scanner self-test material

Synthetic PII-shaped strings whose ONLY purpose is proving that
scanners (`scripts/scan-warehouse-pii.py`, the pre-commit tripwire in
self-test mode) actually fire. Constructed to be unassignable:

- National-ID shapes use all-zero check digits (structurally invalid).
- Emails use `@example.test` (RFC 6761 reserved).
- Phone shapes use all-zero subscriber numbers.
- IBANs use the documented test IBAN pattern (reserved, no real bank).

**This directory is excluded from the normal pre-commit tripwire** (it
would always "fail" — that is the point). The scanner's self-test mode
scans ONLY this directory and requires every canary to be detected.
