#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.owner_review_package_contract import (  # noqa: E402
    build_owner_review_package_contract,
)


def main() -> None:
    contract = build_owner_review_package_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "read_only_review_entries": contract.read_only_review_entries,
        "approval_bound_review_entries": contract.approval_bound_review_entries,
        "audit_visible_entries": contract.audit_visible_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "entries": [
            {
                "owner_review_package_id": entry.owner_review_package_id,
                "operator_intent_id": entry.operator_intent_id,
                "panel_id": entry.panel_id,
                "workspace_id": entry.workspace_id,
                "owner_review_package_state": entry.owner_review_package_state,
                "owner_review_package_class": entry.owner_review_package_class,
                "owner_review_evidence_mode": entry.owner_review_evidence_mode,
                "approval_required": entry.approval_required,
                "handoff_ready": entry.handoff_ready,
                "audit_visible": entry.audit_visible,
                "operator_visible": entry.operator_visible,
                "trace_id": entry.trace_id,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Owner Review Package</title></head><body>")
    print("<h1>Owner Review Package</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
