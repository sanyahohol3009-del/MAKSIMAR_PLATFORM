from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.layout_composition_contract import (
    build_layout_composition_contract,
)


def main() -> None:
    contract = build_layout_composition_contract()

    print("LAYOUT COMPOSITION PREVIEW")
    print("=" * 130)
    for entry in contract.entries:
        print(
            f"{entry.workspace_id:<32} | "
            f"{entry.panel_id:<16} | "
            f"{entry.layout_slot_id:<28} | "
            f"{entry.layout_zone:<24} | "
            f"order={entry.slot_order}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
