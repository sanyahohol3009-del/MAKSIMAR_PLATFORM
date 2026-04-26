#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.replay_artifact_contract import (  # noqa: E402
    build_replay_artifact_contract,
)


def main() -> None:
    contract = build_replay_artifact_contract()

    print("REPLAY ARTIFACT PREVIEW")
    print("=" * 180)

    for entry in contract.entries:
        print(
            f"{entry.replay_artifact_id:<24} | "
            f"{entry.operator_intent_id:<18} | "
            f"{entry.panel_id:<16} | "
            f"{entry.replay_artifact_class:<28}"
        )
        print(
            " " * 5
            + f"workspace_id={entry.workspace_id} | "
            f"replay_artifact_state={entry.replay_artifact_state}"
        )
        print(
            " " * 5
            + f"replay_evidence_mode={entry.replay_evidence_mode} | "
            f"approval_required={entry.approval_required} | "
            f"handoff_ready={entry.handoff_ready} | "
            f"replay_visible={entry.replay_visible}"
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
        f"read_only_replay_entries={contract.read_only_replay_entries} | "
        f"approval_bound_replay_entries={contract.approval_bound_replay_entries} | "
        f"replay_visible_entries={contract.replay_visible_entries} | "
        f"operator_visible_entries={contract.operator_visible_entries}"
    )


if __name__ == "__main__":
    main()
