from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_visibility_policy_contract import (
    build_panel_visibility_policy_contract,
)


def main() -> None:
    contract = build_panel_visibility_policy_contract()

    print("PANEL VISIBILITY POLICY PREVIEW")
    print("=" * 130)
    for entry in contract.entries:
        print(
            f"{entry.panel_id:<16} | "
            f"{entry.visibility_policy:<15} | "
            f"operator={str(entry.operator_visible):<5} | "
            f"nav={str(entry.visible_in_navigation):<5} | "
            f"oob={str(entry.visible_in_oob_dashboard):<5} | "
            f"main={str(entry.visible_in_main_dashboard):<5}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
