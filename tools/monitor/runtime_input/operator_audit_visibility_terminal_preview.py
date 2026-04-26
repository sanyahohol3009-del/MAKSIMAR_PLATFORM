from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_contract import (
    build_operator_audit_visibility_contract,
)


def main() -> None:
    contract = build_operator_audit_visibility_contract()

    print("OPERATOR AUDIT VISIBILITY PREVIEW")
    print("=" * 160)
    for entry in contract.entries:
        print(
            f"{entry.dashboard_id:<28} | "
            f"{entry.audit_surface_id:<28} | "
            f"{entry.audit_scope:<26} | "
            f"{entry.audit_visibility_mode:<30}"
        )
        print(
            "     "
            f"hidden_audit_allowed={entry.hidden_audit_allowed} | "
            f"policy_visibility_required={entry.policy_visibility_required} | "
            f"approval_visibility_required={entry.approval_visibility_required}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
