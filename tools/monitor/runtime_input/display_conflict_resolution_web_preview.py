#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.display_conflict_resolution_contract import (  # noqa: E402
    build_display_conflict_resolution_contract,
)


def main() -> None:
    contract = build_display_conflict_resolution_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "pinned_conflict_entries": contract.pinned_conflict_entries,
        "replaceable_conflict_entries": contract.replaceable_conflict_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "entries": [
            {
                "conflict_id": entry.conflict_id,
                "display_target_id": entry.display_target_id,
                "conflict_decision": entry.conflict_decision,
                "conflict_class": entry.conflict_class,
                "incumbent_assignment_id": entry.incumbent_assignment_id,
                "candidate_display_target_id": entry.candidate_display_target_id,
                "operator_visible": entry.operator_visible,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Display Conflict Resolution</title></head><body>")
    print("<h1>Display Conflict Resolution</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
