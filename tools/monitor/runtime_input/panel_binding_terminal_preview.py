from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_contract import (
    build_panel_binding_contract,
)


def main() -> None:
    contract = build_panel_binding_contract()

    print("PANEL BINDING PREVIEW")
    print("=" * 120)
    for entry in contract.entries:
        print(
            f"{entry.panel_id:<16} | "
            f"{entry.display_target_id:<28} | "
            f"main={str(entry.eligible_for_main_dashboard):<5} | "
            f"oob={str(entry.eligible_for_oob_dashboard):<5} | "
            f"{entry.binding_reason}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
