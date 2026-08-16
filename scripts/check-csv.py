#!/usr/bin/env python3
"""CSV structural gate for data registers.

Replaces the nonexistent upstream `check-csv` hook: validates that each
register CSV parses, has a non-empty header, and keeps a constant column
count — the invariants the seed validators and catalog lint and audit spot-checks rely on.

Usage: python3 scripts/check-csv.py FILE.csv [FILE.csv ...]
Exit: 0 = all clean, 1 = structural defect.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path


def check_csv(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader, None)
            if header is None:
                return [f"{path}: empty file — registers must carry a header row"]
            if not any(cell.strip() for cell in header):
                errors.append(f"{path}: header row is blank")
            width = len(header)
            for lineno, row in enumerate(reader, start=2):
                if len(row) != width:
                    errors.append(
                        f"{path}:{lineno}: {len(row)} columns, expected {width}"
                    )
    except OSError as exc:
        return [f"{path}: unreadable ({exc})"]
    except csv.Error as exc:
        return [f"{path}: csv parse error ({exc})"]
    except UnicodeDecodeError as exc:
        return [f"{path}: not valid UTF-8 ({exc})"]
    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print("check-csv: no files given", file=sys.stderr)
        return 1
    failed = False
    for arg in argv:
        for err in check_csv(Path(arg)):
            print(err, file=sys.stderr)
            failed = True
    if failed:
        return 1
    print(f"check-csv: {len(argv)} file(s) structurally clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
