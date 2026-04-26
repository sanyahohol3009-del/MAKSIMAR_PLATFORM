#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (  # noqa: E402
    build_panel_to_visual_mapping_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_canonical_panel_contract import (  # noqa: E402
    build_visual_shell_canonical_panel_contract,
)


def main() -> None:
    visual_shell_contract = build_visual_shell_canonical_panel_contract()
    mapping_contract = build_panel_to_visual_mapping_contract()

    print("VISUAL MAPPING PREVIEW")
    print("=" * 180)
    print(
        f"visual_shell_canonical_panel_entries={visual_shell_contract.total_entries} | "
        f"panel_to_visual_mapping_entries={mapping_contract.total_entries}"
    )


if __name__ == "__main__":
    main()
