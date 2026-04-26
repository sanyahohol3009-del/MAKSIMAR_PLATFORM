from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.view_targeting_contract import (
    build_view_targeting_contract,
)


def main() -> None:
    contract = build_view_targeting_contract()

    print("VIEW TARGETING PREVIEW")
    print("=" * 110)
    for entry in contract.entries:
        print(
            f"{entry.panel_id:<16} | "
            f"{entry.view_id:<28} | "
            f"{entry.view_target_kind:<18} | "
            f"{entry.view_scope:<12}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
