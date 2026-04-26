#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.final_visible_screen_state_contract import (  # noqa: E402
    build_final_visible_screen_state_contract,
)


def main() -> None:
    contract = build_final_visible_screen_state_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "ready_entries": contract.ready_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "truth_bound_entries": contract.truth_bound_entries,
        "entries": [
            {
                "final_visible_screen_state_id": entry.final_visible_screen_state_id,
                "display_target_id": entry.display_target_id,
                "workspace_id": entry.workspace_id,
                "final_visible_screen_state": entry.final_visible_screen_state,
                "final_visible_screen_state_class": entry.final_visible_screen_state_class,
                "presentation_bundle_ready": entry.presentation_bundle_ready,
                "rollback_readiness_ready": entry.rollback_readiness_ready,
                "operator_visible": entry.operator_visible,
                "truth_bound": entry.truth_bound,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Final Visible Screen State</title></head><body>")
    print("<h1>Final Visible Screen State</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
