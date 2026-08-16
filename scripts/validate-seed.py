#!/usr/bin/env python3
"""validate-seed.py — JSON Schema validation for every seed/taxonomy file.

CI gate (ci.yml) and pre-commit hook. Adding a new seed file requires
registering it here with a schema. Requires: pyyaml, jsonschema.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft7Validator
except ImportError:  # pragma: no cover
    sys.exit("pyyaml + jsonschema required: pip install -e .")

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "seed"
VALIDATORS = SEED / "validators"

FIXTURE_DEFS = {"sellers": "seller", "products": "product", "orders": "order"}


def load(path: Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def validator_for(schema_file: Path) -> Draft7Validator:
    with open(schema_file, encoding="utf-8") as fh:
        return Draft7Validator(json.load(fh))


def check(data: dict, validator: Draft7Validator, errors: list, label: str) -> None:
    for err in sorted(validator.iter_errors(data), key=str):
        errors.append(f"{label}: {err.message} at {list(err.absolute_path)}")


def main() -> int:
    errors: list[str] = []

    # taxonomy
    categories = load(SEED / "taxonomy/categories.yml")
    check(categories, validator_for(VALIDATORS / "categories.schema.json"), errors, "categories.yml")
    attributes = load(SEED / "taxonomy/attributes.yml")
    check(attributes, validator_for(VALIDATORS / "attributes.schema.json"), errors, "attributes.yml")

    codes = {c["code"] for c in categories.get("categories", [])}
    if set(attributes.get("attributes", {})) != codes:
        errors.append("attributes.yml: category keys must match categories.yml codes")

    # translations — schema + completeness against category codes
    trans_validator = validator_for(VALIDATORS / "translations.schema.json")
    for path in sorted((SEED / "taxonomy/translations").glob("*.yml")):
        data = load(path)
        check(data, trans_validator, errors, path.name)
        missing = codes - set(data.get("names", {}))
        if missing:
            errors.append(f"{path.name}: missing translations for {sorted(missing)}")

    # geo + tax
    geo_validator = validator_for(VALIDATORS / "geo.schema.json")
    for path in sorted((SEED / "geo").glob("*.yml")):
        check(load(path), geo_validator, errors, path.name)
    tax_validator = validator_for(VALIDATORS / "tax.schema.json")
    for path in sorted((SEED / "tax").glob("*.yml")):
        check(load(path), tax_validator, errors, path.name)

    # fixtures — per-file record definition + referential integrity
    with open(VALIDATORS / "fixtures.schema.json", encoding="utf-8") as fh:
        fixtures_schema = json.load(fh)
    fixtures: dict = {}
    for stem, definition in FIXTURE_DEFS.items():
        path = SEED / "fixtures" / f"{stem}.yml"
        data = load(path)
        fixtures[stem] = data.get("records", [])
        record_validator = Draft7Validator(fixtures_schema["definitions"][definition])
        for i, record in enumerate(fixtures[stem]):
            check(record, record_validator, errors, f"fixtures/{stem}.yml[{i}]")

    seller_keys = {s["seller_key"] for s in fixtures["sellers"]}
    product_keys = {p["product_key"] for p in fixtures["products"]}
    for i, product in enumerate(fixtures["products"]):
        if product.get("category_code") not in codes:
            errors.append(f"fixtures/products.yml[{i}]: unknown category_code")
        if product.get("seller_key") not in seller_keys:
            errors.append(f"fixtures/products.yml[{i}]: unknown seller_key")
    for i, order in enumerate(fixtures["orders"]):
        if order.get("seller_key") not in seller_keys:
            errors.append(f"fixtures/orders.yml[{i}]: unknown seller_key")
        if order.get("product_key") not in product_keys:
            errors.append(f"fixtures/orders.yml[{i}]: unknown product_key")

    if errors:
        print("seed validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("seed validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
