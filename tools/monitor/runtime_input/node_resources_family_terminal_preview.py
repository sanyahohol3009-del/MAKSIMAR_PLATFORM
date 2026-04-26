#!/usr/bin/env python3
from __future__ import annotations

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
    queue_load_contract = build_queue_load_panel_contract()
    degraded_mode_contract = build_degraded_mode_panel_contract()
    project_map_contract = build_project_map_panel_contract()
    version_control_contract = build_version_control_panel_contract()

    print("NODE RESOURCES FAMILY PREVIEW")
    print("=" * 180)
    print(
        f"queue_load_entries={queue_load_contract.total_entries} | "
        f"degraded_mode_entries={degraded_mode_contract.total_entries} | "
        f"project_map_entries={project_map_contract.total_entries} | "
        f"version_control_entries={version_control_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
