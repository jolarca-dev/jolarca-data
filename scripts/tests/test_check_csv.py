"""Regression tests for scripts/check-csv.py (stdlib unittest, no deps).

Guards the fix for the nonexistent upstream `check-csv` pre-commit hook:
the local validator must catch ragged rows, blank headers, and empty files
while accepting the commented-example register shape.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check-csv.py"


def run_check(content: str) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as fh:
        fh.write(content)
        path = fh.name
    return subprocess.run(
        [sys.executable, str(SCRIPT), path], capture_output=True, text=True
    )


class CheckCsvTest(unittest.TestCase):
    def test_well_formed_register_passes(self):
        result = run_check("a,b,c\n1,2,3\n# comment-row,still,three\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_ragged_row_fails(self):
        result = run_check("a,b,c\n1,2\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("2 columns, expected 3", result.stderr)

    def test_blank_header_fails(self):
        result = run_check(",,\n1,2,3\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("header row is blank", result.stderr)

    def test_empty_file_fails(self):
        result = run_check("")
        self.assertEqual(result.returncode, 1)
        self.assertIn("header row", result.stderr)

    def test_no_args_fails(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 1)


if __name__ == "__main__":
    unittest.main()
