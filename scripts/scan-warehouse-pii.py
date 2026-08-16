#!/usr/bin/env python3
"""scan-warehouse-pii.py — pattern scan for PII-shaped values.

Modes:
  --local       scan committed data files (seed, governance, ml, seeds)
  --warehouse   sample the staging warehouse (needs WH_* env + psycopg2)
  --self-test   prove the scanner fires on synthetic/pii-canaries/

Findings are reported by LOCATION ONLY — offending values are never
printed (docs/runbooks/pii-detected-in-warehouse.md). Requires: pyyaml.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("pyyaml is required: pip install -e .")

ROOT = Path(__file__).resolve().parents[1]
CANARIES = ROOT / "synthetic/pii-canaries/canaries.yml"
SCAN_DIRS = ["seed", "governance", "ml", "warehouse/seeds", "synthetic/generators", "synthetic/regression"]
SCAN_SUFFIXES = {".yml", ".yaml", ".csv", ".md", ".json"}

PATTERNS = {
    "baltic-national-id": re.compile(r"\b[0-9]{11}\b"),
    "lv-personas-kods": re.compile(r"\b[0-9]{6}-[0-9]{5}\b"),
    "baltic-iban": re.compile(r"\b(LT|LV|EE)[0-9]{2}([ ]?[0-9]{4}){3,}\b"),
    "baltic-phone": re.compile(r"\+37[012]([ -]?[0-9]){8,11}\b"),
}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z][A-Za-z0-9.-]*\.[A-Za-z]{2,}")
ALLOWED_EMAIL = re.compile(r"@example\.(test|com|org|net)$", re.IGNORECASE)
NAME_ADDRESS = re.compile(r"\b[A-Z][a-z]+ [A-Z][a-z]+,\s*.*\b(?:g\.|str\.|street|ave\.|road)")


def scan_text(text: str, strict_emails: bool = False) -> list[str]:
    """Return kinds of PII-shaped patterns present in the text."""
    hits = [kind for kind, rx in PATTERNS.items() if rx.search(text)]
    for m in EMAIL.finditer(text):
        if strict_emails or not ALLOWED_EMAIL.search(m.group(0)):
            hits.append("email")
            break
    if NAME_ADDRESS.search(text):
        hits.append("name-with-address")
    return hits


def scan_local() -> int:
    findings = 0
    for rel in SCAN_DIRS:
        base = ROOT / rel
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if path.is_file() and path.suffix in SCAN_SUFFIXES:
                hits = scan_text(path.read_text(encoding="utf-8", errors="replace"))
                if hits:
                    print(f"PII-shaped values: {path.relative_to(ROOT)} ({', '.join(sorted(set(hits)))})")
                    findings += 1
    return findings


def scan_warehouse() -> int:
    try:
        import psycopg2
    except ImportError:
        sys.exit("psycopg2 required for --warehouse: pip install psycopg2-binary")
    if not os.environ.get("WH_HOST"):
        sys.exit("WH_* environment not configured (see .envrc.example) — nothing to scan")
    conn = psycopg2.connect(
        host=os.environ["WH_HOST"], port=int(os.environ.get("WH_PORT", "5432")),
        dbname=os.environ.get("WH_DB"), user=os.environ.get("WH_USER"),
        password=os.environ.get("WH_PASSWORD"),
        connect_timeout=10,
    )
    findings = 0
    try:
        with conn.cursor() as cur:
            cur.execute(
                "select table_schema, table_name, column_name "
                "from information_schema.columns "
                "where table_schema not in ('pg_catalog','information_schema') "
                "  and data_type in ('text','character varying','character')"
            )
            columns = cur.fetchall()
            for schema, table, column in columns:
                cur.execute(
                    f'select "{column}" from "{schema}"."{table}" '  # noqa: S608 - warehouse metadata
                    f'where "{column}" is not null limit 500'
                )
                sampled = [str(row[0]) for row in cur.fetchall()]
                kinds = {k for value in sampled for k in scan_text(value)}
                if kinds:
                    print(f"PII-shaped values: warehouse {schema}.{table}.{column} ({len(sampled)} sampled)")
                    findings += 1
    finally:
        conn.close()
    return findings


def self_test() -> int:
    with open(CANARIES, encoding="utf-8") as fh:
        canaries = yaml.safe_load(fh)["canaries"]
    failures = 0
    for canary in canaries:
        # Self-test uses strict email detection (canary email is reserved-domain by construction).
        hits = scan_text(canary["value"], strict_emails=True)
        status = "DETECTED" if hits else "MISSED"
        print(f"{status}: {canary['kind']} -> {', '.join(sorted(set(hits))) or '-'}")
        if not hits:
            failures += 1
    if failures:
        print(f"self-test FAILED: {failures} canary(ies) missed — scanner is blind", file=sys.stderr)
        return 1
    print("self-test OK: all canaries detected")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--local", action="store_true")
    group.add_argument("--warehouse", action="store_true")
    group.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    findings = scan_local() if args.local else scan_warehouse()
    if findings:
        print(f"FAIL: {findings} location(s) with PII-shaped values — "
              "follow docs/runbooks/pii-detected-in-warehouse.md and notify the DPO", file=sys.stderr)
        return 1
    print("pii scan OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
