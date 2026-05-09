from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.dashboard_read_only_views_models import (
    DashboardReadOnlyViewEntry,
    DashboardReadOnlyViewsContract,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_view_binding_contract,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_memory_registry_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics import (
    build_memory_skill_metrics_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.presentation_display_metrics import (
    build_presentation_display_metrics_contract,
)
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import (
    build_skill_adapter_registry_contract,
)


def _build_root_memory_skill_entries() -> tuple[DashboardReadOnlyViewEntry, ...]:
    memory_registry = build_memory_registry_contract()
    skill_registry = build_skill_adapter_registry_contract()
    memory_skill_metrics = build_memory_skill_metrics_contract()
    presentation_metrics = build_presentation_display_metrics_contract()
    explainable_binding = build_explainable_view_binding_contract()

    memory_entry = memory_registry.entries[0]
    skill_entry = skill_registry.entries[0]

    metric_by_source = {
        entry.source_component: entry
        for entry in memory_skill_metrics.entries
        if entry.source_component in ("memory_registry", "skill_adapter_registry")
    }
    presentation_by_view_id = {
        entry.view_id: entry for entry in presentation_metrics.entries
    }
    explainable_by_view_id = {
        entry.view_id: entry for entry in explainable_binding.entries
    }

    memory_metric = metric_by_source["memory_registry"]
    skill_metric = metric_by_source["skill_adapter_registry"]

    memory_presentation = presentation_by_view_id["view_memory_project_architecture"]
    skill_presentation = presentation_by_view_id["view_simulation_skill_overview"]

    memory_explainable = explainable_by_view_id["view_memory_project_architecture"]
    skill_explainable = explainable_by_view_id["view_simulation_skill_overview"]

    return (
        DashboardReadOnlyViewEntry(
            view_entry_id="dashboardview_memory_project_architecture",
            view_kind="memory_dashboard_view",
            view_id="view_memory_project_architecture",
            linked_memory_tier_id=memory_entry.memory_tier_id,
            linked_skill_id="",
            linked_metric_id=memory_metric.metric_id,
            display_id=memory_presentation.display_id,
            display_role=memory_presentation.display_role,
            panel_id=memory_presentation.panel_id,
            read_only_mode="read_only",
            multilingual_ready=(
                memory_metric.multilingual_ready
                and memory_presentation.multilingual_ready
                and memory_explainable.multilingual_ready
            ),
            explanation_available=(
                memory_explainable.explanation_text_available
                and memory_explainable.explanation_payload_available
            ),
            active=memory_metric.active,
            description=(
                "Dashboard read-only view for foundational memory exposure on the mobile proxy."
            ),
        ),
        DashboardReadOnlyViewEntry(
            view_entry_id="dashboardview_skill_simulation_analysis",
            view_kind="skill_dashboard_view",
            view_id="view_simulation_skill_overview",
            linked_memory_tier_id="",
            linked_skill_id=skill_entry.skill_id,
            linked_metric_id=skill_metric.metric_id,
            display_id=skill_presentation.display_id,
            display_role=skill_presentation.display_role,
            panel_id=skill_presentation.panel_id,
            read_only_mode="read_only",
            multilingual_ready=(
                skill_metric.multilingual_ready
                and skill_presentation.multilingual_ready
                and skill_explainable.multilingual_ready
            ),
            explanation_available=(
                skill_explainable.explanation_text_available
                and skill_explainable.explanation_payload_available
            ),
            active=skill_metric.active,
            description=(
                "Dashboard read-only view for simulation skill exposure on the engineering display."
            ),
        ),
    )


def _build_memory_registry_read_only_entries() -> tuple[DashboardReadOnlyViewEntry, ...]:
    memory_registry = build_memory_registry_contract()
    memory_skill_metrics = build_memory_skill_metrics_contract()
    presentation_metrics = build_presentation_display_metrics_contract()
    explainable_binding = build_explainable_view_binding_contract()
    memory_registry_views = build_memory_registry_view_contract()

    memory_entry = memory_registry.entries[0]
    memory_metric = next(
        entry
        for entry in memory_skill_metrics.entries
        if entry.source_component == "memory_registry"
    )
    memory_presentation = next(
        entry
        for entry in presentation_metrics.entries
        if entry.view_id == "view_memory_project_architecture"
    )
    memory_explainable = next(
        entry
        for entry in explainable_binding.entries
        if entry.view_id == "view_memory_project_architecture"
    )

    return tuple(
        DashboardReadOnlyViewEntry(
            view_entry_id=f"dashboardview_{view.view_id.removeprefix('view_')}",
            view_kind="memory_registry_read_only_view",
            view_id=view.view_id,
            linked_memory_tier_id=memory_entry.memory_tier_id,
            linked_skill_id="",
            linked_metric_id=memory_metric.metric_id,
            display_id=memory_presentation.display_id,
            display_role="mobile_display_proxy",
            panel_id=view.panel_id,
            read_only_mode="read_only",
            multilingual_ready=(
                memory_metric.multilingual_ready
                and memory_presentation.multilingual_ready
                and memory_explainable.multilingual_ready
                and view.preview_ready
            ),
            explanation_available=(
                memory_explainable.explanation_text_available
                and memory_explainable.explanation_payload_available
            ),
            active=view.dashboard_visible,
            description=f"Dashboard read-only memory registry view for {view.source_component}.",
        )
        for view in memory_registry_views.entries
    )


def build_dashboard_read_only_views_contract() -> DashboardReadOnlyViewsContract:
    """Build canonical dashboard read-only memory/skill views contract."""

    entries = (
        *_build_root_memory_skill_entries(),
        *_build_memory_registry_read_only_entries(),
    )

    active_entries = sum(1 for entry in entries if entry.active)
    multilingual_ready_entries = sum(
        1 for entry in entries if entry.multilingual_ready
    )
    explanation_available_entries = sum(
        1 for entry in entries if entry.explanation_available
    )

    return DashboardReadOnlyViewsContract(
        total_entries=len(entries),
        active_entries=active_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        explanation_available_entries=explanation_available_entries,
        entries=entries,
    )
