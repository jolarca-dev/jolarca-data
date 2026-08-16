# Generators — seeded synthetic data

Deterministic generators for fixtures used by demo/staging environments
and dbt-ci. Uses `faker` when available (locale-aware lt_LT/lv_LV/et_EE
name pools); falls back to built-in synthetic pools so `make check`
works without optional dependencies.

```bash
python3 generate_fixtures.py --seed 20260801 --out ../../seed/fixtures
```

Invariants enforced by the generator:

- Keys follow the `SYN-` scheme (`SYN-SLR-…`, `SYN-PRD-…`, …).
- Contacts use `@example.test` only.
- Category codes come from `seed/taxonomy/categories.yml`.
- VAT rates come from `seed/tax/vat-rates.yml` (country + vat_class).
- Currency is always EUR.

`test_generate_fixtures.py` asserts determinism (same seed → same
output) and regeneration divergence (new seed → new identities).
