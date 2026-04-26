from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_source_binding_contract import (
    build_panel_source_binding_contract,
)


def main() -> None:
    contract = build_panel_source_binding_contract()

    print("PANEL SOURCE BINDING PREVIEW")
    print("=" * 120)
    for entry in contract.entries:
        print(
            f"{entry.panel_id:<16} | "
            f"{entry.source_binding:<22} | "
            f"{entry.source_contract_name:<38} | "
            f"{entry.source_scope:<12} | "
            f"read_only={str(entry.read_only):<5}"
        )
        print(f"     {entry.description}")


if __name__ == "__main__":
    main()
