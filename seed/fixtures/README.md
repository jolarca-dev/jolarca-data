# Fixtures — demo sellers/products/orders

100% synthetic (faker-seeded, PII-free by construction). Used by
`jol-m-marketplace` demo/staging environments and by dbt-ci as the
synthetic raw schema.

## Generation procedure

1. Run the generator with an explicit seed:

   ```bash
   python3 synthetic/generators/generate_fixtures.py --seed <N> --out seed/fixtures
   ```

2. Regeneration with a **different** seed MUST produce new synthetic
   identities — this is a fixture invariant, not a side effect.
3. Commit the output together with the seed value recorded below.

| File | Records | Generated with |
|------|---------|----------------|
| `sellers.yml` | 5 synthetic sellers | seed=20260801 (scaffold baseline) |
| `products.yml` | 8 synthetic products | seed=20260801 |
| `orders.yml` | 10 synthetic orders | seed=20260801 |

Rules:

- Identities use the `SYN-` key scheme and `@example.test` contacts —
  the PII tripwire in CI relies on both. Never replace them with real
  values "for realism".
- Amounts are EUR cents; VAT rates reference `seed/tax/vat-rates.yml`.
- Schema validation: `make seed-validate` (schemas in `../validators/`).
