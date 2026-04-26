from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_contract import (
    build_main_operator_dashboard_contract,
)


def main() -> None:
    contract = build_main_operator_dashboard_contract()

    print("MAIN OPERATOR DASHBOARD PREVIEW")
    print("=" * 120)
    for entry in contract.entries:
        print(
            f"{entry.dashboard_id:<28} | "
            f"{entry.dashboard_role:<20} | "
            f"{entry.primary_workspace_id:<32}"
        )
        print(f"     secondary_workspaces={entry.secondary_workspace_ids}")
        print(
            "     "
            f"read_only_foundation_reuse={entry.read_only_foundation_reuse} | "
            f"creates_second_root={entry.creates_second_root}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
