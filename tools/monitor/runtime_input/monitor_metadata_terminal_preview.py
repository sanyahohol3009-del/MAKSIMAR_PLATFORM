#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_metadata_contract import (  # noqa: E402
    build_monitor_metadata_contract,
)


def main() -> None:
    contract = build_monitor_metadata_contract()

    print("MONITOR METADATA PREVIEW")
    print("=" * 170)

    for entry in contract.entries:
        print(
            f"{entry.monitor_id:<22} | "
            f"{entry.display_target_id:<30} | "
            f"{entry.display_role:<28} | "
            f"{entry.display_zone:<28}"
        )
        print(
            " " * 5
            + f"fallback={entry.fallback_display_target_id} | "
            f"occupancy_class={entry.occupancy_class} | "
            f"assignment_count={entry.assignment_count}"
        )
        print(
            " " * 5
            + f"foundation={entry.supports_foundation_panels} | "
            f"operator={entry.supports_operator_surfaces} | "
            f"multi_monitor_capable={entry.multi_monitor_capable} | "
            f"operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 170)
    print(
        f"total_entries={contract.total_entries} | "
        f"foundation_metadata_entries={contract.foundation_metadata_entries} | "
        f"operator_metadata_entries={contract.operator_metadata_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
