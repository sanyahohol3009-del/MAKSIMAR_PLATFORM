#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_visible_state_contract import (  # noqa: E402
    build_dashboard_visible_state_contract,
)


def main() -> None:
    contract = build_dashboard_visible_state_contract()

    print("DASHBOARD VISIBLE STATE PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.dashboard_visible_state_id:<28} | "
            f"{entry.workspace_id:<28} | "
            f"{entry.dashboard_visible_state:<32} | "
            f"{entry.dashboard_visible_state_class:<36}"
        )
        print(
            " " * 5
            + f"preview_surface_ready={entry.preview_surface_ready} | "
            f"rollback_readiness_ready={entry.rollback_readiness_ready} | "
            f"workspace_restore_ready={entry.workspace_restore_ready}"
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
