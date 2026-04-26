#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.chart_render_adapter_contract import (  # noqa: E402
    build_chart_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (  # noqa: E402
    build_graph_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.motion_render_adapter_contract import (  # noqa: E402
    build_motion_render_adapter_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.overlay_render_adapter_contract import (  # noqa: E402
    build_overlay_render_adapter_contract,
)


def main() -> None:
    graph_contract = build_graph_render_adapter_contract()
    chart_contract = build_chart_render_adapter_contract()
    overlay_contract = build_overlay_render_adapter_contract()
    motion_contract = build_motion_render_adapter_contract()

    print("RENDER ADAPTER BOUNDARY PREVIEW")
    print("=" * 180)
    print(
        f"graph_adapter_entries={graph_contract.total_entries} | "
        f"chart_adapter_entries={chart_contract.total_entries} | "
        f"overlay_adapter_entries={overlay_contract.total_entries} | "
        f"motion_adapter_entries={motion_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
