#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_bottom_ticker_contract import build_visual_bottom_ticker_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_explainability_sidebar_contract import build_visual_explainability_sidebar_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_signal_overlay_contract import build_visual_signal_overlay_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_status_bar_contract import build_visual_status_bar_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_topology_overlay_contract import build_visual_topology_overlay_contract  # noqa: E402


def main() -> None:
    payload = {
        "visual_signal_overlay_contract": build_visual_signal_overlay_contract().total_entries,
        "visual_topology_overlay_contract": build_visual_topology_overlay_contract().total_entries,
        "visual_explainability_sidebar_contract": (
            build_visual_explainability_sidebar_contract().total_entries
        ),
        "visual_status_bar_contract": build_visual_status_bar_contract().status_bar_id,
        "visual_bottom_ticker_contract": build_visual_bottom_ticker_contract().bottom_ticker_id,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Visual Elements</title></head><body>")
    print("<h1>Visual Elements</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
