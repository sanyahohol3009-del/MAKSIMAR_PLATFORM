#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.free_display_selection_contract import (  # noqa: E402
    build_free_display_selection_contract,
)


def main() -> None:
    contract = build_free_display_selection_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "no_free_display_entries": contract.no_free_display_entries,
        "replaceable_candidate_entries": contract.replaceable_candidate_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "entries": [
            {
                "selection_id": entry.selection_id,
                "requested_role_hint": entry.requested_role_hint,
                "selection_decision": entry.selection_decision,
                "selection_reason": entry.selection_reason,
                "candidate_display_target_id": entry.candidate_display_target_id,
                "operator_visible": entry.operator_visible,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Free Display Selection</title></head><body>")
    print("<h1>Free Display Selection</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
