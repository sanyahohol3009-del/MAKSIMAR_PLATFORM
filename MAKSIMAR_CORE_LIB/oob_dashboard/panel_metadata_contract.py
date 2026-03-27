from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    build_panel_id_vocabulary_normalization_model,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_models import (
    PanelMetadataContract,
    PanelMetadataEntry,
)


def build_panel_metadata_contract() -> PanelMetadataContract:
    """Build canonical panel metadata contract."""
    vocabulary_model = build_panel_id_vocabulary_normalization_model()
    vocabulary_entries = {
        entry.canonical_panel_id: entry for entry in vocabulary_model.entries
    }

    panel_state_class_map = {
        "panel_consistency": "diagnostics",
        "panel_snapshot": "foundation",
        "panel_incident": "diagnostics",
        "panel_diagnostics": "diagnostics",
        "panel_chat": "operator",
        "panel_settings": "admin",
        "panel_gesture_control": "operator",
        "panel_queue_load": "topology",
        "panel_node_topology": "topology",
        "panel_degraded_mode": "diagnostics",
        "panel_project_map": "topology",
        "panel_data_flow": "topology",
        "panel_dependency_map": "topology",
        "panel_version_control_dashboard": "admin",
        "panel_foundation_runtime_status_001": "foundation",
        "panel_foundation_guard_status_001": "foundation",
        "panel_foundation_core_guard_status_001": "foundation",
        "panel_foundation_kernel_guard_status_001": "foundation",
        "panel_navigation": "operator",
    }

    read_mode_map = {
        "panel_consistency": "read_only",
        "panel_snapshot": "read_only",
        "panel_incident": "read_only",
        "panel_diagnostics": "read_only",
        "panel_chat": "interactive_controlled",
        "panel_settings": "interactive_restricted",
        "panel_gesture_control": "interactive_restricted",
        "panel_queue_load": "read_only",
        "panel_node_topology": "read_only",
        "panel_degraded_mode": "read_only",
        "panel_project_map": "read_only",
        "panel_data_flow": "read_only",
        "panel_dependency_map": "read_only",
        "panel_version_control_dashboard": "read_only",
        "panel_foundation_runtime_status_001": "read_only",
        "panel_foundation_guard_status_001": "read_only",
        "panel_foundation_core_guard_status_001": "read_only",
        "panel_foundation_kernel_guard_status_001": "read_only",
        "panel_navigation": "hidden_internal",
    }

    priority_map = {
        "panel_consistency": 30,
        "panel_snapshot": 20,
        "panel_incident": 10,
        "panel_diagnostics": 15,
        "panel_chat": 60,
        "panel_settings": 90,
        "panel_gesture_control": 80,
        "panel_queue_load": 40,
        "panel_node_topology": 35,
        "panel_degraded_mode": 12,
        "panel_project_map": 45,
        "panel_data_flow": 50,
        "panel_dependency_map": 55,
        "panel_version_control_dashboard": 95,
        "panel_foundation_runtime_status_001": 1,
        "panel_foundation_guard_status_001": 2,
        "panel_foundation_core_guard_status_001": 3,
        "panel_foundation_kernel_guard_status_001": 4,
        "panel_navigation": 100,
    }

    source_domain_map = {
        "panel_consistency": "diagnostics",
        "panel_snapshot": "foundation",
        "panel_incident": "diagnostics",
        "panel_diagnostics": "diagnostics",
        "panel_chat": "interaction",
        "panel_settings": "interaction",
        "panel_gesture_control": "control",
        "panel_queue_load": "execution_observability",
        "panel_node_topology": "execution_observability",
        "panel_degraded_mode": "diagnostics",
        "panel_project_map": "execution_observability",
        "panel_data_flow": "execution_observability",
        "panel_dependency_map": "execution_observability",
        "panel_version_control_dashboard": "execution_observability",
        "panel_foundation_runtime_status_001": "foundation",
        "panel_foundation_guard_status_001": "foundation",
        "panel_foundation_core_guard_status_001": "foundation",
        "panel_foundation_kernel_guard_status_001": "foundation",
        "panel_navigation": "navigation",
    }

    entries = tuple(
        PanelMetadataEntry(
            panel_id=entry.canonical_panel_id,
            display_title=entry.display_title,
            description=entry.description,
            priority=priority_map[entry.canonical_panel_id],
            source_domain=source_domain_map[entry.canonical_panel_id],
            read_mode=read_mode_map[entry.canonical_panel_id],
            panel_state_class=panel_state_class_map[entry.canonical_panel_id],
            panel_family=entry.panel_family,
            panel_kind=entry.panel_kind,
            panel_role=entry.panel_role,
        )
        for entry in vocabulary_entries.values()
    )

    return PanelMetadataContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_mode == "read_only"),
        interactive_controlled_entries=sum(
            1 for entry in entries if entry.read_mode == "interactive_controlled"
        ),
        interactive_restricted_entries=sum(
            1 for entry in entries if entry.read_mode == "interactive_restricted"
        ),
        hidden_internal_entries=sum(
            1 for entry in entries if entry.read_mode == "hidden_internal"
        ),
        entries=entries,
    )
