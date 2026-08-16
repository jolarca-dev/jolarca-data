#!/usr/bin/env python3
"""catalog-lint.py — no orphan datasets.

Every dataset must be registered in governance/data-catalog.md AND
governance/ownership-register.csv, owned, classified, and
retention-mapped. Pure stdlib.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOV = ROOT / "governance"

CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"}
RETENTION_CLASSES = {"short-term", "operational", "statutory", "indefinite-reference", "none-synthetic"}
REQUIRED_COLUMNS = ["dataset_id", "business_owner", "technical_steward",
                    "classification", "ropa_purpose", "retention_class"]


def main() -> int:
    errors: list[str] = []

    csv_path = GOV / "ownership-register.csv"
    with open(csv_path, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != REQUIRED_COLUMNS:
            errors.append(f"{csv_path}: header must be {REQUIRED_COLUMNS}")
        rows = list(reader)

    seen: set[str] = set()
    for i, row in enumerate(rows, start=2):
        dataset_id = (row.get("dataset_id") or "").strip()
        if not dataset_id:
            errors.append(f"ownership-register.csv:{i}: empty dataset_id")
            continue
        if dataset_id in seen:
            errors.append(f"ownership-register.csv:{i}: duplicate dataset_id {dataset_id}")
        seen.add(dataset_id)
        for field in ("business_owner", "technical_steward"):
            if not (row.get(field) or "").strip():
                errors.append(f"ownership-register.csv:{i}: {dataset_id} missing {field} (no orphans)")
        if row.get("classification") not in CLASSIFICATIONS:
            errors.append(f"ownership-register.csv:{i}: {dataset_id} classification "
                          f"{row.get('classification')!r} not in {sorted(CLASSIFICATIONS)}")
        if row.get("retention_class") not in RETENTION_CLASSES:
            errors.append(f"ownership-register.csv:{i}: {dataset_id} retention_class "
                          f"{row.get('retention_class')!r} not in {sorted(RETENTION_CLASSES)}")

    # Cross-check against the human-readable catalog
    catalog = (GOV / "data-catalog.md").read_text(encoding="utf-8")
    catalog_ids: set[str] = set()
    for line in catalog.splitlines():
        m = re.match(r"^\|\s*([a-z0-9_*]+)\s*\|", line)
        if m and m.group(1) not in ("dataset_id",):
            catalog_ids.add(m.group(1))
    catalog_ids.discard("seed_*")  # wildcard family row in retention docs only

    for dataset_id in sorted(seen):
        if f"| {dataset_id} |" not in catalog:
            errors.append(f"data-catalog.md: dataset {dataset_id} missing from catalog table")
    for catalog_id in sorted(catalog_ids):
        if catalog_id not in seen and not any(catalog_id.startswith(p) for p in ("seed_",)):
            errors.append(f"data-catalog.md: catalog row {catalog_id} has no register entry")

    if errors:
        print("catalog lint FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"catalog lint OK ({len(seen)} datasets registered, owned, classified, retention-mapped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
