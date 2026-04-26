#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.action_queue_panel_content_contract import (  # noqa: E402
    build_action_queue_panel_content_contract,
)


def main() -> None:
    contract = build_action_queue_panel_content_contract()

    print("ACTION QUEUE PANEL PREVIEW")
    print("=" * 150)

    for entry in contract.entries:
        print(
            f"{entry.operator_intent_id:<20} | "
            f"{entry.action_queue_class:<28} | "
            f"{entry.intent_kind:<18} | "
            f"approval_required={str(entry.approval_required):<5} | "
            f"handoff_ready={str(entry.handoff_ready):<5}"
        )
        print(
            " " * 5
            + f"trace_id={entry.trace_id} | operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 150)
    print(
        f"total_entries={contract.total_entries} | "
        f"read_only_entries={contract.read_only_entries} | "
        f"approval_bound_entries={contract.approval_bound_entries} | "
        f"handoff_ready_entries={contract.handoff_ready_entries}"
    )


if __name__ == "__main__":
    main()
