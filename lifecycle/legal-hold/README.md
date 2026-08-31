# Legal holds — counsel-controlled suspension of retention

A hold suspends retention jobs for specific entities (hashed keys —
never cleartext identities in this file). **Holds suspend; they never
delete and never reveal.** Setting or releasing a hold is a
counsel/DPO-controlled action and is logged.

## Operating rules

1. Entities are referenced by pseudonymous key only; the mapping to a
   subject exists inside `jolarca`/`jolarca-compliance`.
2. Every hold carries: reason class (litigation, regulatory inquiry,
   audit), requested by (role, not name in this file), start date.
3. Retention jobs MUST consult `holds.yml` and skip held entities,
   reporting them as skipped in the run proof.
4. Quarterly review with counsel; stale holds escalate.

## holds.yml format

```yaml
holds: []
# - entity_key: <32-char hash>
#   reason_class: litigation
#   requested_by: general-counsel
#   started_at: "YYYY-MM-DD"
```
