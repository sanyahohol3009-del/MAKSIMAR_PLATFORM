#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_restore_contract import (  # noqa: E402
    build_workspace_restore_contract,
)


def main() -> None:
    contract = build_workspace_restore_contract()

    print("WORKSPACE RESTORE PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.workspace_restore_id:<24} | "
            f"{entry.workspace_id:<32} | "
            f"{entry.workspace_restore_state:<24} | "
            f"{entry.workspace_restore_class:<30}"
        )
        print(
            " " * 5
            + f"workspace_read_model_ready={entry.workspace_read_model_ready} | "
            f"display_assignment_restore_ready={entry.display_assignment_restore_ready} | "
            f"display_restore_continuity_ready={entry.display_restore_continuity_ready}"
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
