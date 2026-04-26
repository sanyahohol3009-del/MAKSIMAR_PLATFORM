#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_capability_matrix_contract import (  # noqa: E402
    build_visual_capability_matrix_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_degraded_mode_capability_contract import (  # noqa: E402
    build_visual_degraded_mode_capability_contract,
)


def main() -> None:
    capability_contract = build_visual_capability_matrix_contract()
    degraded_contract = build_visual_degraded_mode_capability_contract()

    print("VISUAL CAPABILITY MATRIX PREVIEW")
    print("=" * 180)
    print(
        f"capability_entries={capability_contract.total_entries} | "
        f"swap_safe_entries={capability_contract.swap_safe_entries} | "
        f"degraded_entries={degraded_contract.total_entries} | "
        f"readable_degraded_entries={degraded_contract.readable_operator_state_preserved_entries}"
    )


if __name__ == "__main__":
    main()
