from __future__ import annotations

from dataclasses import asdict
from typing import Any

from MAKSIMAR_CORE_LIB.oob_dashboard.logs_panel_content_contract import (
    build_logs_panel_content_contract,
)


def build_logs_panel_payload() -> dict[str, Any]:
    """Build canonical payload for the logs panel."""
    contract = build_logs_panel_content_contract()
    entry = contract.entries[0]

    return {
        "panel_id": entry.panel_id,
        "panel_state": entry.panel_state,
        "summary": {
            "total_log_related_entries": entry.total_log_related_entries,
            "failure_visible_entries": entry.failure_visible_entries,
            "incident_visible_entries": entry.incident_visible_entries,
            "stalled_stage_visible_entries": entry.stalled_stage_visible_entries,
        },
        "severity": {
            "critical_entries": entry.critical_entries,
            "warning_entries": entry.warning_entries,
            "info_entries": entry.info_entries,
        },
        "visibility": {
            "source_file_visible_entries": entry.source_file_visible_entries,
            "visible_in_main_dashboard": entry.visible_in_main_dashboard,
            "visible_in_oob_dashboard": entry.visible_in_oob_dashboard,
            "read_only": entry.read_only,
            "operator_visible": entry.operator_visible,
        },
        "description": entry.description,
        "raw_entry": asdict(entry),
    }
