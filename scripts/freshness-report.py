#!/usr/bin/env python3
"""freshness-report.py — source freshness vs SLA.

Reads freshness SLAs from warehouse/models/staging/_staging.yml, checks
max(loaded_at) per raw table, and reports staleness. --fail-on-stale
exits non-zero when any source exceeds its error_after horizon.
Requires: pyyaml, psycopg2 (warehouse connection via WH_* env).
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("pyyaml is required: pip install -e .")

ROOT = Path(__file__).resolve().parents[1]
STAGING_YML = ROOT / "warehouse/models/staging/_staging.yml"


def load_slas() -> dict:
    with open(STAGING_YML, encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    source = doc["sources"][0]
    loaded_at = source.get("loaded_at_field", "created_at")
    slas = {}
    for table in source.get("tables", []):
        freshness = table.get("freshness", source.get("freshness", {}))
        slas[table["name"]] = {
            "loaded_at": loaded_at,
            "warn": _hours(freshness.get("warn_after")),
            "error": _hours(freshness.get("error_after")),
        }
    return slas


def _hours(spec: dict | None) -> float | None:
    if not spec:
        return None
    mult = {"minute": 1 / 60, "hour": 1, "day": 24}.get(spec.get("period"), 1)
    return spec["count"] * mult


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fail-on-stale", action="store_true",
                        help="exit non-zero when any source exceeds error_after")
    args = parser.parse_args()

    if not os.environ.get("WH_HOST"):
        sys.exit("WH_* environment not configured (see .envrc.example) — nothing to check")
    try:
        import psycopg2
    except ImportError:
        sys.exit("psycopg2 required: pip install psycopg2-binary")

    slas = load_slas()
    conn = psycopg2.connect(
        host=os.environ["WH_HOST"], port=int(os.environ.get("WH_PORT", "5432")),
        dbname=os.environ.get("WH_DB"), user=os.environ.get("WH_USER"),
        password=os.environ.get("WH_PASSWORD"),
        connect_timeout=10,
    )
    now = datetime.now(timezone.utc)
    stale = 0
    try:
        with conn.cursor() as cur:
            for table, sla in sorted(slas.items()):
                cur.execute(f'select max("{sla["loaded_at"]}") from raw."{table}"')  # noqa: S608
                row = cur.fetchone()
                newest = row[0] if row and row[0] else None
                if newest is None:
                    print(f"{table}: EMPTY — no rows landed")
                    stale += 1
                    continue
                age = now - (newest if newest.tzinfo else newest.replace(tzinfo=timezone.utc))
                age_h = age.total_seconds() / 3600
                status = "ok"
                if sla["error"] is not None and age_h > sla["error"]:
                    status, stale = "STALE (error)", stale + 1
                elif sla["warn"] is not None and age_h > sla["warn"]:
                    status = "stale (warn)"
                print(f"{table}: newest {newest.isoformat()} ({age_h:.1f}h old) — {status} "
                      f"[warn {sla['warn']}h / error {sla['error']}h]")
    finally:
        conn.close()

    if args.fail_on_stale and stale:
        print(f"FAIL: {stale} source(s) beyond freshness SLA — "
              "follow docs/runbooks/pipeline-failure.md", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
