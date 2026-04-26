#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.free_display_selection_contract import (  # noqa: E402
    build_free_display_selection_contract,
)


def main() -> None:
    contract = build_free_display_selection_contract()
    entry = contract.entries[0]

    print("FREE DISPLAY SELECTION PREVIEW")
    print("=" * 170)
    print(
        f"{entry.selection_id:<28} | "
        f"{entry.requested_role_hint:<28} | "
        f"{entry.selection_decision:<40}"
    )
    print(
        " " * 5
        + f"selection_reason={entry.selection_reason} | "
        f"candidate_display_target_id={entry.candidate_display_target_id} | "
        f"operator_visible={entry.operator_visible}"
    )
    print(" " * 5 + entry.description)
    print("-" * 170)
    print(
        f"total_entries={contract.total_entries} | "
        f"no_free_display_entries={contract.no_free_display_entries} | "
        f"replaceable_candidate_entries={contract.replaceable_candidate_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
