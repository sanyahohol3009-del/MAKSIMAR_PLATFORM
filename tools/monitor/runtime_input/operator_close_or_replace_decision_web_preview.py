#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_close_or_replace_decision_contract import (  # noqa: E402
    build_operator_close_or_replace_decision_contract,
)


def main() -> None:
    contract = build_operator_close_or_replace_decision_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "retain_entries": contract.retain_entries,
        "replace_entries": contract.replace_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "entries": [
            {
                "decision_id": entry.decision_id,
                "display_target_id": entry.display_target_id,
                "logical_target_id": entry.logical_target_id,
                "decision_state": entry.decision_state,
                "decision_class": entry.decision_class,
                "decision_action": entry.decision_action,
                "candidate_display_target_id": entry.candidate_display_target_id,
                "operator_visible": entry.operator_visible,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Operator Close Or Replace Decision</title></head><body>")
    print("<h1>Operator Close Or Replace Decision</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
