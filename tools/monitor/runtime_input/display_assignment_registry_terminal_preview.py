#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (  # noqa: E402
    build_display_assignment_registry_contract,
)


def main() -> None:
    contract = build_display_assignment_registry_contract()

    print("DISPLAY ASSIGNMENT REGISTRY PREVIEW")
    print("=" * 175)

    for entry in contract.entries:
        print(
            f"{entry.assignment_id:<22} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.assignment_role:<30}"
        )
        print(
            " " * 5
            + f"panel_or_surface_id={entry.panel_or_surface_id} | "
            f"workspace_id={entry.workspace_id}"
        )
        print(
            " " * 5
            + f"assignment_state={entry.assignment_state} | "
            f"replaceable={entry.replaceable} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 175)
    print(
        f"total_entries={contract.total_entries} | "
        f"active_entries={contract.active_entries} | "
        f"replaceable_entries={contract.replaceable_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
