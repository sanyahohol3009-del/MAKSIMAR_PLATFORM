from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_contract import (
    build_operator_control_plane_handoff_contract,
)


def main() -> None:
    contract = build_operator_control_plane_handoff_contract()

    print("OPERATOR CONTROL PLANE HANDOFF PREVIEW")
    print("=" * 160)
    for entry in contract.entries:
        print(
            f"{entry.dashboard_id:<28} | "
            f"{entry.interaction_surface_id:<34} | "
            f"{entry.handoff_target:<32} | "
            f"{entry.handoff_mode:<26}"
        )
        print(
            "     "
            f"action_submission_allowed={entry.action_submission_allowed} | "
            f"direct_execution_allowed={entry.direct_execution_allowed} | "
            f"approval_required={entry.approval_required} | "
            f"policy_gate_required={entry.policy_gate_required}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
