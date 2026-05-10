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
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.view_resolution_models import (
    build_view_resolution_contract,
)


def build_presentation_summary() -> Dict[str, object]:
    requests = build_presentation_request_contract()
    views = build_view_resolution_contract()
    panels = build_panel_resolution_contract()
    targets = build_display_target_selection_contract()

    summary_ready = (
        requests.ready_requests == requests.total_requests
        and requests.action_execution_allowed_requests == 0
        and requests.direct_display_switching_allowed_requests == 0
        and views.ready_resolutions == views.total_resolutions
        and panels.ready_panels == panels.total_panels
        and panels.action_execution_allowed_panels == 0
        and targets.ready_selections == targets.total_selections
        and targets.direct_display_switching_allowed_selections == 0
    )

    return {
        "presentation_requests": requests.total_requests,
        "presentation_ready_requests": requests.ready_requests,
        "presentation_action_execution_allowed_requests": requests.action_execution_allowed_requests,
        "presentation_direct_display_switching_allowed_requests": requests.direct_display_switching_allowed_requests,
        "view_resolutions": views.total_resolutions,
        "view_ready_resolutions": views.ready_resolutions,
        "view_dashboard_bound_resolutions": views.dashboard_bound_resolutions,
        "view_source_bound_resolutions": views.source_bound_resolutions,
        "panel_resolutions": panels.total_panels,
        "panel_ready_resolutions": panels.ready_panels,
        "panel_source_bound_resolutions": panels.source_bound_panels,
        "panel_action_execution_allowed": panels.action_execution_allowed_panels,
        "display_target_selections": targets.total_selections,
        "display_target_ready_selections": targets.ready_selections,
        "display_target_direct_switching_allowed": targets.direct_display_switching_allowed_selections,
        "summary_ready": summary_ready,
    }
