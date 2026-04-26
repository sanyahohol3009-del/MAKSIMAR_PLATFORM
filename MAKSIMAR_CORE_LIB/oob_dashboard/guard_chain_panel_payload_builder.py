from __future__ import annotations

from dataclasses import asdict
from typing import Any

from MAKSIMAR_CORE_LIB.oob_dashboard.guard_chain_panel_content_contract import (
    build_guard_chain_panel_content_contract,
)


def build_guard_chain_panel_payload() -> dict[str, Any]:
    """Build canonical payload for the guard-chain panel."""
    contract = build_guard_chain_panel_content_contract()
    entry = contract.entries[0]

    return {
        "panel_id": entry.panel_id,
        "panel_state": entry.panel_state,
        "summary": {
            "total_chain_entries": entry.total_chain_entries,
            "consistent_chain_entries": entry.consistent_chain_entries,
            "partial_chain_entries": entry.partial_chain_entries,
            "mismatch_chain_entries": entry.mismatch_chain_entries,
            "unknown_chain_entries": entry.unknown_chain_entries,
        },
        "chain_health": {
            "alive_chain_entries": entry.alive_chain_entries,
            "degraded_chain_entries": entry.degraded_chain_entries,
            "dead_chain_entries": entry.dead_chain_entries,
            "broken_chain_entries": entry.broken_chain_entries,
        },
        "presence": {
            "runtime_entry_present": entry.runtime_entry_present,
            "guard_entry_present": entry.guard_entry_present,
            "core_guard_entry_present": entry.core_guard_entry_present,
            "kernel_guard_entry_present": entry.kernel_guard_entry_present,
        },
        "state_context": {
            "warming_up_panels": entry.warming_up_panels,
            "historical_only_panels": entry.historical_only_panels,
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
