#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_placement_restore_contract import (  # noqa: E402
    build_panel_placement_restore_contract,
)


def main() -> None:
    contract = build_panel_placement_restore_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "ready_entries": contract.ready_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "truth_bound_entries": contract.truth_bound_entries,
        "entries": [
            {
                "panel_placement_restore_id": entry.panel_placement_restore_id,
                "workspace_id": entry.workspace_id,
                "panel_placement_restore_state": entry.panel_placement_restore_state,
                "panel_placement_restore_class": entry.panel_placement_restore_class,
                "dashboard_session_restore_ready": entry.dashboard_session_restore_ready,
                "display_assignment_restore_ready": entry.display_assignment_restore_ready,
                "operator_visible": entry.operator_visible,
                "truth_bound": entry.truth_bound,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Panel Placement Restore</title></head><body>")
    print("<h1>Panel Placement Restore</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
