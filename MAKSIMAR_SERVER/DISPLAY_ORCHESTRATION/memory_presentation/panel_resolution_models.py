from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.view_resolution_models import (
    build_view_resolution_contract,
)

_PANEL_RESOLUTION_ID_PATTERN = re.compile(r"^panel_resolution_[a-z][a-z0-9_]*_[0-9]{3}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class PanelResolutionEntry:
    panel_resolution_id: str
    view_resolution_id: str
    resolved_view_id: str
    resolved_panel_id: str
    panel_dashboard_bound: bool
    panel_source_bound: bool
    panel_read_only: bool
    panel_action_execution_allowed: bool
    panel_resolution_ready: bool
    description: str

    def __post_init__(self) -> None:
        resolution_id = _ensure_non_empty_str(
            self.panel_resolution_id,
            "panel_resolution_id",
        )
        if not _PANEL_RESOLUTION_ID_PATTERN.fullmatch(resolution_id):
            raise ValueError(f"Invalid panel_resolution_id: {resolution_id}")

        for field_name in (
            "view_resolution_id",
            "resolved_view_id",
            "resolved_panel_id",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "panel_dashboard_bound",
            "panel_source_bound",
            "panel_read_only",
            "panel_action_execution_allowed",
            "panel_resolution_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.panel_source_bound:
            raise ValueError("panel_source_bound must be True")
        if not self.panel_read_only:
            raise ValueError("panel_read_only must be True")
        if self.panel_action_execution_allowed:
            raise ValueError("panel_action_execution_allowed must be False")
        if not self.panel_resolution_ready:
            raise ValueError("panel_resolution_ready must be True")


@dataclass(frozen=True, slots=True)
class PanelResolutionContract:
    total_panels: int
    ready_panels: int
    dashboard_bound_panels: int
    source_bound_panels: int
    read_only_panels: int
    action_execution_allowed_panels: int
    entries: tuple[PanelResolutionEntry, ...]

    def __post_init__(self) -> None:
        if self.total_panels != len(self.entries):
            raise ValueError("total_panels must match entries length")
        if self.total_panels <= 0:
            raise ValueError("total_panels must be >= 1")

        expected = {
            "ready_panels": sum(1 for entry in self.entries if entry.panel_resolution_ready),
            "dashboard_bound_panels": sum(1 for entry in self.entries if entry.panel_dashboard_bound),
            "source_bound_panels": sum(1 for entry in self.entries if entry.panel_source_bound),
            "read_only_panels": sum(1 for entry in self.entries if entry.panel_read_only),
            "action_execution_allowed_panels": sum(1 for entry in self.entries if entry.panel_action_execution_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_panels != self.total_panels:
            raise ValueError("all panel resolutions must be ready")
        if self.source_bound_panels != self.total_panels:
            raise ValueError("all panel resolutions must be source-bound")
        if self.read_only_panels != self.total_panels:
            raise ValueError("all panel resolutions must be read-only")
        if self.action_execution_allowed_panels != 0:
            raise ValueError("panel resolutions must not execute actions")


def build_panel_resolution_contract() -> PanelResolutionContract:
    dashboard = build_dashboard_read_only_views_contract()
    views = build_view_resolution_contract()

    panel_ids_from_dashboard = {entry.panel_id for entry in dashboard.entries}

    entries = tuple(
        PanelResolutionEntry(
            panel_resolution_id=view.view_resolution_id.replace(
                "view_resolution_",
                "panel_resolution_",
                1,
            ),
            view_resolution_id=view.view_resolution_id,
            resolved_view_id=view.resolved_view_id,
            resolved_panel_id=view.resolved_panel_id,
            panel_dashboard_bound=view.resolved_panel_id in panel_ids_from_dashboard,
            panel_source_bound=True,
            panel_read_only=True,
            panel_action_execution_allowed=False,
            panel_resolution_ready=True,
            description=f"Read-only panel resolution for {view.resolved_view_id}.",
        )
        for view in views.entries
    )

    return PanelResolutionContract(
        total_panels=len(entries),
        ready_panels=sum(1 for entry in entries if entry.panel_resolution_ready),
        dashboard_bound_panels=sum(1 for entry in entries if entry.panel_dashboard_bound),
        source_bound_panels=sum(1 for entry in entries if entry.panel_source_bound),
        read_only_panels=sum(1 for entry in entries if entry.panel_read_only),
        action_execution_allowed_panels=sum(1 for entry in entries if entry.panel_action_execution_allowed),
        entries=entries,
    )
