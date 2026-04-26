#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.approval_queue_panel_content_contract import (  # noqa: E402
    build_approval_queue_panel_content_contract,
)


def main() -> None:
    contract = build_approval_queue_panel_content_contract()

    print("APPROVAL QUEUE PANEL PREVIEW")
    print("=" * 150)

    for entry in contract.entries:
        print(
            f"{entry.operator_intent_id:<20} | "
            f"{entry.approval_queue_class:<24} | "
            f"{entry.intent_kind:<18} | "
            f"approval_required={str(entry.approval_required):<5} | "
            f"handoff_ready={str(entry.handoff_ready):<5}"
        )
        print(
            " " * 5
            + f"pending_approval_visible={entry.pending_approval_visible} | "
            f"trace_id={entry.trace_id}"
        )
        print(" " * 5 + entry.description)

    print("-" * 150)
    print(
        f"total_entries={contract.total_entries} | "
        f"pending_approval_entries={contract.pending_approval_entries} | "
        f"handoff_ready_entries={contract.handoff_ready_entries}"
    )


if __name__ == "__main__":
    main()
