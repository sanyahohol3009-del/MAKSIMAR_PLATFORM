from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)


def main() -> None:
    contract = build_panel_view_display_chain_contract()

    print("PANEL VIEW DISPLAY CHAIN PREVIEW")
    print("=" * 140)
    for entry in contract.entries:
        print(
            f"{entry.panel_id:<16} | "
            f"{entry.view_id:<28} | "
            f"{entry.display_target_id:<28} | "
            f"{entry.display_role:<28} | "
            f"{entry.display_zone:<28}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
