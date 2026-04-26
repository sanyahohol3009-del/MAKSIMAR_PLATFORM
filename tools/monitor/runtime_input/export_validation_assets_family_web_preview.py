#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.export_status_panel_contract import (  # noqa: E402
    build_export_status_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.project_assets_panel_contract import (  # noqa: E402
    build_project_assets_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.validation_assets_panel_contract import (  # noqa: E402
    build_validation_assets_panel_contract,
)


def main() -> None:
    payload = {
        "export_status_panel_contract": build_export_status_panel_contract().total_entries,
        "validation_assets_panel_contract": build_validation_assets_panel_contract().total_entries,
        "project_assets_panel_contract": build_project_assets_panel_contract().total_entries,
    }

    pretty = html.escape(json.dumps(payload, indent=2))
    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Export Validation Assets Family</title></head><body>")
    print("<h1>Export / Validation / Assets Family</h1>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
