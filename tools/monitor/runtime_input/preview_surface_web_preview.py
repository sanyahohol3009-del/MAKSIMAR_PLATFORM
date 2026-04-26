#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_contract import (  # noqa: E402
    build_preview_surface_contract,
)


def main() -> None:
    contract = build_preview_surface_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "foundation_preview_entries": contract.foundation_preview_entries,
        "interaction_preview_entries": contract.interaction_preview_entries,
        "panel_preview_generation_entries": contract.panel_preview_generation_entries,
        "fixture_preview_generation_entries": contract.fixture_preview_generation_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "entries": [
            {
                "preview_surface_id": entry.preview_surface_id,
                "panel_id": entry.panel_id,
                "workspace_id": entry.workspace_id,
                "preview_surface_state": entry.preview_surface_state,
                "preview_surface_class": entry.preview_surface_class,
                "preview_generation_mode": entry.preview_generation_mode,
                "visible_in_navigation": entry.visible_in_navigation,
                "visible_in_main_dashboard": entry.visible_in_main_dashboard,
                "operator_visible": entry.operator_visible,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Preview Surface</title></head><body>")
    print("<h1>Preview Surface</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
