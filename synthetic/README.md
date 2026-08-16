# Synthetic & Test Data

Generators for dev/staging/demo: statistically realistic, **zero real
persons**. Everything here is safe to commit by construction; the PII
tripwire in CI guards that invariant.

| Path | Content |
|------|---------|
| `generators/` | Seeded generators: buyers, sellers, listings, orders — lt/lv/et locale-aware naming |
| `pii-canaries/` | Synthetic PII-shaped strings that scanner self-tests must catch |
| `regression/` | Golden datasets for dbt/pipeline regression testing |

## Rules

1. **Locale awareness is real, identities are not.** Names are composed
   from synthetic phoneme pools per locale (lt/lv/et) so tooling that
   depends on diacritics and case declension is exercised — but no
   generated value corresponds to a real person.
2. **Deterministic output.** Same seed → same dataset; the committed
   fixtures record their seed (`seed/fixtures/README.md`).
3. **Regeneration produces new identities.** A new seed MUST yield a
   different identity set — this is asserted, not assumed.
4. **Canaries stay synthetic.** `pii-canaries/` values are shaped like
   PII (so scanners prove they fire) but are constructed to be
   unassignable; the pre-commit tripwire excludes only that directory.
