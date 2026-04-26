#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_conflict_resolution_contract import (  # noqa: E402
    build_display_conflict_resolution_contract,
)


def main() -> None:
    contract = build_display_conflict_resolution_contract()

    print("DISPLAY CONFLICT RESOLUTION PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.conflict_id:<22} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.conflict_decision:<28} | "
            f"{entry.conflict_class:<32}"
        )
        print(
            " " * 5
            + f"incumbent_assignment_id={entry.incumbent_assignment_id} | "
            f"candidate_display_target_id={entry.candidate_display_target_id} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"pinned_conflict_entries={contract.pinned_conflict_entries} | "
        f"replaceable_conflict_entries={contract.replaceable_conflict_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
