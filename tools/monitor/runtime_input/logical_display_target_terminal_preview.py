#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.logical_display_target_contract import (  # noqa: E402
    build_logical_display_target_contract,
)


def main() -> None:
    contract = build_logical_display_target_contract()

    print("LOGICAL DISPLAY TARGET PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.logical_target_id:<28} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.logical_target_class:<36}"
        )
        print(
            " " * 5
            + f"physical_monitor_id={entry.physical_monitor_id} | "
            f"display_role={entry.display_role} | "
            f"display_zone={entry.display_zone}"
        )
        print(
            " " * 5
            + f"logical_target_state={entry.logical_target_state} | "
            f"fallback_display_target_id={entry.fallback_display_target_id} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
