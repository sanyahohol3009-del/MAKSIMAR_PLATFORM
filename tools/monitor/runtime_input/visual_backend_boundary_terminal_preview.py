#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_contract import (  # noqa: E402
    build_visual_backend_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_chart_backend_contract import (  # noqa: E402
    build_visual_chart_backend_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_graph_backend_contract import (  # noqa: E402
    build_visual_graph_backend_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_overlay_backend_contract import (  # noqa: E402
    build_visual_overlay_backend_contract,
)


def main() -> None:
    backend_contract = build_visual_backend_contract()
    graph_contract = build_visual_graph_backend_contract()
    chart_contract = build_visual_chart_backend_contract()
    overlay_contract = build_visual_overlay_backend_contract()

    print("VISUAL BACKEND BOUNDARY PREVIEW")
    print("=" * 180)
    print(
        f"visual_backend_entries={backend_contract.total_entries} | "
        f"graph_backend={graph_contract.graph_backend_name} | "
        f"chart_backend={chart_contract.chart_backend_name} | "
        f"overlay_backend={overlay_contract.overlay_backend_name}"
    )


if __name__ == "__main__":
    main()
