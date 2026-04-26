from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_dashboard_read_model_contract import (
    build_main_operator_dashboard_read_model_contract,
)


def main() -> None:
    contract = build_main_operator_dashboard_read_model_contract()

    print("MAIN OPERATOR DASHBOARD READ MODEL PREVIEW")
    print("=" * 150)
    for row in contract.rows:
        print(
            f"{row.dashboard_id:<28} | "
            f"{row.dashboard_role:<20} | "
            f"{row.primary_workspace_id:<32} | "
            f"workspaces={row.total_workspace_count} | "
            f"panels={row.total_panel_count}"
        )
        print(f"     secondary_workspaces={row.secondary_workspace_ids}")
        print(
            "     "
            f"read_only_foundation_reuse={row.read_only_foundation_reuse} | "
            f"supports_multimonitor_layout={row.supports_multimonitor_layout} | "
            f"supports_voice_gesture_addressing={row.supports_voice_gesture_addressing}"
        )
        print(f"     {row.description}")


if __name__ == "__main__":
    main()
