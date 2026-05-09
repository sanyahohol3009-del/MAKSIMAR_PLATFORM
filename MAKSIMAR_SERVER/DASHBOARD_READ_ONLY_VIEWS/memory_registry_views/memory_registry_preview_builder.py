from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views.memory_registry_summary_builder import (
    build_memory_registry_view_summary,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views.memory_registry_view_builder import (
    build_memory_registry_panel_contract,
    build_memory_registry_view_contract,
)


_MEMORY_REGISTRY_VIEW_FLOW = (
    "memory_registry_summary",
    "panel_contract",
    "view_contract",
    "dashboard_read_only_preview",
)


def build_memory_registry_view_preview() -> Dict[str, object]:
    summary = build_memory_registry_view_summary()
    panel_contract = build_memory_registry_panel_contract()
    view_contract = build_memory_registry_view_contract()

    return {
        "flow": _MEMORY_REGISTRY_VIEW_FLOW,
        "summary_ready": summary["summary_ready"],
        "total_panels": panel_contract.total_panels,
        "ready_panels": panel_contract.ready_panels,
        "read_only_panels": panel_contract.read_only_panels,
        "total_views": view_contract.total_views,
        "read_only_views": view_contract.read_only_views,
        "preview_ready_views": view_contract.preview_ready_views,
        "dashboard_visible_views": view_contract.dashboard_visible_views,
        "action_exposure_allowed_panels": panel_contract.action_exposure_allowed_panels,
        "display_orchestration_allowed_panels": panel_contract.display_orchestration_allowed_panels,
        "panel_ids": tuple(panel.panel_id for panel in panel_contract.entries),
        "view_ids": tuple(view.view_id for view in view_contract.entries),
        "retrieval_phase_ready": summary["retrieval_phase_ready"],
        "read_only": summary["read_only"],
        "action_exposure_allowed": summary["action_exposure_allowed"],
        "display_orchestration_allowed": summary["display_orchestration_allowed"],
        "preview_ready": True,
    }
