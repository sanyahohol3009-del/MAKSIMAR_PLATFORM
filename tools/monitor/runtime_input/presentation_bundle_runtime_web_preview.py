#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.presentation_bundle_runtime_contract import (  # noqa: E402
    build_presentation_bundle_runtime_contract,
)


def main() -> None:
    contract = build_presentation_bundle_runtime_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "foundation_runtime_entries": contract.foundation_runtime_entries,
        "interaction_runtime_entries": contract.interaction_runtime_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "truth_bound_entries": contract.truth_bound_entries,
        "entries": [
            {
                "presentation_bundle_runtime_id": entry.presentation_bundle_runtime_id,
                "display_target_id": entry.display_target_id,
                "workspace_id": entry.workspace_id,
                "presentation_bundle_runtime_state": entry.presentation_bundle_runtime_state,
                "presentation_bundle_runtime_class": entry.presentation_bundle_runtime_class,
                "presentation_bundle_runtime_mode": entry.presentation_bundle_runtime_mode,
                "visible_state_ready": entry.visible_state_ready,
                "operator_visible": entry.operator_visible,
                "truth_bound": entry.truth_bound,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Presentation Bundle Runtime</title></head><body>")
    print("<h1>Presentation Bundle Runtime</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
