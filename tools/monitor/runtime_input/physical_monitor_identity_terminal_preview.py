#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.physical_monitor_identity_contract import (  # noqa: E402
    build_physical_monitor_identity_contract,
)


def main() -> None:
    contract = build_physical_monitor_identity_contract()

    print("PHYSICAL MONITOR IDENTITY PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.physical_monitor_id:<24} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.identity_class:<38}"
        )
        print(
            " " * 5
            + f"monitor_inventory_id={entry.monitor_inventory_id} | "
            f"physical_slot_label={entry.physical_slot_label}"
        )
        print(
            " " * 5
            + f"identity_state={entry.identity_state} | "
            f"hotplug_detectable={entry.hotplug_detectable} | "
            f"multi_monitor_capable={entry.multi_monitor_capable} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"hotplug_detectable_entries={contract.hotplug_detectable_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
