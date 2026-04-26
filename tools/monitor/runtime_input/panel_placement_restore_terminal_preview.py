#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_placement_restore_contract import (  # noqa: E402
    build_panel_placement_restore_contract,
)


def main() -> None:
    contract = build_panel_placement_restore_contract()

    print("PANEL PLACEMENT RESTORE PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.panel_placement_restore_id:<32} | "
            f"{entry.workspace_id:<32} | "
            f"{entry.panel_placement_restore_state:<32} | "
            f"{entry.panel_placement_restore_class:<36}"
        )
        print(
            " " * 5
            + f"dashboard_session_restore_ready={entry.dashboard_session_restore_ready} | "
            f"display_assignment_restore_ready={entry.display_assignment_restore_ready}"
        )
        print(
            " " * 5
            + f"operator_visible={entry.operator_visible} | "
            f"truth_bound={entry.truth_bound}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"ready_entries={contract.ready_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries} | "
        f"truth_bound_entries={contract.truth_bound_entries}"
    )


if __name__ == "__main__":
    main()
