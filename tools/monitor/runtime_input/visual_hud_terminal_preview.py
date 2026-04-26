#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_composition_contract import build_visual_hud_composition_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_contract import build_visual_hud_preview_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_snapshot_contract import build_visual_hud_snapshot_contract  # noqa: E402


def main() -> None:
    composition_contract = build_visual_hud_composition_contract()
    snapshot_contract = build_visual_hud_snapshot_contract()
    preview_contract = build_visual_hud_preview_contract()

    print("VISUAL HUD PREVIEW")
    print("=" * 180)
    print(
        f"visual_hud_composition_id={composition_contract.composition_id} | "
        f"visual_hud_snapshot_id={snapshot_contract.snapshot_id} | "
        f"visual_hud_preview_id={preview_contract.preview_id}"
    )


if __name__ == "__main__":
    main()
