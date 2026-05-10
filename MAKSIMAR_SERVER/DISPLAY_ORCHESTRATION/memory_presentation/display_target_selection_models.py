from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_summary,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import build_display_orchestration_contract
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.panel_resolution_models import (
    build_panel_resolution_contract,
)

_DISPLAY_TARGET_SELECTION_ID_PATTERN = re.compile(
    r"^display_target_selection_[a-z][a-z0-9_]*_[0-9]{3}$"
)


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
class DisplayTargetSelectionEntry:
    target_selection_id: str
    panel_resolution_id: str
    command_intent: str
    selected_display_id: str
    selected_display_role: str
    selected_zone_id: str
    selected_panel_id: str
    topology_bound: bool
    orchestration_bound: bool
    registry_routed: bool
    read_only: bool
    direct_display_switching_allowed: bool
    target_selection_ready: bool
    description: str

    def __post_init__(self) -> None:
        target_selection_id = _ensure_non_empty_str(
            self.target_selection_id,
            "target_selection_id",
        )
        if not _DISPLAY_TARGET_SELECTION_ID_PATTERN.fullmatch(target_selection_id):
            raise ValueError(f"Invalid target_selection_id: {target_selection_id}")

        for field_name in (
            "panel_resolution_id",
            "command_intent",
            "selected_display_id",
            "selected_display_role",
            "selected_zone_id",
            "selected_panel_id",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "topology_bound",
            "orchestration_bound",
            "registry_routed",
            "read_only",
            "direct_display_switching_allowed",
            "target_selection_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.topology_bound:
            raise ValueError("topology_bound must be True")
        if not self.orchestration_bound:
            raise ValueError("orchestration_bound must be True")
        if not self.registry_routed:
            raise ValueError("registry_routed must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.direct_display_switching_allowed:
            raise ValueError("direct_display_switching_allowed must be False")
        if not self.target_selection_ready:
            raise ValueError("target_selection_ready must be True")


@dataclass(frozen=True, slots=True)
class DisplayTargetSelectionContract:
    total_selections: int
    ready_selections: int
    topology_bound_selections: int
    orchestration_bound_selections: int
    registry_routed_selections: int
    read_only_selections: int
    direct_display_switching_allowed_selections: int
    entries: tuple[DisplayTargetSelectionEntry, ...]

    def __post_init__(self) -> None:
        if self.total_selections != len(self.entries):
            raise ValueError("total_selections must match entries length")
        if self.total_selections <= 0:
            raise ValueError("total_selections must be >= 1")

        expected = {
            "ready_selections": sum(1 for entry in self.entries if entry.target_selection_ready),
            "topology_bound_selections": sum(1 for entry in self.entries if entry.topology_bound),
            "orchestration_bound_selections": sum(1 for entry in self.entries if entry.orchestration_bound),
            "registry_routed_selections": sum(1 for entry in self.entries if entry.registry_routed),
            "read_only_selections": sum(1 for entry in self.entries if entry.read_only),
            "direct_display_switching_allowed_selections": sum(
                1 for entry in self.entries if entry.direct_display_switching_allowed
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_selections != self.total_selections:
            raise ValueError("all display target selections must be ready")
        if self.topology_bound_selections != self.total_selections:
            raise ValueError("all display target selections must be topology-bound")
        if self.orchestration_bound_selections != self.total_selections:
            raise ValueError("all display target selections must be orchestration-bound")
        if self.registry_routed_selections != self.total_selections:
            raise ValueError("all display target selections must be registry-routed")
        if self.read_only_selections != self.total_selections:
            raise ValueError("all display target selections must be read-only")
        if self.direct_display_switching_allowed_selections != 0:
            raise ValueError("display target selection must not directly switch displays")


def build_display_target_selection_contract() -> DisplayTargetSelectionContract:
    panels = build_panel_resolution_contract()
    orchestration = build_display_orchestration_contract()
    topology_summary = build_display_topology_summary()

    route_by_panel = {entry.selected_panel_id: entry for entry in orchestration.entries}

    entries = tuple(
        DisplayTargetSelectionEntry(
            target_selection_id=panel.panel_resolution_id.replace(
                "panel_resolution_",
                "display_target_selection_",
                1,
            ),
            panel_resolution_id=panel.panel_resolution_id,
            command_intent=route_by_panel[panel.resolved_panel_id].command_intent,
            selected_display_id=route_by_panel[panel.resolved_panel_id].selected_display_id,
            selected_display_role=route_by_panel[panel.resolved_panel_id].selected_display_role,
            selected_zone_id=route_by_panel[panel.resolved_panel_id].selected_zone_id,
            selected_panel_id=panel.resolved_panel_id,
            topology_bound=bool(topology_summary["summary_ready"]),
            orchestration_bound=panel.resolved_panel_id in route_by_panel,
            registry_routed=route_by_panel[panel.resolved_panel_id].registry_routed,
            read_only=True,
            direct_display_switching_allowed=False,
            target_selection_ready=(
                bool(topology_summary["summary_ready"])
                and panel.resolved_panel_id in route_by_panel
                and route_by_panel[panel.resolved_panel_id].registry_routed
            ),
            description=f"Read-only display target selection for {panel.resolved_panel_id}.",
        )
        for panel in panels.entries
    )

    return DisplayTargetSelectionContract(
        total_selections=len(entries),
        ready_selections=sum(1 for entry in entries if entry.target_selection_ready),
        topology_bound_selections=sum(1 for entry in entries if entry.topology_bound),
        orchestration_bound_selections=sum(1 for entry in entries if entry.orchestration_bound),
        registry_routed_selections=sum(1 for entry in entries if entry.registry_routed),
        read_only_selections=sum(1 for entry in entries if entry.read_only),
        direct_display_switching_allowed_selections=sum(
            1 for entry in entries if entry.direct_display_switching_allowed
        ),
        entries=entries,
    )
