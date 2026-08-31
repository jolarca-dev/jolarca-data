# ML / Embedding Datasets — feeds ai_service_app semantic search

Dataset governance for AI: every dataset here carries provenance,
license basis, and a PII-free certification before it may be consumed.

| Path | Content |
|------|---------|
| `embeddings/` | Product-description embedding build jobs (pgvector export format) |
| `evaluation/` | Search relevance eval sets (synthetic + human-labeled, anonymized) |
| `translation-memory/` | Domain glossary pairs lt/lv/et/en (legal terms sync with jolarca-legal) |

## Governance rules (apply to every artifact under ml/)

1. **Provenance is recorded.** Source dataset, build date, model +
   version for every embedding build; catalog entry per dataset
   (`governance/data-catalog.md`: ml_embeddings_products,
   ml_translation_memory).
2. **License basis declared.** Product descriptions are licensed by
   sellers under the seller agreement; eval labels by contributors
   under the CLA (`jolarca-legal/intellectual-property/copyright/`).
   No scraped external corpora.
3. **PII-free certification.** Builds run on pseudonymous warehouse
   marts only; the pii-scan gate applies to committed eval data.
   Embeddings of erased listings are dropped on erasure propagation
   (`lifecycle/anonymization/`).
4. **No personal data in prompts or eval sets.** Human-labeled sets are
   anonymized before commit.
