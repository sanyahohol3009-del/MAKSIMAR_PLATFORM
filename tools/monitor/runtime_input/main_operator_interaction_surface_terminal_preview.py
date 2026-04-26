#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (  # noqa: E402
    build_main_operator_interaction_surface_contract,
)


def main() -> None:
    """Render the canonical main-operator interaction surface preview."""
    contract = build_main_operator_interaction_surface_contract()

    print("MAIN OPERATOR INTERACTION SURFACE PREVIEW")
    print("=" * 156)

    for entry in contract.entries:
        print(
            f"{entry.operator_intent_id:<20} | "
            f"{entry.surface_class:<22} | "
            f"{entry.intent_kind:<18} | "
            f"approval_required={str(entry.approval_required):<5} | "
            f"handoff_ready={str(entry.handoff_ready):<5}"
        )
        print(
            " " * 5
            + f"pending_approval_visible={entry.pending_approval_visible} | "
            f"forbidden_state_visible={entry.forbidden_state_visible} | "
            f"audit_visible={entry.audit_visible} | "
            f"trace_id={entry.trace_id}"
        )
        print(" " * 5 + entry.description)

    print("-" * 156)
    print(
        f"total_entries={contract.total_entries} | "
        f"read_only_surface_entries={contract.read_only_surface_entries} | "
        f"approval_bound_surface_entries={contract.approval_bound_surface_entries} | "
        f"pending_approval_visible_entries={contract.pending_approval_visible_entries} | "
        f"handoff_ready_entries={contract.handoff_ready_entries} | "
        f"audit_visible_entries={contract.audit_visible_entries}"
    )


if __name__ == "__main__":
    main()
