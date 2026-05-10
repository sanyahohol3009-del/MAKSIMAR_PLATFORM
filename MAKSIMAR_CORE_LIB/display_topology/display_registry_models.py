from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)

_DISPLAY_REGISTRY_ID_PATTERN = re.compile(r"^display_registry_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class DisplayRegistryEntry:
    display_registry_id: str
    display_id: str
    display_role: str
    visibility_mode: str
    zone_count: int
    default_panel_count: int
    capability_count: int
    multilingual_ready: bool
    explainable_ready: bool
    registry_routing_ready: bool
    dashboard_bindable: bool
    read_only: bool
    direct_switching_allowed: bool
    registry_entry_ready: bool
    description: str

    def __post_init__(self) -> None:
        display_registry_id = _ensure_non_empty_str(
            self.display_registry_id,
            "display_registry_id",
        )
        if not _DISPLAY_REGISTRY_ID_PATTERN.fullmatch(display_registry_id):
            raise ValueError(f"Invalid display_registry_id: {display_registry_id}")

        _ensure_non_empty_str(self.display_id, "display_id")
        _ensure_non_empty_str(self.display_role, "display_role")
        _ensure_non_empty_str(self.visibility_mode, "visibility_mode")
        _ensure_non_empty_str(self.description, "description")

        for field_name in ("zone_count", "default_panel_count", "capability_count"):
            value = _ensure_non_negative_int(getattr(self, field_name), field_name)
            if value <= 0:
                raise ValueError(f"{field_name} must be >= 1")

        for field_name in (
            "multilingual_ready",
            "explainable_ready",
            "registry_routing_ready",
            "dashboard_bindable",
            "read_only",
            "direct_switching_allowed",
            "registry_entry_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.multilingual_ready:
            raise ValueError("multilingual_ready must be True")
        if not self.explainable_ready:
            raise ValueError("explainable_ready must be True")
        if not self.registry_routing_ready:
            raise ValueError("registry_routing_ready must be True")
        if not self.dashboard_bindable:
            raise ValueError("dashboard_bindable must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.direct_switching_allowed:
            raise ValueError("direct_switching_allowed must be False")
        if not self.registry_entry_ready:
            raise ValueError("registry_entry_ready must be True")


@dataclass(frozen=True, slots=True)
class DisplayRegistryContract:
    total_entries: int
    ready_entries: int
    dashboard_bindable_entries: int
    registry_routing_ready_entries: int
    read_only_entries: int
    direct_switching_allowed_entries: int
    entries: tuple[DisplayRegistryEntry, ...]

    def __post_init__(self) -> None:
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")
        if self.total_entries <= 0:
            raise ValueError("total_entries must be >= 1")

        computed_ready = sum(1 for entry in self.entries if entry.registry_entry_ready)
        computed_bindable = sum(1 for entry in self.entries if entry.dashboard_bindable)
        computed_registry = sum(1 for entry in self.entries if entry.registry_routing_ready)
        computed_read_only = sum(1 for entry in self.entries if entry.read_only)
        computed_switching = sum(1 for entry in self.entries if entry.direct_switching_allowed)

        expected = {
            "ready_entries": computed_ready,
            "dashboard_bindable_entries": computed_bindable,
            "registry_routing_ready_entries": computed_registry,
            "read_only_entries": computed_read_only,
            "direct_switching_allowed_entries": computed_switching,
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_entries != self.total_entries:
            raise ValueError("all display registry entries must be ready")
        if self.dashboard_bindable_entries != self.total_entries:
            raise ValueError("all display registry entries must be dashboard-bindable")
        if self.registry_routing_ready_entries != self.total_entries:
            raise ValueError("all display registry entries must be registry-routed")
        if self.read_only_entries != self.total_entries:
            raise ValueError("all display registry entries must be read-only")
        if self.direct_switching_allowed_entries != 0:
            raise ValueError("display registry must not allow direct switching")

        display_ids = tuple(entry.display_id for entry in self.entries)
        if len(set(display_ids)) != len(display_ids):
            raise ValueError("duplicate display_id values detected")


def build_display_registry_contract() -> DisplayRegistryContract:
    topology = build_display_topology_contract()

    entries = tuple(
        DisplayRegistryEntry(
            display_registry_id=f"display_registry_{entry.display_id.removeprefix('display_')}",
            display_id=entry.display_id,
            display_role=entry.display_role,
            visibility_mode=entry.visibility_mode,
            zone_count=len(entry.zone_ids),
            default_panel_count=len(entry.default_panel_ids),
            capability_count=len(entry.capabilities),
            multilingual_ready=entry.supports_multilingual_rendering,
            explainable_ready=entry.supports_explainable_views,
            registry_routing_ready=entry.supports_registry_routing,
            dashboard_bindable=True,
            read_only=True,
            direct_switching_allowed=False,
            registry_entry_ready=True,
            description=f"Read-only display registry entry for {entry.display_id}.",
        )
        for entry in topology.entries
    )

    return DisplayRegistryContract(
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.registry_entry_ready),
        dashboard_bindable_entries=sum(1 for entry in entries if entry.dashboard_bindable),
        registry_routing_ready_entries=sum(1 for entry in entries if entry.registry_routing_ready),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        direct_switching_allowed_entries=sum(
            1 for entry in entries if entry.direct_switching_allowed
        ),
        entries=entries,
    )
