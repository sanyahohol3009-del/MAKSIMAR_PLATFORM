from __future__ import annotations

from dataclasses import asdict
from typing import Any

from MAKSIMAR_CORE_LIB.oob_dashboard.system_status_panel_content_contract import (
    build_system_status_panel_content_contract,
)


def build_system_status_panel_payload() -> dict[str, Any]:
    """Build canonical payload for the system-status panel."""
    contract = build_system_status_panel_content_contract()
    entry = contract.entries[0]

    return {
        "panel_id": entry.panel_id,
        "panel_state": entry.panel_state,
        "summary": {
            "total_foundation_panels": entry.total_foundation_panels,
            "alive_panels": entry.alive_panels,
            "degraded_panels": entry.degraded_panels,
            "broken_panels": entry.broken_panels,
            "warming_up_panels": entry.warming_up_panels,
        },
        "truth": {
            "truth_consistent_panels": entry.truth_consistent_panels,
            "truth_partial_panels": entry.truth_partial_panels,
            "truth_mismatch_panels": entry.truth_mismatch_panels,
        },
        "live_historical": {
            "historical_only_panels": entry.historical_only_panels,
            "current_live_visible_panels": entry.current_live_visible_panels,
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
