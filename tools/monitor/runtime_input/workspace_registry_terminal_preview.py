from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


def main() -> None:
    contract = build_workspace_registry_contract()

    print("WORKSPACE REGISTRY PREVIEW")
    print("=" * 120)
    for entry in contract.entries:
        print(
            f"{entry.workspace_id:<32} | "
            f"{entry.workspace_role:<24} | "
            f"{entry.primary_display_target_id:<28}"
        )
        print(f"     panels={entry.included_panel_ids}")
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
