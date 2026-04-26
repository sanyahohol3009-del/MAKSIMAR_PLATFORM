#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.test_coverage_debt_summary_contract import (  # noqa: E402
    build_test_coverage_debt_summary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.test_warning_cleanup_policy_contract import (  # noqa: E402
    build_test_warning_cleanup_policy_contract,
)


def main() -> None:
    warning_contract = build_test_warning_cleanup_policy_contract()
    coverage_contract = build_test_coverage_debt_summary_contract()

    print("TEST QUALITY CLEANUP PREVIEW")
    print("=" * 180)
    print(
        f"warning_cleanup_entries={warning_contract.total_entries} | "
        f"xdist_sensitive_entries={warning_contract.xdist_sensitive_entries} | "
        f"coverage_debt_entries={coverage_contract.total_entries} | "
        f"high_priority_debt_entries={coverage_contract.high_priority_entries}"
    )


if __name__ == "__main__":
    main()
