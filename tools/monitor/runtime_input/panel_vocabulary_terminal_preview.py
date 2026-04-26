from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_vocabulary_contract import (
    build_panel_vocabulary_contract,
)


def main() -> None:
    contract = build_panel_vocabulary_contract()

    print("PANEL VOCABULARY PREVIEW")
    print("=" * 80)
    for entry in contract.entries:
        print(
            f"{entry.display_priority:02d} | "
            f"{entry.panel_id:<16} | "
            f"{entry.panel_family:<12} | "
            f"{entry.panel_kind:<10} | "
            f"{entry.title}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
