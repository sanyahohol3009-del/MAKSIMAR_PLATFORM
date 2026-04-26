#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.module_graph_audit_adapter_contract import (  # noqa: E402
    build_module_graph_audit_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_graph_navigation_adapter_contract import (  # noqa: E402
    build_module_graph_navigation_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.module_graph_surface_adapter_contract import (  # noqa: E402
    build_module_graph_surface_adapter_contract,
)


def main() -> None:
    surface_contract = build_module_graph_surface_adapter_contract()
    navigation_contract = build_module_graph_navigation_adapter_contract()
    audit_contract = build_module_graph_audit_adapter_contract()

    print("MODULE GRAPH ADAPTER PREVIEW")
    print("=" * 180)
    print(
        f"surface_adapter_entries={surface_contract.total_entries} | "
        f"navigation_adapter_entries={navigation_contract.total_entries} | "
        f"audit_adapter_entries={audit_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
