#!/usr/bin/env python3
from __future__ import annotations

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
    theme_contract = build_visual_theme_contract()
    render_surface_contract = build_visual_render_surface_contract()
    shell_contract = build_visual_shell_contract()
    renderer_contract = build_visual_renderer_contract()

    print("BASIC HUD PREVIEW")
    print("=" * 180)
    print(
        f"visual_theme_id={theme_contract.theme_id} | "
        f"visual_render_surface_entries={render_surface_contract.total_entries} | "
        f"visual_shell_id={shell_contract.shell_id} | "
        f"visual_renderer_id={renderer_contract.renderer_id}"
    )


if __name__ == "__main__":
    main()
