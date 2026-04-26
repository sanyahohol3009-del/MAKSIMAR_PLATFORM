#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.audit_timeline_panel_content_contract import (  # noqa: E402
    build_audit_timeline_panel_content_contract,
)


def main() -> None:
    contract = build_audit_timeline_panel_content_contract()

    print("AUDIT TIMELINE PANEL PREVIEW")
    print("=" * 150)

    for entry in contract.entries:
        print(
            f"{entry.operator_intent_id:<20} | "
            f"{entry.audit_timeline_class:<28} | "
            f"{entry.intent_kind:<18} | "
            f"approval_required={str(entry.approval_required):<5} | "
            f"audit_visible={str(entry.audit_visible):<5}"
        )
        print(
            " " * 5
            + f"trace_id={entry.trace_id} | operator_visible={entry.operator_visible}"
        )
        print(" " * 5 + entry.description)

    print("-" * 150)
    print(
        f"total_entries={contract.total_entries} | "
        f"audit_visible_entries={contract.audit_visible_entries} | "
        f"approval_required_entries={contract.approval_required_entries}"
    )


if __name__ == "__main__":
    main()
