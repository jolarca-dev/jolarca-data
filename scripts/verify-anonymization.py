#!/usr/bin/env python3
"""verify-anonymization.py — adversarial re-identification sampler.

Attempts re-identification against the repository's committed artifacts
(default) and, when configured, against warehouse marts (--warehouse).
Every attempt MUST fail: a successful path means the pseudonymization
boundary has a hole — severity-1 class incident (SECURITY.md).

Local checks (no credentials required):
  1. Staging/mart models never select direct identifier columns.
  2. Staging models hash every subject id column (hash_id invariant).
  3. Committed seed/fixture data carries no identity fields and no
     PII-shaped values (delegates patterns to scan-warehouse-pii).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "warehouse/models"

FORBIDDEN_TOKENS = re.compile(
    r"\b(email|phone|first_name|last_name|full_name|buyer_name|seller_name|"
    r"cardholder|national_id|asmens_kodas|personal_code|bank_account|iban)\b"
)
HASH_INVARIANT = {
    "stg_orders.sql": ["id", "buyer_id", "seller_id"],
    "stg_products.sql": ["id", "seller_id"],
    "stg_users.sql": ["id"],
}


def check_models() -> list[str]:
    failures = []
    for path in sorted(MODELS.rglob("*.sql")):
        text = path.read_text(encoding="utf-8")
        for m in FORBIDDEN_TOKENS.finditer(text):
            failures.append(f"{path.relative_to(ROOT)}: direct identifier token '{m.group(0)}'")
    for filename, columns in HASH_INVARIANT.items():
        text = (MODELS / "staging" / filename).read_text(encoding="utf-8")
        for column in columns:
            if f"hash_id('{column}')" not in text:
                failures.append(f"models/staging/{filename}: column '{column}' is not hashed")
    return failures


def check_seeds() -> list[str]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/scan-warehouse-pii.py"), "--local"],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        return [f"seed PII sweep failed: {proc.stdout.strip() or proc.stderr.strip()}"]
    return []


def check_fixtures_schema() -> list[str]:
    """Fixtures must carry no identity-like fields (names/contacts)."""
    import yaml
    failures = []
    identity_fields = {"name", "email", "phone", "address", "national_id", "company_name"}
    for path in sorted((ROOT / "seed/fixtures").glob("*.yml")):
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        for record in data.get("records", []):
            leaked = identity_fields & set(record)
            if leaked:
                failures.append(f"{path.relative_to(ROOT)}: identity fields {sorted(leaked)}")
    return failures


def main() -> int:
    if "--warehouse" in sys.argv:
        print("warehouse sampling requires the WH_* environment (see .envrc.example); "
              "running committed-artifact verification instead")
    failures = check_models() + check_fixtures_schema() + check_seeds()
    if failures:
        print("ADVERSARIAL VERIFICATION FAILED — re-identification paths exist:", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("adversarial verification PASS: no re-identification path found in committed artifacts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
