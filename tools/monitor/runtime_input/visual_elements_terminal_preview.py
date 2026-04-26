#!/usr/bin/env python3
from __future__ import annotations

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
    signal_overlay_contract = build_visual_signal_overlay_contract()
    topology_overlay_contract = build_visual_topology_overlay_contract()
    explainability_sidebar_contract = build_visual_explainability_sidebar_contract()
    status_bar_contract = build_visual_status_bar_contract()
    bottom_ticker_contract = build_visual_bottom_ticker_contract()

    print("VISUAL ELEMENTS PREVIEW")
    print("=" * 180)
    print(
        f"visual_signal_overlay_entries={signal_overlay_contract.total_entries} | "
        f"visual_topology_overlay_entries={topology_overlay_contract.total_entries} | "
        f"visual_explainability_sidebar_entries={explainability_sidebar_contract.total_entries} | "
        f"visual_status_bar_id={status_bar_contract.status_bar_id} | "
        f"visual_bottom_ticker_id={bottom_ticker_contract.bottom_ticker_id}"
    )


if __name__ == "__main__":
    main()
