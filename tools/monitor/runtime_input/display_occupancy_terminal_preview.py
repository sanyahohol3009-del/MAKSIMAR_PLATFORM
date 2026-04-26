#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_occupancy_contract import (  # noqa: E402
    build_display_occupancy_contract,
)


def main() -> None:
    contract = build_display_occupancy_contract()

    print("DISPLAY OCCUPANCY PREVIEW")
    print("=" * 160)

    for entry in contract.entries:
        print(
            f"{entry.display_target_id:<30} | "
            f"{entry.occupancy_state:<22} | "
            f"{entry.occupancy_class:<30}"
        )
        print(
            " " * 5
            + f"total_assignments={entry.total_assignments} | "
            f"replaceable_assignments={entry.replaceable_assignments} | "
            f"pinned_assignments={entry.pinned_assignments} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 160)
    print(
        f"total_entries={contract.total_entries} | "
        f"pinned_entries={contract.pinned_entries} | "
        f"replaceable_entries={contract.replaceable_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
