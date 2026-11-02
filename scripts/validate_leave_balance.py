#!/usr/bin/env python3
"""Validate configured annual leave balances in LEAVE_REQUEST.md."""

import re
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
REQUEST_DOCUMENT = REPOSITORY_ROOT / "LEAVE_REQUEST.md"
EXPECTED_BALANCES = {
    "casual leave": 12,
    "sick leave": 10,
    "earned leave": 15,
}


def main() -> int:
    if not REQUEST_DOCUMENT.is_file():
        print(f"FAIL: {REQUEST_DOCUMENT.name} was not found")
        return 1

    document = REQUEST_DOCUMENT.read_text(encoding="utf-8-sig")
    errors = []
    balances = {}

    for leave_type, expected_days in EXPECTED_BALANCES.items():
        match = re.search(
            rf"-\s*{re.escape(leave_type)}:\s*(\d+)\s+days?\b",
            document,
            re.IGNORECASE,
        )
        if not match:
            errors.append(f"Missing or invalid annual balance for {leave_type.title()}")
            continue

        actual_days = int(match.group(1))
        balances[leave_type] = actual_days
        if actual_days != expected_days:
            errors.append(
                f"{leave_type.title()} balance is {actual_days} days; expected {expected_days}"
            )

    print("Leave balance validation results:")
    if balances:
        for leave_type, days in balances.items():
            status = "PASS" if days == EXPECTED_BALANCES[leave_type] else "FAIL"
            print(f"- {status}: {leave_type.title()} = {days} days/year")

    if errors:
        for error in errors:
            print(f"- FAIL: {error}")
        print("Result: FAILED")
        return 1

    print("Result: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
