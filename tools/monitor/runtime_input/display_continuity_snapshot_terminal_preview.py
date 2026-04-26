#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_continuity_snapshot_contract import (  # noqa: E402
    build_display_continuity_snapshot_contract,
)


def main() -> None:
    contract = build_display_continuity_snapshot_contract()

    print("DISPLAY CONTINUITY SNAPSHOT PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.snapshot_id:<32} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.snapshot_state:<18} | "
            f"{entry.snapshot_class:<32}"
        )
        print(
            " " * 5
            + f"active_assignments={entry.active_assignments} | "
            f"selected_assignment_present={entry.selected_assignment_present} | "
            f"shared_surface={entry.shared_surface} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"shared_surface_entries={contract.shared_surface_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
