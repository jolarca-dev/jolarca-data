# Embeddings — product-description embedding builds

Build jobs producing product-description vectors for the semantic
search service (`ai_service_app`), exported in **pgvector format**.

## Build contract

- Input: `dim_products` (active listings) — pseudonymous warehouse
  mart; never production text with seller identity fields.
- Output: `(product_key, embedding vector, model_ref, built_at)` —
  product_key is the pseudonymous hash, so erasure propagation can
  drop vectors without ever knowing the listing's owner.
- Provenance: every build records model + version + seed data date
  (catalog: ml_embeddings_products).

## Lifecycle

1. Rebuild on taxonomy MAJOR changes (description semantics shift).
2. Incremental nightly for new/changed listings (when the warehouse
   environment is live).
3. On erasure events: drop vectors for the erased subject's listings
   — verified by `lifecycle/anonymization/`.
