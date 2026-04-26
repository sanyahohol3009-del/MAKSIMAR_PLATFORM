from __future__ import annotations

from dataclasses import asdict
from typing import Any

from MAKSIMAR_CORE_LIB.oob_dashboard.incidents_panel_content_contract import (
    build_incidents_panel_content_contract,
)


def build_incidents_panel_payload() -> dict[str, Any]:
    """Build canonical payload for the incidents panel."""
    contract = build_incidents_panel_content_contract()
    entry = contract.entries[0]

    return {
        "panel_id": entry.panel_id,
        "panel_state": entry.panel_state,
        "summary": {
            "total_incident_entries": entry.total_incident_entries,
            "active_incident_entries": entry.active_incident_entries,
            "history_visible_entries": entry.history_visible_entries,
            "kill_chain_triggered_entries": entry.kill_chain_triggered_entries,
        },
        "severity": {
            "critical_entries": entry.critical_entries,
            "warning_entries": entry.warning_entries,
            "info_entries": entry.info_entries,
        },
        "lifecycle": {
            "archived_entries": entry.archived_entries,
            "recovered_entries": entry.recovered_entries,
        },
        "visibility": {
            "visible_in_main_dashboard": entry.visible_in_main_dashboard,
            "visible_in_oob_dashboard": entry.visible_in_oob_dashboard,
            "read_only": entry.read_only,
            "operator_visible": entry.operator_visible,
        },
        "description": entry.description,
        "raw_entry": asdict(entry),
    }
