from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views.memory_registry_panel_models import (
    MemoryRegistryPanelContract,
    MemoryRegistryPanelEntry,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views.memory_registry_summary_builder import (
    build_memory_registry_view_summary,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views.memory_registry_view_models import (
    MemoryRegistryViewContract,
    MemoryRegistryViewEntry,
)


def build_memory_registry_panel_contract() -> MemoryRegistryPanelContract:
    summary = build_memory_registry_view_summary()

    panels = (
        MemoryRegistryPanelEntry(
            panel_id="panel_memory_domain_map",
            panel_kind="memory_domain_map",
            title="Memory Domain Map",
            source_component="MEMORY_REGISTRY",
            source_entries=int(summary["memory_registry_total_entries"]),
            visible_entries=int(summary["memory_registry_active_entries"]),
            read_only=True,
            action_exposure_allowed=False,
            display_orchestration_allowed=False,
            status="ready",
        ),
        MemoryRegistryPanelEntry(
            panel_id="panel_memory_registry_graph",
            panel_kind="memory_registry_graph",
            title="Memory Registry Graph",
            source_component="GLOBAL_REGISTRY",
            source_entries=int(summary["global_registry_total_entries"]),
            visible_entries=int(summary["global_registry_dashboard_visible_entries"]),
            read_only=True,
            action_exposure_allowed=False,
            display_orchestration_allowed=False,
            status="ready",
        ),
        MemoryRegistryPanelEntry(
            panel_id="panel_memory_timeline",
            panel_kind="memory_timeline",
            title="Memory Timeline",
            source_component="HISTORY_BINDING",
            source_entries=int(summary["memory_registry_total_entries"]),
            visible_entries=int(summary["memory_registry_active_entries"]),
            read_only=True,
            action_exposure_allowed=False,
            display_orchestration_allowed=False,
            status="ready",
        ),
        MemoryRegistryPanelEntry(
            panel_id="panel_memory_retrieval_trace",
            panel_kind="retrieval_trace",
            title="Retrieval Trace",
            source_component="CONTROL_PLANE_MEMORY_ROUTING",
            source_entries=int(summary["retrieval_evidence_item_count"]),
            visible_entries=int(summary["retrieval_selected_source_count"]),
            read_only=True,
            action_exposure_allowed=False,
            display_orchestration_allowed=False,
            status="ready",
        ),
        MemoryRegistryPanelEntry(
            panel_id="panel_memory_storage_map",
            panel_kind="storage_map",
            title="Storage Map",
            source_component="STORAGE_REGISTRY",
            source_entries=int(summary["storage_total_entries"]),
            visible_entries=int(summary["storage_dashboard_visible_entries"]),
            read_only=True,
            action_exposure_allowed=False,
            display_orchestration_allowed=False,
            status="ready",
        ),
        MemoryRegistryPanelEntry(
            panel_id="panel_memory_media_artifact_flow",
            panel_kind="media_artifact_flow",
            title="Media Artifact Flow",
            source_component="MEDIA_MEMORY",
            source_entries=int(summary["media_total_records"]),
            visible_entries=int(summary["media_dashboard_visible_records"]),
            read_only=True,
            action_exposure_allowed=False,
            display_orchestration_allowed=False,
            status="ready",
        ),
        MemoryRegistryPanelEntry(
            panel_id="panel_memory_model_store_status",
            panel_kind="model_store_status",
            title="Model Store Status",
            source_component="MEDIA_MEMORY_MODEL_STORE",
            source_entries=int(summary["media_total_records"]),
            visible_entries=1,
            read_only=True,
            action_exposure_allowed=False,
            display_orchestration_allowed=False,
            status="ready",
        ),
        MemoryRegistryPanelEntry(
            panel_id="panel_memory_history_flow",
            panel_kind="history_flow",
            title="History Flow",
            source_component="HISTORY_BINDING",
            source_entries=int(summary["memory_registry_total_entries"]),
            visible_entries=int(summary["memory_registry_active_entries"]),
            read_only=True,
            action_exposure_allowed=False,
            display_orchestration_allowed=False,
            status="ready",
        ),
    )

    return MemoryRegistryPanelContract(
        total_panels=len(panels),
        ready_panels=sum(1 for panel in panels if panel.status == "ready"),
        read_only_panels=sum(1 for panel in panels if panel.read_only),
        action_exposure_allowed_panels=sum(
            1 for panel in panels if panel.action_exposure_allowed
        ),
        display_orchestration_allowed_panels=sum(
            1 for panel in panels if panel.display_orchestration_allowed
        ),
        entries=panels,
    )


def build_memory_registry_view_contract() -> MemoryRegistryViewContract:
    panels = build_memory_registry_panel_contract()

    entries = tuple(
        MemoryRegistryViewEntry(
            view_id=f"view_{panel.panel_id.removeprefix('panel_')}",
            panel_id=panel.panel_id,
            source_component=panel.source_component,
            source_ref=f"read_only://{panel.source_component.lower()}",
            visible_count=panel.visible_entries,
            read_only=True,
            preview_ready=True,
            dashboard_visible=True,
        )
        for panel in panels.entries
    )

    return MemoryRegistryViewContract(
        total_views=len(entries),
        read_only_views=sum(1 for entry in entries if entry.read_only),
        preview_ready_views=sum(1 for entry in entries if entry.preview_ready),
        dashboard_visible_views=sum(1 for entry in entries if entry.dashboard_visible),
        entries=entries,
    )
