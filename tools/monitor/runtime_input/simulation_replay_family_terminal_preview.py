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
from MAKSIMAR_CORE_LIB.oob_dashboard.simulation_result_contract import (  # noqa: E402
    build_simulation_result_contract,
)


def main() -> None:
    simulation_result_contract = build_simulation_result_contract()
    replay_artifact_contract = build_replay_artifact_contract()

    print("SIMULATION REPLAY FAMILY PREVIEW")
    print("=" * 180)
    print(
        f"simulation_result_entries={simulation_result_contract.total_entries} | "
        f"replay_artifact_entries={replay_artifact_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
