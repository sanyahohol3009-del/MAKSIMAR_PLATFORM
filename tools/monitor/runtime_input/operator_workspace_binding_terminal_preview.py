from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_workspace_binding_contract import (
    build_operator_workspace_binding_contract,
)


def main() -> None:
    contract = build_operator_workspace_binding_contract()

    print("OPERATOR WORKSPACE BINDING PREVIEW")
    print("=" * 140)
    for entry in contract.entries:
        print(
            f"{entry.dashboard_id:<28} | "
            f"{entry.workspace_id:<32} | "
            f"{entry.binding_role:<30} | "
            f"order={entry.workspace_order} | "
            f"primary={entry.is_primary_workspace}"
        )
        print(f"     read_only_binding={entry.read_only_binding}")
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
