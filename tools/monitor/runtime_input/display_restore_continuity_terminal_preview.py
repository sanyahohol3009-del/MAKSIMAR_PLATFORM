#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_restore_continuity_contract import (  # noqa: E402
    build_display_restore_continuity_contract,
)


def main() -> None:
    contract = build_display_restore_continuity_contract()

    print("DISPLAY RESTORE CONTINUITY PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.continuity_id:<30} | "
            f"{entry.assignment_id:<22} | "
            f"{entry.display_target_id:<30}"
        )
        print(
            " " * 5
            + f"restore_continuity_state={entry.restore_continuity_state} | "
            f"restore_continuity_class={entry.restore_continuity_class} | "
            f"workspace_id={entry.workspace_id} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"direct_restore_entries={contract.direct_restore_entries} | "
        f"shared_surface_restore_entries={contract.shared_surface_restore_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
