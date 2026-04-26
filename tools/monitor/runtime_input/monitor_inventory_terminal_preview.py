#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (  # noqa: E402
    build_monitor_inventory_contract,
)


def main() -> None:
    contract = build_monitor_inventory_contract()

    print("MONITOR INVENTORY PREVIEW")
    print("=" * 150)

    for entry in contract.entries:
        print(
            f"{entry.monitor_id:<22} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.monitor_role:<28} | "
            f"foundation={str(entry.supports_foundation_panels):<5} | "
            f"operator={str(entry.supports_operator_surfaces):<5}"
        )
        print(
            " " * 5
            + f"multi_monitor_capable={entry.multi_monitor_capable} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 150)
    print(
        f"total_entries={contract.total_entries} | "
        f"foundation_monitor_entries={contract.foundation_monitor_entries} | "
        f"operator_monitor_entries={contract.operator_monitor_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
