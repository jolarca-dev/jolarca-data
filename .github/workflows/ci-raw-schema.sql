-- ci-raw-schema.sql — synthetic source stand-in for dbt-ci ONLY.
-- Mirrors ingestion/contracts/* field allow-lists so staging models can
-- build in CI without ever touching the real read replica. Values are
-- synthetic literals; keep them that way (PII scan runs on this file).

create schema if not exists raw;

create table raw.orders (
  id            bigint primary key,
  buyer_id      bigint not null,
  seller_id     bigint not null,
  status        text   not null,
  amount_cents  integer not null,
  currency      char(3) not null,
  category_code text   not null,
  country_code  char(2) not null,
  vat_rate_pct  numeric(5, 2) not null,
  created_at    timestamptz not null
);

create table raw.products (
  id            bigint primary key,
  seller_id     bigint not null,
  category_code text   not null,
  title         text   not null,
  price_cents   integer not null,
  currency      char(3) not null,
  status        text   not null,
  created_at    timestamptz not null
);

create table raw.users (
  id                 bigint primary key,
  role               text   not null,
  country_code       char(2) not null,
  consent_marketing  boolean not null,
  created_at         timestamptz not null
);

insert into raw.orders values
  (1, 101, 201, 'paid',      12100, 'EUR', 'vestments',   'LT', 21.00, '2026-08-01 10:00:00+00'),
  (2, 102, 201, 'paid',       5900, 'EUR', 'icons',       'LV', 21.00, '2026-08-02 11:00:00+00'),
  (3, 103, 202, 'shipped',    3400, 'EUR', 'books',       'EE', 22.00, '2026-08-03 12:00:00+00'),
  (4, 104, 202, 'refunded',   9900, 'EUR', 'funeral',     'LT', 21.00, '2026-08-04 13:00:00+00'),
  (5, 105, 203, 'paid',      25000, 'EUR', 'services',    'LT', 21.00, '2026-08-05 14:00:00+00');

insert into raw.products values
  (1001, 201, 'vestments', 'Synthetic chasuble',      12100, 'EUR', 'active',   '2026-07-01 09:00:00+00'),
  (1002, 201, 'icons',     'Synthetic icon panel',     5900, 'EUR', 'active',   '2026-07-02 09:00:00+00'),
  (1003, 202, 'books',     'Synthetic hymnal',         3400, 'EUR', 'active',   '2026-07-03 09:00:00+00'),
  (1004, 203, 'services',  'Synthetic ceremony svc',  25000, 'EUR', 'inactive', '2026-07-04 09:00:00+00');

insert into raw.users values
  (101, 'buyer',  'LT', true,  '2026-01-10 08:00:00+00'),
  (102, 'buyer',  'LV', false, '2026-02-11 08:00:00+00'),
  (201, 'seller', 'LT', true,  '2026-03-12 08:00:00+00'),
  (202, 'seller', 'EE', false, '2026-04-13 08:00:00+00'),
  (203, 'seller', 'LT', true,  '2026-05-14 08:00:00+00');
