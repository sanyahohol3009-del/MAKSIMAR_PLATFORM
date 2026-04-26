#!/usr/bin/env python3
from __future__ import annotations

import html
import json
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
    payload = {
        "topology_panel_content_contract": build_topology_panel_content_contract().total_entries,
        "node_topology_panel_contract": build_node_topology_panel_contract().total_entries,
        "data_flow_panel_contract": build_data_flow_panel_contract().total_entries,
        "dependency_map_panel_contract": build_dependency_map_panel_contract().total_entries,
        "dashboard_execution_panels_shell_contract": (
            build_dashboard_execution_panels_shell_contract().total_panels
        ),
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Topology Rich Family</title></head><body>")
    print("<h1>Topology Rich Family</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
