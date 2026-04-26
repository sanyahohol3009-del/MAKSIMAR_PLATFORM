#!/usr/bin/env python3
from __future__ import annotations

import html
import json
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
    payload = {
        "visual_shell_canonical_panel_contract": (
            build_visual_shell_canonical_panel_contract().total_entries
        ),
        "panel_to_visual_mapping_contract": (
            build_panel_to_visual_mapping_contract().total_entries
        ),
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Visual Mapping</title></head><body>")
    print("<h1>Visual Mapping</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
