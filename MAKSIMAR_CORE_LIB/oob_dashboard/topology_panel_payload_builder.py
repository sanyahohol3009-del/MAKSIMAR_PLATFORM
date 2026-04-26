from __future__ import annotations

from dataclasses import asdict
from typing import Any

from MAKSIMAR_CORE_LIB.oob_dashboard.topology_panel_content_contract import (
    build_topology_panel_content_contract,
)


def build_topology_panel_payload() -> dict[str, Any]:
    """Build canonical payload for the topology panel."""
    contract = build_topology_panel_content_contract()
    entry = contract.entries[0]

    return {
        "panel_id": entry.panel_id,
        "panel_state": entry.panel_state,
        "nodes": {
            "total_topology_entries": entry.total_topology_entries,
            "runtime_nodes": entry.runtime_nodes,
            "guard_nodes": entry.guard_nodes,
            "core_guard_nodes": entry.core_guard_nodes,
            "kernel_guard_nodes": entry.kernel_guard_nodes,
        },
        "relationships": {
            "topology_relationships": entry.topology_relationships,
            "startup_order_valid": entry.startup_order_valid,
        },
        "health": {
            "alive_nodes": entry.alive_nodes,
            "degraded_nodes": entry.degraded_nodes,
            "broken_nodes": entry.broken_nodes,
            "dead_nodes": entry.dead_nodes,
        },
        "truth": {
            "truth_consistent_nodes": entry.truth_consistent_nodes,
            "truth_partial_nodes": entry.truth_partial_nodes,
            "truth_mismatch_nodes": entry.truth_mismatch_nodes,
        },
        "live_historical": {
            "historical_only_nodes": entry.historical_only_nodes,
            "current_live_visible_nodes": entry.current_live_visible_nodes,
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
