-- extract-role.sql — least-privilege extract role for the READ REPLICA.
-- Executed by jol-m-infrastructure (change management applies); kept
-- here as the source of truth for what analytics is granted.

create role jol_extract login;

-- Replica only. No superuser, no create, no production access.
grant connect on database marketplace to jol_extract;
grant usage on schema public to jol_extract;

-- Table-scoped reads matching ingestion/contracts/postgres.yml
grant select on table public.orders to jol_extract;
grant select on table public.products to jol_extract;
grant select on table public.users to jol_extract;

-- Explicitly nothing else: no grants on payments, payouts, sessions,
-- consent logs, or identity documents.
