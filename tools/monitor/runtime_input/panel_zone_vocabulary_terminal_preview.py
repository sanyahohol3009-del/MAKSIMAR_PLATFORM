from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_zone_vocabulary_contract import (
    build_panel_zone_vocabulary_contract,
)


def main() -> None:
    contract = build_panel_zone_vocabulary_contract()

    print("PANEL ZONE / SLOT VOCABULARY PREVIEW")
    print("=" * 130)
    for entry in contract.entries:
        print(
            f"{entry.layout_zone:<24} | "
            f"{entry.layout_slot_id:<28} | "
            f"{entry.slot_family:<22} | "
            f"order={entry.slot_order}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
