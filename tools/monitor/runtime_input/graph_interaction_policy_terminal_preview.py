#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_interaction_policy_contract import (  # noqa: E402
    build_graph_interaction_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.graph_interaction_selection_contract import (  # noqa: E402
    build_graph_interaction_selection_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.graph_non_execution_guard_contract import (  # noqa: E402
    build_graph_non_execution_guard_contract,
)


def main() -> None:
    policy_contract = build_graph_interaction_policy_contract()
    guard_contract = build_graph_non_execution_guard_contract()
    selection_contract = build_graph_interaction_selection_contract()

    print("SAFE GRAPH INTERACTION POLICY PREVIEW")
    print("=" * 180)
    print(
        f"interaction_policy_entries={policy_contract.total_entries} | "
        f"guard_entries={guard_contract.total_entries} | "
        f"selection_entries={selection_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
