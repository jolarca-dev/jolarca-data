# Geo reference data — LT/LV/EE

Reference sets for checkout/delivery flows and analytics geo
dimensions. Content here is a **representative subset**; the full
administrative lists are loaded from official open-data sources by
`jol-m-marketplace` — this seed provides the stable code scheme and
demo coverage.

| File | Content |
|------|---------|
| `municipalities.yml` | Municipalities (LT savivaldybės, LV novadi, EE omavalitsused) + parish boundary refs |
| `lockers.yml` | Parcel-locker location refs (Omniva/DPD) — synthetic location codes |

Rules:

- Codes are stable identifiers; name changes are PATCH, code changes are
  MAJOR for consumers.
- Locker coordinates in committed files are synthetic/approximate — the
  authoritative live locations come from carrier APIs at runtime.
