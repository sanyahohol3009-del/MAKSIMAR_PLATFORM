from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_read_model_contract import (
    build_workspace_read_model_contract,
)


def main() -> None:
    contract = build_workspace_read_model_contract()

    print("WORKSPACE READ MODEL PREVIEW")
    print("=" * 130)
    for row in contract.rows:
        print(
            f"{row.workspace_id:<32} | "
            f"{row.workspace_role:<24} | "
            f"{row.primary_display_target_id:<28} | "
            f"panel_count={row.panel_count}"
        )
        print(f"     panel_ids={row.panel_ids}")
        print(f"     {row.description}")


if __name__ == "__main__":
    main()
