from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_contract import (
    build_panel_binding_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)


ViewId = Literal[
    "view_foundation_runtime",
    "view_foundation_guard",
    "view_foundation_core_guard",
    "view_foundation_kernel_guard",
    "view_consistency",
    "view_snapshot",
    "view_incident",
    "view_diagnostics",
    "view_chat",
    "view_settings",
    "view_gesture_control",
    "view_queue_load",
    "view_node_topology",
    "view_degraded_mode",
    "view_project_map",
    "view_data_flow",
    "view_dependency_map",
    "view_version_control",
    "view_navigation",
]

ViewTargetKind = Literal[
    "foundation_view",
    "diagnostics_view",
    "interaction_view",
    "execution_view",
    "navigation_view",
]


@dataclass(frozen=True, slots=True)
class ViewTargetingEntry:
    """Canonical view-targeting entry for one panel."""

    panel_id: str
    view_id: ViewId
    view_target_kind: ViewTargetKind
    view_scope: str
    description: str


@dataclass(frozen=True, slots=True)
class ViewTargetingContract:
    """Canonical view-targeting contract."""

    total_entries: int
    foundation_views: int
    diagnostics_views: int
    interaction_views: int
    execution_views: int
    navigation_views: int
    entries: tuple[ViewTargetingEntry, ...]


def build_view_targeting_contract() -> ViewTargetingContract:
    """Build canonical view-targeting contract."""
    panel_binding_contract = build_panel_binding_contract()
    metadata_contract = build_panel_metadata_contract()

    metadata_map = {entry.panel_id: entry for entry in metadata_contract.entries}

    view_id_map: dict[str, ViewId] = {
        "panel_foundation_runtime_status_001": "view_foundation_runtime",
        "panel_foundation_guard_status_001": "view_foundation_guard",
        "panel_foundation_core_guard_status_001": "view_foundation_core_guard",
        "panel_foundation_kernel_guard_status_001": "view_foundation_kernel_guard",
        "panel_consistency": "view_consistency",
        "panel_snapshot": "view_snapshot",
        "panel_incident": "view_incident",
        "panel_diagnostics": "view_diagnostics",
        "panel_chat": "view_chat",
        "panel_settings": "view_settings",
        "panel_gesture_control": "view_gesture_control",
        "panel_queue_load": "view_queue_load",
        "panel_node_topology": "view_node_topology",
        "panel_degraded_mode": "view_degraded_mode",
        "panel_project_map": "view_project_map",
        "panel_data_flow": "view_data_flow",
        "panel_dependency_map": "view_dependency_map",
        "panel_version_control_dashboard": "view_version_control",
        "panel_navigation": "view_navigation",
    }

    def resolve_view_target_kind(panel_id: str) -> ViewTargetKind:
        panel_family = metadata_map[panel_id].panel_family

        if panel_family == "foundation_status":
            return "foundation_view"
        if panel_family in ("diagnostics", "read_only_monitoring"):
            return "diagnostics_view"
        if panel_family in ("interaction", "control"):
            return "interaction_view"
        if panel_family == "execution_observability":
            return "execution_view"
        return "navigation_view"

    def resolve_view_scope(panel_id: str) -> str:
        return metadata_map[panel_id].source_domain

    entries = tuple(
        ViewTargetingEntry(
            panel_id=entry.panel_id,
            view_id=view_id_map[entry.panel_id],
            view_target_kind=resolve_view_target_kind(entry.panel_id),
            view_scope=resolve_view_scope(entry.panel_id),
            description=(
                f"Canonical view-targeting entry for {metadata_map[entry.panel_id].display_title}."
            ),
        )
        for entry in panel_binding_contract.entries
    )

    return ViewTargetingContract(
        total_entries=len(entries),
        foundation_views=sum(
            1 for entry in entries if entry.view_target_kind == "foundation_view"
        ),
        diagnostics_views=sum(
            1 for entry in entries if entry.view_target_kind == "diagnostics_view"
        ),
        interaction_views=sum(
            1 for entry in entries if entry.view_target_kind == "interaction_view"
        ),
        execution_views=sum(
            1 for entry in entries if entry.view_target_kind == "execution_view"
        ),
        navigation_views=sum(
            1 for entry in entries if entry.view_target_kind == "navigation_view"
        ),
        entries=entries,
    )
