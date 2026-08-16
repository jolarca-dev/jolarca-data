# VAT rate references

Rates per category per country. These are **references for analytics
and seed fixtures** — the charging authority is Stripe Tax at
transaction time (see `seed/fixtures` doctrine). Rates are validated
against Stripe Tax on the review date below; re-validate quarterly and
on any EU VAT directive change.

- Last validated against Stripe Tax: 2026-08-01 (scaffold baseline —
  re-validate before first production use).
- Reduced rate applies to `books` (per national schedules).
- OSS threshold/registration data lives in `jol-m-compliance` tax
  records, not here.
