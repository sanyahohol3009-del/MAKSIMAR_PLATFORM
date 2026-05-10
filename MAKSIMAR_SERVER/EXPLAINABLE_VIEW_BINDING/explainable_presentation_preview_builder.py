from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_binding_models import (
    build_explainable_presentation_binding_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_presentation_summary_builder import (
    build_explainable_presentation_summary,
)


_EXPLAINABLE_PRESENTATION_PREVIEW_FLOW = (
    "presentation_router",
    "explainable_view_binding",
    "explainable_presentation_binding",
    "explainable_presentation_summary",
    "explainable_presentation_preview",
)


def build_explainable_presentation_preview() -> Dict[str, object]:
    contract = build_explainable_presentation_binding_contract()
    summary = build_explainable_presentation_summary()

    return {
        "flow": _EXPLAINABLE_PRESENTATION_PREVIEW_FLOW,
        "preview_ready": bool(summary["summary_ready"]),
        "summary_ready": summary["summary_ready"],
        "base_explainable_entries": summary["base_explainable_entries"],
        "explainable_presentation_bindings": summary["explainable_presentation_bindings"],
        "explainable_presentation_ready_bindings": summary[
            "explainable_presentation_ready_bindings"
        ],
        "dashboard_bound_bindings": summary["dashboard_bound_bindings"],
        "route_bound_bindings": summary["route_bound_bindings"],
        "action_execution_allowed_bindings": summary["action_execution_allowed_bindings"],
        "direct_display_switching_allowed_bindings": summary[
            "direct_display_switching_allowed_bindings"
        ],
        "presentation_route_ids": tuple(
            entry.presentation_route_id for entry in contract.entries
        ),
        "command_intents": tuple(entry.command_intent for entry in contract.entries),
        "view_ids": tuple(entry.view_id for entry in contract.entries),
        "panel_ids": tuple(entry.panel_id for entry in contract.entries),
        "display_ids": tuple(entry.display_id for entry in contract.entries),
        "selected_zone_ids": tuple(entry.selected_zone_id for entry in contract.entries),
        "resolution_sources": tuple(entry.resolution_source for entry in contract.entries),
        "explainable_binding_ids": tuple(
            entry.explainable_binding_id for entry in contract.entries
        ),
    }
