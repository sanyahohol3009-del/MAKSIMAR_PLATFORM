#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.simulation_result_contract import (  # noqa: E402
    build_simulation_result_contract,
)


def main() -> None:
    contract = build_simulation_result_contract()

    print("SIMULATION RESULT PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.simulation_result_id:<24} | "
            f"{entry.operator_intent_id:<18} | "
            f"{entry.panel_id:<16} | "
            f"{entry.simulation_result_class:<32}"
        )
        print(
            " " * 5
            + f"workspace_id={entry.workspace_id} | "
            f"simulation_result_state={entry.simulation_result_state}"
        )
        print(
            " " * 5
            + f"simulation_evidence_mode={entry.simulation_evidence_mode} | "
            f"approval_required={entry.approval_required} | "
            f"handoff_ready={entry.handoff_ready} | "
            f"review_visible={entry.review_visible}"
        )
        print(
            " " * 5
            + f"operator_visible={entry.operator_visible} | "
            f"trace_id={entry.trace_id}"
        )
        print(" " * 5 + entry.description)

    print("-" * 180)
    print(
        f"total_entries={contract.total_entries} | "
        f"read_only_simulation_entries={contract.read_only_simulation_entries} | "
        f"approval_bound_simulation_entries={contract.approval_bound_simulation_entries} | "
        f"review_visible_entries={contract.review_visible_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
