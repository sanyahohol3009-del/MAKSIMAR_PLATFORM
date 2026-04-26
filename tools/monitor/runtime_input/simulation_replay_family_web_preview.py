#!/usr/bin/env python3
from __future__ import annotations

import html
import json
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
    payload = {
        "simulation_result_contract": build_simulation_result_contract().total_entries,
        "replay_artifact_contract": build_replay_artifact_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Simulation Replay Family</title></head><body>")
    print("<h1>Simulation Replay Family</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
