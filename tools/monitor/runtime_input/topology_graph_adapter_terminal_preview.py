#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.topology_graph_edge_adapter_contract import (  # noqa: E402
    build_topology_graph_edge_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.topology_graph_layout_contract import (  # noqa: E402
    build_topology_graph_layout_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.topology_graph_node_adapter_contract import (  # noqa: E402
    build_topology_graph_node_adapter_contract,
)


def main() -> None:
    node_contract = build_topology_graph_node_adapter_contract()
    edge_contract = build_topology_graph_edge_adapter_contract()
    layout_contract = build_topology_graph_layout_contract()

    print("TOPOLOGY GRAPH ADAPTER PREVIEW")
    print("=" * 180)
    print(
        f"node_adapter_entries={node_contract.total_entries} | "
        f"edge_adapter_entries={edge_contract.total_entries} | "
        f"layout_entries={layout_contract.total_entries} | "
        f"layout_edge_count={layout_contract.edge_count}"
    )


if __name__ == "__main__":
    main()
