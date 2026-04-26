from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_contract import (
    build_operator_interaction_read_model_contract,
)


def main() -> None:
    contract = build_operator_interaction_read_model_contract()

    print("OPERATOR INTERACTION READ MODEL PREVIEW")
    print("=" * 180)
    for entry in contract.entries:
        print(
            f"{entry.operator_intent_id:<18} | "
            f"{entry.dashboard_id:<24} | "
            f"{entry.workspace_id:<32} | "
            f"{entry.interaction_lane:<20} | "
            f"{entry.handoff_state:<14}"
        )
        print(
            "     "
            f"intent_kind={entry.intent_kind} | "
            f"approval_state={entry.approval_state} | "
            f"audit_visibility_state={entry.audit_visibility_state}"
        )
        print(
            "     "
            f"approval_required={entry.approval_required} | "
            f"handoff_ready={entry.handoff_ready} | "
            f"operator_visible={entry.operator_visible} | "
            f"trace_id={entry.trace_id}"
        )
        print(f"     {entry.description}")

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"read_only_lane_entries={contract.read_only_lane_entries} | "
        f"approval_bound_lane_entries={contract.approval_bound_lane_entries} | "
        f"approval_required_entries={contract.approval_required_entries} | "
        f"handoff_ready_entries={contract.handoff_ready_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
