#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_contract import (  # noqa: E402
    build_preview_surface_contract,
)


def main() -> None:
    contract = build_preview_surface_contract()

    print("PREVIEW SURFACE PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.preview_surface_id:<24} | "
            f"{entry.panel_id:<18} | "
            f"{entry.workspace_id:<32} | "
            f"{entry.preview_surface_class:<28}"
        )
        print(
            " " * 5
            + f"preview_surface_state={entry.preview_surface_state} | "
            f"preview_generation_mode={entry.preview_generation_mode}"
        )
        print(
            " " * 5
            + f"visible_in_navigation={entry.visible_in_navigation} | "
            f"visible_in_main_dashboard={entry.visible_in_main_dashboard} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"foundation_preview_entries={contract.foundation_preview_entries} | "
        f"interaction_preview_entries={contract.interaction_preview_entries} | "
        f"panel_preview_generation_entries={contract.panel_preview_generation_entries} | "
        f"fixture_preview_generation_entries={contract.fixture_preview_generation_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
