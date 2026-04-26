#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.degraded_mode_panel_contract import (  # noqa: E402
    build_degraded_mode_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.project_map_panel_contract import (  # noqa: E402
    build_project_map_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.queue_load_panel_contract import (  # noqa: E402
    build_queue_load_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.version_control_panel_contract import (  # noqa: E402
    build_version_control_panel_contract,
)


def main() -> None:
    payload = {
        "queue_load_panel_contract": build_queue_load_panel_contract().total_entries,
        "degraded_mode_panel_contract": build_degraded_mode_panel_contract().total_entries,
        "project_map_panel_contract": build_project_map_panel_contract().total_entries,
        "version_control_panel_contract": build_version_control_panel_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Node Resources Family</title></head><body>")
    print("<h1>Node Resources Family</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
