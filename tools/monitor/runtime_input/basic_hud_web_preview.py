#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import build_visual_render_surface_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_renderer_contract import build_visual_renderer_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_shell_contract import build_visual_shell_contract  # noqa: E402
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import build_visual_theme_contract  # noqa: E402


def main() -> None:
    payload = {
        "visual_theme_contract": build_visual_theme_contract().theme_id,
        "visual_render_surface_contract": build_visual_render_surface_contract().total_entries,
        "visual_shell_contract": build_visual_shell_contract().shell_id,
        "visual_renderer_contract": build_visual_renderer_contract().renderer_id,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Basic HUD</title></head><body>")
    print("<h1>Basic HUD</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
