from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_guard_contract import (
    build_operator_interaction_guard_contract,
)


def main() -> None:
    contract = build_operator_interaction_guard_contract()

    print("OPERATOR INTERACTION GUARD PREVIEW")
    print("=" * 150)
    for entry in contract.entries:
        print(
            f"{entry.dashboard_id:<28} | "
            f"{entry.interaction_surface_id:<34} | "
            f"{entry.guard_mode:<30}"
        )
        print(
            "     "
            f"direct_execution_allowed={entry.direct_execution_allowed} | "
            f"approval_required={entry.approval_required} | "
            f"policy_gate_required={entry.policy_gate_required} | "
            f"forbidden_state_visible={entry.forbidden_state_visible}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
