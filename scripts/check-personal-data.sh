#!/usr/bin/env bash
# check-personal-data.sh — PII tripwire for committed files.
# Flags Baltic national IDs, IBANs, realistic phone shapes, and emails
# outside reserved example domains. TRIPWIRE ONLY: passing does not
# make a commit lawful (CONTRIBUTING.md). synthetic/pii-canaries/ is
# excluded by design (scanner self-test material — see its README).
set -euo pipefail

cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"

EXCLUDE='synthetic/pii-canaries/'
FILES=$(git ls-files -- '*.md' '*.csv' '*.txt' '*.yml' '*.yaml' '*.sql' '*.py' '*.sh' 2>/dev/null \
    | grep -v "^${EXCLUDE}" || true)

if [ -z "$FILES" ]; then
    # Not a git repo (or nothing tracked): fall back to filesystem scan.
    FILES=$(find . \
        \( -name '*.md' -o -name '*.csv' -o -name '*.yml' -o -name '*.yaml' \
           -o -name '*.sql' -o -name '*.py' -o -name '*.sh' -o -name '*.txt' \) \
        -not -path './.git/*' -not -path './.venv/*' -not -path './.idea/*' \
        -not -path "./${EXCLUDE}*")
fi

PATTERNS=(
    # Baltic national IDs: LT asmens kodas / EE isikukood (11 digits)
    '\b[0-9]{11}\b'
    # LV personas kods (DDMMYY-NNNNN)
    '\b[0-9]{6}-[0-9]{5}\b'
    # Baltic IBANs with 12+ following digits (grouped or not)
    '\b(LT|LV|EE)[0-9]{2}([ ]?[0-9]{4}){3,}\b'
    # Realistic Baltic mobile shapes (LT +370 6xxxxxxx, LV +371 2xxxxxxx, EE +372 5xxxxxxx)
    '\+37[012][ -]?[625][0-9]{6,7}\b'
)

fail=0
for pattern in "${PATTERNS[@]}"; do
    # shellcheck disable=SC2086
    matches=$(grep -nIE "$pattern" $FILES 2>/dev/null || true)
    if [ -n "$matches" ]; then
        echo "PII-shaped pattern detected ($pattern):" >&2
        echo "$matches" >&2
        fail=1
    fi
done

# Emails outside reserved example domains. Domain must start with a
# letter (excludes action-pinned SHAs like checkout@<hex> and image
# refs like postgres@127.0.0.1).
# shellcheck disable=SC2086
emails=$(grep -nIEo '[A-Za-z0-9._%+-]+@[A-Za-z][A-Za-z0-9.-]*\.[A-Za-z]{2,}' $FILES 2>/dev/null \
    | grep -vE '@example\.(test|com|org|net)([:0-9]|$)' || true)
if [ -n "$emails" ]; then
    echo "Email addresses outside reserved example domains:" >&2
    echo "$emails" >&2
    fail=1
fi

if [ "$fail" -ne 0 ]; then
    echo "FAIL: personal-data tripwire fired — see CONTRIBUTING.md minimization rules." >&2
    exit 1
fi
echo "personal-data tripwire OK"
