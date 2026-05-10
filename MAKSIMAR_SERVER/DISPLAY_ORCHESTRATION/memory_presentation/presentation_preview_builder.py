from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.display_target_selection_models import (
    build_display_target_selection_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.panel_resolution_models import (
    build_panel_resolution_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.presentation_request_models import (
    build_presentation_request_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.presentation_summary_builder import (
    build_presentation_summary,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.view_resolution_models import (
    build_view_resolution_contract,
)


_PRESENTATION_PREVIEW_FLOW = (
    "presentation_request",
    "view_resolution",
    "panel_resolution",
    "display_target_selection",
    "presentation_summary",
    "presentation_preview",
)


def build_presentation_preview() -> Dict[str, object]:
    requests = build_presentation_request_contract()
    views = build_view_resolution_contract()
    panels = build_panel_resolution_contract()
    targets = build_display_target_selection_contract()
    summary = build_presentation_summary()

    return {
        "flow": _PRESENTATION_PREVIEW_FLOW,
        "preview_ready": bool(summary["summary_ready"]),
        "summary_ready": summary["summary_ready"],
        "presentation_requests": summary["presentation_requests"],
        "presentation_ready_requests": summary["presentation_ready_requests"],
        "view_resolutions": summary["view_resolutions"],
        "view_ready_resolutions": summary["view_ready_resolutions"],
        "panel_resolutions": summary["panel_resolutions"],
        "panel_ready_resolutions": summary["panel_ready_resolutions"],
        "display_target_selections": summary["display_target_selections"],
        "display_target_ready_selections": summary["display_target_ready_selections"],
        "action_execution_allowed": summary["presentation_action_execution_allowed_requests"]
        + summary["panel_action_execution_allowed"],
        "direct_display_switching_allowed": summary["presentation_direct_display_switching_allowed_requests"]
        + summary["display_target_direct_switching_allowed"],
        "request_ids": tuple(entry.presentation_request_id for entry in requests.entries),
        "command_intents": tuple(entry.command_intent for entry in requests.entries),
        "resolved_view_ids": tuple(entry.resolved_view_id for entry in views.entries),
        "resolved_panel_ids": tuple(entry.resolved_panel_id for entry in panels.entries),
        "selected_display_ids": tuple(entry.selected_display_id for entry in targets.entries),
        "selected_zone_ids": tuple(entry.selected_zone_id for entry in targets.entries),
    }
