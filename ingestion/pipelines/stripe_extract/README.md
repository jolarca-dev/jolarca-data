# stripe_extract — charges/payouts metadata only

Extracts settlement metadata from Stripe with a **restricted key**:

- Allowed: charge ids, amounts, currencies, payout ids/periods, fee
  metadata, status timestamps.
- Prohibited: PAN/full card data, cardholder names, full bank account
  numbers, dispute evidence content. The SAQ-A boundary holds in
  analytics too.

Key custody follows `jolarca-infrastructure` token rotation discipline;
the key lives in Vaultwarden and is referenced via `EXTRACT_STRIPE_KEY`
(see `.envrc.example`) — never committed.

Output goes through `../pseudonymizer/` (account references are hashed)
before landing; see `../contracts/stripe.yml` for the field allow-list.
