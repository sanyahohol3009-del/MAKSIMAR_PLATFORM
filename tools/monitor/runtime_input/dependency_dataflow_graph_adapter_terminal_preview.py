#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.dataflow_graph_adapter_contract import (  # noqa: E402
    build_dataflow_graph_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_graph_adapter_contract import (  # noqa: E402
    build_dependency_graph_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.graph_selection_mapping_contract import (  # noqa: E402
    build_graph_selection_mapping_contract,
)


def main() -> None:
    dependency_contract = build_dependency_graph_adapter_contract()
    dataflow_contract = build_dataflow_graph_adapter_contract()
    selection_contract = build_graph_selection_mapping_contract()

    print("DEPENDENCY / DATAFLOW GRAPH ADAPTER PREVIEW")
    print("=" * 180)
    print(
        f"dependency_adapter_entries={dependency_contract.total_entries} | "
        f"dataflow_adapter_entries={dataflow_contract.total_entries} | "
        f"selection_mapping_entries={selection_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
