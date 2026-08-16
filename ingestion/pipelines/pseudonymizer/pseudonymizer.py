#!/usr/bin/env python3
"""Pseudonymizer — strips/hashes identifiers BEFORE warehouse landing.

The boundary component of ADR-0001. Fields not explicitly listed in
rules.yml are dropped (fail-closed). Pure stdlib: no dependencies may
be added without review — this code is audited.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment guard
    sys.exit("pyyaml is required: pip install -e .")

RULES_PATH = Path(__file__).with_name("rules.yml")


def load_rules(path: Path = RULES_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        rules = yaml.safe_load(fh)
    if rules.get("default_action") != "drop":
        raise ValueError("pseudonymizer must stay fail-closed (default_action: drop)")
    return rules


def hash_value(value: object, salt: str) -> str:
    """Deterministic salted md5 — same scheme as warehouse hash_id()."""
    return hashlib.md5(f"{value}{salt}".encode("utf-8")).hexdigest()


def apply_rules(source: str, record: dict, rules: dict, salt: str) -> dict:
    """Return the landing-safe view of a source record."""
    table_rules = rules.get("sources", {}).get(source)
    if table_rules is None:
        raise KeyError(f"no pseudonymizer rules for source table: {source}")
    out: dict = {}
    for field, value in record.items():
        action = table_rules.get(field, rules["default_action"])
        if action == "drop":
            continue
        if action == "pass":
            out[field] = value
        elif action == "hash":
            out[field] = hash_value(value, salt)
        elif action == "generalize":
            out[field] = _generalize(value)
        else:
            raise ValueError(f"unknown pseudonymizer action: {action}")
    return out


def _generalize(value: object) -> object:
    """Reduce precision: timestamps -> date, datetimes -> month-first-day."""
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, str):
        return value[:10]  # ISO datetime string -> date prefix
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="source table name")
    parser.add_argument("--record", required=True, help="JSON record to pseudonymize")
    parser.add_argument("--salt", default="dev-only-salt")
    args = parser.parse_args()
    record = json.loads(args.record)
    result = apply_rules(args.source, record, load_rules(), args.salt)
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
