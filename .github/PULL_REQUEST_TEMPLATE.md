## Change summary

<!-- One paragraph: what changes, why, link to the intake issue. -->

## Dataset checklist (mandatory — CONTRIBUTING.md)

- Data classification: [ ] PUBLIC  [ ] INTERNAL  [ ] CONFIDENTIAL  [ ] RESTRICTED
- RoPA purpose reference: <!-- jol-m-compliance RoPA entry id, or "n/a (no personal data)" -->
- Retention class: <!-- per governance/retention-map.md, or "n/a" -->
- Catalog entry + ownership row added for new datasets: [ ] yes / n/a
- No personal data committed (fixtures are synthetic): [ ] confirmed
- No warehouse credentials or connection strings introduced: [ ] confirmed

## Warehouse impact

- Models added/changed: <!-- names, or "none" -->
- Staging still pseudonymous (hashed IDs, no names/emails): [ ] confirmed / n/a
- dbt tests cover the change (unique/not_null/relationships + custom): [ ] yes / n/a
- Backfill required: [ ] yes / no — <!-- window & owner -->

## Seed impact

- Taxonomy change class: [ ] MAJOR (breaking for consumers)  [ ] MINOR  [ ] PATCH  [ ] n/a
- Translations complete for lt/lv/et/en: [ ] yes / n/a
- Fixture regeneration documented (new identities on reseed): [ ] yes / n/a

## Compliance notes

<!-- GDPR / VAT-OSS / DSA analytics relevance, DPO consulted (yes/no),
or "none". -->
