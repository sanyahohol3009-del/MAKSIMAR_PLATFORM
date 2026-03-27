from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_models import (
    PanelMetadataEntry,
)


SourceBindingKind = Literal[
    "foundation_live_status_adapter",
    "foundation_status_summary_contract",
    "foundation_incident_view",
    "foundation_diagnostics_correlation_view",
    "gesture_panel_contract",
    "dashboard_navigation_contract",
    "dashboard_chat_contract",
    "dashboard_settings_panel",
    "execution_panel_contract",
]


@dataclass(frozen=True, slots=True)
class PanelSourceBindingEntry:
    """Canonical source binding entry for one panel."""

    panel_id: str
    source_binding: SourceBindingKind
    source_contract_name: str
    source_scope: str
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class PanelSourceBindingContract:
    """Canonical source binding contract for normalized panels."""

    total_entries: int
    read_only_entries: int
    mutable_entries: int
    entries: tuple[PanelSourceBindingEntry, ...]
    metadata_entries: tuple[PanelMetadataEntry, ...]


def build_panel_source_binding_contract() -> PanelSourceBindingContract:
    """Build canonical source binding contract."""
    metadata_contract = build_panel_metadata_contract()
    metadata_entries = metadata_contract.entries

    binding_map: dict[str, tuple[SourceBindingKind, str, str, bool, str]] = {
        "panel_consistency": (
            "foundation_diagnostics_correlation_view",
            "foundation_diagnostics_correlation_view",
            "diagnostics",
            True,
            "Consistency panel reads canonical diagnostics correlation output.",
        ),
        "panel_snapshot": (
            "foundation_live_status_adapter",
            "foundation_live_status_adapter",
            "foundation",
            True,
            "Snapshot panel reads canonical live foundation status adapter output.",
        ),
        "panel_incident": (
            "foundation_incident_view",
            "foundation_incident_failure_localization_view",
            "diagnostics",
            True,
            "Incident panel reads canonical incident failure localization view.",
        ),
        "panel_diagnostics": (
            "foundation_diagnostics_correlation_view",
            "foundation_diagnostics_correlation_view",
            "diagnostics",
            True,
            "Diagnostics panel reads canonical diagnostics correlation view.",
        ),
        "panel_chat": (
            "dashboard_chat_contract",
            "build_dashboard_chat_contract",
            "interaction",
            False,
            "Chat panel reads dashboard chat contract and supports controlled interaction.",
        ),
        "panel_settings": (
            "dashboard_settings_panel",
            "build_dashboard_settings_panel",
            "interaction",
            False,
            "Settings panel reads canonical dashboard settings contract.",
        ),
        "panel_gesture_control": (
            "gesture_panel_contract",
            "build_dashboard_gesture_panel",
            "control",
            False,
            "Gesture panel reads canonical gesture panel contract.",
        ),
        "panel_queue_load": (
            "execution_panel_contract",
            "build_queue_load_panel_contract",
            "execution_observability",
            True,
            "Queue/load panel reads canonical execution panel contract.",
        ),
        "panel_node_topology": (
            "execution_panel_contract",
            "build_node_topology_panel_contract",
            "execution_observability",
            True,
            "Node topology panel reads canonical node topology contract.",
        ),
        "panel_degraded_mode": (
            "execution_panel_contract",
            "build_degraded_mode_panel_contract",
            "execution_observability",
            True,
            "Degraded mode panel reads canonical degraded mode contract.",
        ),
        "panel_project_map": (
            "execution_panel_contract",
            "build_project_map_panel_contract",
            "execution_observability",
            True,
            "Project map panel reads canonical project map contract.",
        ),
        "panel_data_flow": (
            "execution_panel_contract",
            "build_data_flow_panel_contract",
            "execution_observability",
            True,
            "Data flow panel reads canonical data flow contract.",
        ),
        "panel_dependency_map": (
            "execution_panel_contract",
            "build_dependency_map_panel_contract",
            "execution_observability",
            True,
            "Dependency map panel reads canonical dependency map contract.",
        ),
        "panel_version_control_dashboard": (
            "execution_panel_contract",
            "build_version_control_panel_contract",
            "execution_observability",
            True,
            "Version control dashboard reads canonical version control contract.",
        ),
        "panel_foundation_runtime_status_001": (
            "foundation_status_summary_contract",
            "build_foundation_status_panel_summary_contract",
            "foundation",
            True,
            "Foundation runtime panel reads canonical foundation status summary contract.",
        ),
        "panel_foundation_guard_status_001": (
            "foundation_status_summary_contract",
            "build_foundation_status_panel_summary_contract",
            "foundation",
            True,
            "Foundation guard panel reads canonical foundation status summary contract.",
        ),
        "panel_foundation_core_guard_status_001": (
            "foundation_status_summary_contract",
            "build_foundation_status_panel_summary_contract",
            "foundation",
            True,
            "Foundation core guard panel reads canonical foundation status summary contract.",
        ),
        "panel_foundation_kernel_guard_status_001": (
            "foundation_status_summary_contract",
            "build_foundation_status_panel_summary_contract",
            "foundation",
            True,
            "Foundation kernel guard panel reads canonical foundation status summary contract.",
        ),
        "panel_navigation": (
            "dashboard_navigation_contract",
            "build_dashboard_navigation_contract",
            "navigation",
            True,
            "Navigation panel reads canonical dashboard navigation contract.",
        ),
    }

    entries = tuple(
        PanelSourceBindingEntry(
            panel_id=entry.panel_id,
            source_binding=binding_map[entry.panel_id][0],
            source_contract_name=binding_map[entry.panel_id][1],
            source_scope=binding_map[entry.panel_id][2],
            read_only=binding_map[entry.panel_id][3],
            description=binding_map[entry.panel_id][4],
        )
        for entry in metadata_entries
    )

    return PanelSourceBindingContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        mutable_entries=sum(1 for entry in entries if not entry.read_only),
        entries=entries,
        metadata_entries=metadata_entries,
    )
