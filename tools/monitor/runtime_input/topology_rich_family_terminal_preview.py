#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_execution_shell_contract import (  # noqa: E402
    build_dashboard_execution_panels_shell_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.data_flow_panel_contract import (  # noqa: E402
    build_data_flow_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_map_panel_contract import (  # noqa: E402
    build_dependency_map_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.node_topology_panel_contract import (  # noqa: E402
    build_node_topology_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_content_contract import (  # noqa: E402
    build_topology_panel_content_contract,
)


def main() -> None:
    topology_contract = build_topology_panel_content_contract()
    node_topology_contract = build_node_topology_panel_contract()
    data_flow_contract = build_data_flow_panel_contract()
    dependency_map_contract = build_dependency_map_panel_contract()
    execution_shell_contract = build_dashboard_execution_panels_shell_contract()

    print("TOPOLOGY RICH FAMILY PREVIEW")
    print("=" * 180)
    print(
        f"topology_entries={topology_contract.total_entries} | "
        f"node_topology_entries={node_topology_contract.total_entries} | "
        f"data_flow_entries={data_flow_contract.total_entries} | "
        f"dependency_map_entries={dependency_map_contract.total_entries} | "
        f"execution_shell_panels={execution_shell_contract.total_panels}"
    )


if __name__ == "__main__":
    main()
