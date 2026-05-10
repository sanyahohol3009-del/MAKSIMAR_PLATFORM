from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_binding_models import (
    build_explainable_presentation_binding_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_view_binding_contract import (
    build_explainable_view_binding_contract,
)


def build_explainable_presentation_summary() -> Dict[str, object]:
    base = build_explainable_view_binding_contract()
    presentation = build_explainable_presentation_binding_contract()

    summary_ready = (
        base.total_entries >= presentation.total_bindings
        and base.multilingual_ready_entries == base.total_entries
        and base.explanation_text_entries == base.total_entries
        and base.explanation_payload_entries == base.total_entries
        and presentation.ready_bindings == presentation.total_bindings
        and presentation.presentation_route_bound_bindings == presentation.total_bindings
        and presentation.explainable_source_bound_bindings == presentation.total_bindings
        and presentation.explanation_text_bindings == presentation.total_bindings
        and presentation.explanation_payload_bindings == presentation.total_bindings
        and presentation.multilingual_ready_bindings == presentation.total_bindings
        and presentation.read_only_bindings == presentation.total_bindings
        and presentation.action_execution_allowed_bindings == 0
        and presentation.direct_display_switching_allowed_bindings == 0
    )

    return {
        "base_explainable_entries": base.total_entries,
        "base_multilingual_ready_entries": base.multilingual_ready_entries,
        "base_explanation_text_entries": base.explanation_text_entries,
        "base_explanation_payload_entries": base.explanation_payload_entries,
        "explainable_presentation_bindings": presentation.total_bindings,
        "explainable_presentation_ready_bindings": presentation.ready_bindings,
        "presentation_route_bound_bindings": presentation.presentation_route_bound_bindings,
        "explainable_source_bound_bindings": presentation.explainable_source_bound_bindings,
        "explanation_text_bindings": presentation.explanation_text_bindings,
        "explanation_payload_bindings": presentation.explanation_payload_bindings,
        "multilingual_ready_bindings": presentation.multilingual_ready_bindings,
        "read_only_bindings": presentation.read_only_bindings,
        "dashboard_bound_bindings": presentation.dashboard_bound_bindings,
        "route_bound_bindings": presentation.route_bound_bindings,
        "action_execution_allowed_bindings": presentation.action_execution_allowed_bindings,
        "direct_display_switching_allowed_bindings": presentation.direct_display_switching_allowed_bindings,
        "summary_ready": summary_ready,
    }
