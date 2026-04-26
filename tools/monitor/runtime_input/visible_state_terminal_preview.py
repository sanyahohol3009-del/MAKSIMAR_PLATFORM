#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visible_state_contract import (  # noqa: E402
    build_visible_state_contract,
)


def main() -> None:
    contract = build_visible_state_contract()

    print("VISIBLE STATE PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.visible_state_id:<20} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.visible_state_class:<26}"
        )
        print(
            " " * 5
            + f"workspace_id={entry.workspace_id} | "
            f"visible_state_state={entry.visible_state_state} | "
            f"visible_state_mode={entry.visible_state_mode}"
        )
        print(
            " " * 5
            + f"final_visible_screen_state_ready={entry.final_visible_screen_state_ready} | "
            f"operator_visible={entry.operator_visible} | "
            f"truth_bound={entry.truth_bound}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"foundation_visible_entries={contract.foundation_visible_entries} | "
        f"interaction_visible_entries={contract.interaction_visible_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries} | "
        f"truth_bound_entries={contract.truth_bound_entries}"
    )


if __name__ == "__main__":
    main()
