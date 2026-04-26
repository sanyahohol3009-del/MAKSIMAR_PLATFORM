#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_runtime_contract import (  # noqa: E402
    build_presentation_bundle_runtime_contract,
)


def main() -> None:
    contract = build_presentation_bundle_runtime_contract()

    print("PRESENTATION BUNDLE RUNTIME PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.presentation_bundle_runtime_id:<32} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.presentation_bundle_runtime_class:<32}"
        )
        print(
            " " * 5
            + f"workspace_id={entry.workspace_id} | "
            f"presentation_bundle_runtime_state={entry.presentation_bundle_runtime_state} | "
            f"presentation_bundle_runtime_mode={entry.presentation_bundle_runtime_mode}"
        )
        print(
            " " * 5
            + f"visible_state_ready={entry.visible_state_ready} | "
            f"operator_visible={entry.operator_visible} | "
            f"truth_bound={entry.truth_bound}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"foundation_runtime_entries={contract.foundation_runtime_entries} | "
        f"interaction_runtime_entries={contract.interaction_runtime_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries} | "
        f"truth_bound_entries={contract.truth_bound_entries}"
    )


if __name__ == "__main__":
    main()
