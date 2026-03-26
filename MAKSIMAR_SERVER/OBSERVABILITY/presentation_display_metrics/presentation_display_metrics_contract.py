from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_view_binding_contract,
)
from MAKSIMAR_SERVER.OBSERVABILITY.presentation_display_metrics.presentation_display_metrics_models import (
    PresentationDisplayMetricEntry,
    PresentationDisplayMetricsContract,
)


def build_presentation_display_metrics_contract() -> PresentationDisplayMetricsContract:
    """Build observability contract for presentation/display routing."""
    display_topology = build_display_topology_contract()
    display_orchestration = build_display_orchestration_contract()
    explainable_binding = build_explainable_view_binding_contract()

    display_by_id = {
        entry.display_id: entry for entry in display_topology.entries
    }
    explainable_by_view_id = {
        entry.view_id: entry for entry in explainable_binding.entries
    }

    entries = []
    for orchestration_entry in display_orchestration.entries:
        display_entry = display_by_id[orchestration_entry.selected_display_id]
        explainable_entry = explainable_by_view_id[orchestration_entry.resolved_view_id]

        entries.append(
            PresentationDisplayMetricEntry(
                metric_id=f"pdmetric_{orchestration_entry.route_request_id}",
                source_component="display_orchestration",
                route_request_id=orchestration_entry.route_request_id,
                view_id=orchestration_entry.resolved_view_id,
                display_id=orchestration_entry.selected_display_id,
                display_role=orchestration_entry.selected_display_role,
                zone_id=orchestration_entry.selected_zone_id,
                panel_id=orchestration_entry.selected_panel_id,
                visibility_mode=display_entry.visibility_mode,
                explanation_bound=(
                    explainable_entry.explanation_text_available
                    and explainable_entry.explanation_payload_available
                ),
                multilingual_ready=(
                    display_entry.supports_multilingual_rendering
                    and orchestration_entry.multilingual_ready
                    and explainable_entry.multilingual_ready
                ),
                registry_routed=(
                    display_entry.supports_registry_routing
                    and orchestration_entry.registry_routed
                ),
                event_severity="info",
                alert_emitted=False,
                description=(
                    f"Observability metric for presentation/display route "
                    f"{orchestration_entry.route_request_id}."
                ),
            )
        )

    private_route_entries = sum(
        1 for entry in entries if entry.visibility_mode == "private"
    )
    shared_route_entries = sum(
        1 for entry in entries if entry.visibility_mode == "shared"
    )
    explanation_bound_entries = sum(
        1 for entry in entries if entry.explanation_bound
    )
    multilingual_ready_entries = sum(
        1 for entry in entries if entry.multilingual_ready
    )

    return PresentationDisplayMetricsContract(
        total_entries=len(entries),
        private_route_entries=private_route_entries,
        shared_route_entries=shared_route_entries,
        explanation_bound_entries=explanation_bound_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        entries=tuple(entries),
    )
