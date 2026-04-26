from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_taxonomy_contract import (
    build_panel_taxonomy_contract,
)


def main() -> None:
    contract = build_panel_taxonomy_contract()

    print("PANEL TAXONOMY PREVIEW")
    print("=" * 110)
    for entry in contract.entries:
        print(
            f"{entry.panel_id:<16} | "
            f"{entry.panel_family:<12} | "
            f"{entry.panel_kind:<12} | "
            f"{entry.panel_role:<22}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
