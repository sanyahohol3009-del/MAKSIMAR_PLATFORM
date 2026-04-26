#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.data_flow_panel_contract import (  # noqa: E402
    build_data_flow_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_map_panel_contract import (  # noqa: E402
    build_dependency_map_panel_contract,
)


def main() -> None:
    data_flow_contract = build_data_flow_panel_contract()
    dependency_map_contract = build_dependency_map_panel_contract()

    print("DEPENDENCY / DATAFLOW FAMILY PREVIEW")
    print("=" * 180)
    print(
        f"data_flow_entries={data_flow_contract.total_entries} | "
        f"dependency_map_entries={dependency_map_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
