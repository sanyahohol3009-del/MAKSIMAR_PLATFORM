#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_composition_contract import build_visual_hud_composition_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_contract import build_visual_hud_preview_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_snapshot_contract import build_visual_hud_snapshot_contract  # noqa: E402


def main() -> None:
    payload = {
        "visual_hud_composition_contract": (
            build_visual_hud_composition_contract().composition_id
        ),
        "visual_hud_snapshot_contract": (
            build_visual_hud_snapshot_contract().snapshot_id
        ),
        "visual_hud_preview_contract": (
            build_visual_hud_preview_contract().preview_id
        ),
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Visual HUD</title></head><body>")
    print("<h1>Visual HUD</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
