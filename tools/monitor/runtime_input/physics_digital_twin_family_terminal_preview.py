#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.digital_twin_panel_contract import (  # noqa: E402
    build_digital_twin_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.physics_status_panel_contract import (  # noqa: E402
    build_physics_status_panel_contract,
)


def main() -> None:
    physics_status_contract = build_physics_status_panel_contract()
    digital_twin_contract = build_digital_twin_panel_contract()

    print("PHYSICS / DIGITAL TWIN FAMILY PREVIEW")
    print("=" * 180)
    print(
        f"physics_status_entries={physics_status_contract.total_entries} | "
        f"digital_twin_entries={digital_twin_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
