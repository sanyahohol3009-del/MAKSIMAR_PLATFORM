from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_binding_models import (
    build_explainable_presentation_binding_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_preview_builder import (
    build_explainable_presentation_preview,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_summary_builder import (
    build_explainable_presentation_summary,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_view_binding_contract import (
    build_explainable_view_binding_contract,
)


_FORBIDDEN_EXPLAINABLE_ROOTS = (
    "dashboard_root",
    "display_manager_root",
    "gesture_root",
    "navigation_root",
    "explainability_root",
    "MAKSIMAR_CORE_LIB/memory_engine/explainable_view_binding",
)


@dataclass(frozen=True, slots=True)
class ExplainablePhaseReadiness:
    base_explainable_entries: int
    explainable_presentation_bindings: int
    dashboard_bound_bindings: int
    route_bound_bindings: int
    flow: Tuple[str, ...]
    base_explainable_ready: bool
    presentation_binding_ready: bool
    source_bound_ready: bool
    explanation_text_ready: bool
    explanation_payload_ready: bool
    multilingual_ready: bool
    read_only_ready: bool
    dashboard_bound_ready: bool
    route_bound_ready: bool
    route_bound_monitoring_ready: bool
    action_execution_allowed: int
    direct_display_switching_allowed: int
    no_new_explainability_roots: bool
    phase_ready: bool


def _no_forbidden_explainable_roots() -> bool:
    return not any(Path(root_name).exists() for root_name in _FORBIDDEN_EXPLAINABLE_ROOTS)


def build_explainable_phase_readiness() -> ExplainablePhaseReadiness:
    base = build_explainable_view_binding_contract()
    binding = build_explainable_presentation_binding_contract()
    summary = build_explainable_presentation_summary()
    preview = build_explainable_presentation_preview()

    base_explainable_ready = (
        base.total_entries >= binding.total_bindings
        and base.multilingual_ready_entries == base.total_entries
        and base.explanation_text_entries == base.total_entries
        and base.explanation_payload_entries == base.total_entries
    )
    presentation_binding_ready = (
        binding.ready_bindings == binding.total_bindings
        and binding.presentation_route_bound_bindings == binding.total_bindings
    )
    source_bound_ready = binding.explainable_source_bound_bindings == binding.total_bindings
    explanation_text_ready = binding.explanation_text_bindings == binding.total_bindings
    explanation_payload_ready = binding.explanation_payload_bindings == binding.total_bindings
    multilingual_ready = binding.multilingual_ready_bindings == binding.total_bindings
    read_only_ready = binding.read_only_bindings == binding.total_bindings
    dashboard_bound_ready = binding.dashboard_bound_bindings == 2
    route_bound_ready = binding.route_bound_bindings == 1

    monitoring_entries = tuple(
        entry for entry in binding.entries if entry.command_intent == "show_monitoring"
    )
    route_bound_monitoring_ready = (
        len(monitoring_entries) == 1
        and monitoring_entries[0].resolution_source == "display_orchestration_route"
        and monitoring_entries[0].view_id == "view_monitoring_panel"
        and monitoring_entries[0].panel_id == "panel_monitoring_panel"
        and monitoring_entries[0].explanation_text_available
        and monitoring_entries[0].explanation_payload_available
        and monitoring_entries[0].binding_ready
    )

    action_execution_allowed = int(summary["action_execution_allowed_bindings"])
    direct_display_switching_allowed = int(
        summary["direct_display_switching_allowed_bindings"]
    )
    no_new_explainability_roots = _no_forbidden_explainable_roots()

    phase_ready = (
        bool(summary["summary_ready"])
        and bool(preview["preview_ready"])
        and base_explainable_ready
        and presentation_binding_ready
        and source_bound_ready
        and explanation_text_ready
        and explanation_payload_ready
        and multilingual_ready
        and read_only_ready
        and dashboard_bound_ready
        and route_bound_ready
        and route_bound_monitoring_ready
        and action_execution_allowed == 0
        and direct_display_switching_allowed == 0
        and no_new_explainability_roots
    )

    return ExplainablePhaseReadiness(
        base_explainable_entries=base.total_entries,
        explainable_presentation_bindings=binding.total_bindings,
        dashboard_bound_bindings=binding.dashboard_bound_bindings,
        route_bound_bindings=binding.route_bound_bindings,
        flow=tuple(str(item) for item in preview["flow"]),
        base_explainable_ready=base_explainable_ready,
        presentation_binding_ready=presentation_binding_ready,
        source_bound_ready=source_bound_ready,
        explanation_text_ready=explanation_text_ready,
        explanation_payload_ready=explanation_payload_ready,
        multilingual_ready=multilingual_ready,
        read_only_ready=read_only_ready,
        dashboard_bound_ready=dashboard_bound_ready,
        route_bound_ready=route_bound_ready,
        route_bound_monitoring_ready=route_bound_monitoring_ready,
        action_execution_allowed=action_execution_allowed,
        direct_display_switching_allowed=direct_display_switching_allowed,
        no_new_explainability_roots=no_new_explainability_roots,
        phase_ready=phase_ready,
    )


def build_explainable_phase_preview() -> Dict[str, object]:
    readiness = build_explainable_phase_readiness()

    return {
        "flow": readiness.flow,
        "preview_ready": readiness.phase_ready,
        "phase_ready": readiness.phase_ready,
        "base_explainable_entries": readiness.base_explainable_entries,
        "explainable_presentation_bindings": readiness.explainable_presentation_bindings,
        "dashboard_bound_bindings": readiness.dashboard_bound_bindings,
        "route_bound_bindings": readiness.route_bound_bindings,
        "base_explainable_ready": readiness.base_explainable_ready,
        "presentation_binding_ready": readiness.presentation_binding_ready,
        "source_bound_ready": readiness.source_bound_ready,
        "explanation_text_ready": readiness.explanation_text_ready,
        "explanation_payload_ready": readiness.explanation_payload_ready,
        "multilingual_ready": readiness.multilingual_ready,
        "read_only_ready": readiness.read_only_ready,
        "dashboard_bound_ready": readiness.dashboard_bound_ready,
        "route_bound_ready": readiness.route_bound_ready,
        "route_bound_monitoring_ready": readiness.route_bound_monitoring_ready,
        "action_execution_allowed": readiness.action_execution_allowed,
        "direct_display_switching_allowed": readiness.direct_display_switching_allowed,
        "no_new_explainability_roots": readiness.no_new_explainability_roots,
    }
