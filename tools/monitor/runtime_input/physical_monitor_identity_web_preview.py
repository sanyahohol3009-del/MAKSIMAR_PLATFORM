#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from MAKSIMAR_CORE_LIB.oob_dashboard.physical_monitor_identity_contract import (  # noqa: E402
    build_physical_monitor_identity_contract,
)


def main() -> None:
    contract = build_physical_monitor_identity_contract()

    payload = {
        "contract_id": contract.contract_id,
        "total_entries": contract.total_entries,
        "hotplug_detectable_entries": contract.hotplug_detectable_entries,
        "operator_visible_entries": contract.operator_visible_entries,
        "entries": [
            {
                "physical_monitor_id": entry.physical_monitor_id,
                "display_target_id": entry.display_target_id,
                "monitor_inventory_id": entry.monitor_inventory_id,
                "identity_state": entry.identity_state,
                "identity_class": entry.identity_class,
                "physical_slot_label": entry.physical_slot_label,
                "hotplug_detectable": entry.hotplug_detectable,
                "multi_monitor_capable": entry.multi_monitor_capable,
                "operator_visible": entry.operator_visible,
                "description": entry.description,
            }
            for entry in contract.entries
        ],
    }

    pretty = html.escape(json.dumps(payload, indent=2))

    print("<!doctype html>")
    print("<html><head><meta charset='utf-8'><title>Physical Monitor Identity</title></head><body>")
    print("<h1>Physical Monitor Identity</h1>")
    print(f"<p><strong>contract_id:</strong> {html.escape(contract.contract_id)}</p>")
    print("<pre>")
    print(pretty)
    print("</pre>")
    print("</body></html>")


if __name__ == "__main__":
    main()
