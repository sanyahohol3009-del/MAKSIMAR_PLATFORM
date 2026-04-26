#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_replacement_policy_contract import (  # noqa: E402
    build_display_replacement_policy_contract,
)


def main() -> None:
    contract = build_display_replacement_policy_contract()

    print("DISPLAY REPLACEMENT POLICY PREVIEW")
    print("=" * 170)

    for entry in contract.entries:
        print(
            f"{entry.display_target_id:<30} | "
            f"{entry.replacement_decision:<31} | "
            f"{entry.replacement_class:<40}"
        )
        print(
            " " * 5
            + f"active_assignments={entry.active_assignments} | "
            f"replaceable_assignments={entry.replaceable_assignments} | "
            f"pinned_assignments={entry.pinned_assignments} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 170)
    print(
        f"total_entries={contract.total_entries} | "
        f"not_replaceable_entries={contract.not_replaceable_entries} | "
        f"replaceable_entries={contract.replaceable_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
