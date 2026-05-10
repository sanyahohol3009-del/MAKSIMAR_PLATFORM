from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)

_ZONE_LAYOUT_ID_PATTERN = re.compile(r"^zone_layout_[a-z][a-z0-9_]*$")


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


def _zone_class(zone_id: str) -> str:
    if "sidebar" in zone_id:
        return "navigation_zone"
    if "explanation" in zone_id:
        return "explanation_zone"
    if "engineering" in zone_id or "simulation" in zone_id:
        return "engineering_zone"
    if "mobile" in zone_id:
        return "mobile_private_zone"
    return "main_content_zone"


@dataclass(frozen=True, slots=True)
class ZoneLayoutEntry:
    zone_layout_id: str
    display_id: str
    display_role: str
    zone_id: str
    zone_index: int
    zone_class: str
    default_panel_ids: tuple[str, ...]
    visibility_mode: str
    read_only: bool
    layout_ready: bool
    description: str

    def __post_init__(self) -> None:
        zone_layout_id = _ensure_non_empty_str(self.zone_layout_id, "zone_layout_id")
        if not _ZONE_LAYOUT_ID_PATTERN.fullmatch(zone_layout_id):
            raise ValueError(f"Invalid zone_layout_id: {zone_layout_id}")

        _ensure_non_empty_str(self.display_id, "display_id")
        _ensure_non_empty_str(self.display_role, "display_role")
        _ensure_non_empty_str(self.zone_id, "zone_id")
        _ensure_non_empty_str(self.zone_class, "zone_class")
        _ensure_non_empty_str(self.visibility_mode, "visibility_mode")
        _ensure_non_empty_str(self.description, "description")

        _ensure_non_negative_int(self.zone_index, "zone_index")
        if self.zone_index <= 0:
            raise ValueError("zone_index must be >= 1")

        if not isinstance(self.default_panel_ids, tuple) or not self.default_panel_ids:
            raise ValueError("default_panel_ids must be a non-empty tuple")
        if len(set(self.default_panel_ids)) != len(self.default_panel_ids):
            raise ValueError("default_panel_ids must contain unique values")

        _ensure_bool(self.read_only, "read_only")
        _ensure_bool(self.layout_ready, "layout_ready")

        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.layout_ready:
            raise ValueError("layout_ready must be True")


@dataclass(frozen=True, slots=True)
class ZoneLayoutContract:
    total_zones: int
    ready_zones: int
    private_zones: int
    shared_zones: int
    read_only_zones: int
    entries: tuple[ZoneLayoutEntry, ...]

    def __post_init__(self) -> None:
        if self.total_zones != len(self.entries):
            raise ValueError("total_zones must match entries length")
        if self.total_zones <= 0:
            raise ValueError("total_zones must be >= 1")

        expected = {
            "ready_zones": sum(1 for entry in self.entries if entry.layout_ready),
            "private_zones": sum(1 for entry in self.entries if entry.visibility_mode == "private"),
            "shared_zones": sum(1 for entry in self.entries if entry.visibility_mode == "shared"),
            "read_only_zones": sum(1 for entry in self.entries if entry.read_only),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_zones != self.total_zones:
            raise ValueError("all zones must be ready")
        if self.read_only_zones != self.total_zones:
            raise ValueError("all zones must be read-only")

        layout_ids = tuple(entry.zone_layout_id for entry in self.entries)
        if len(set(layout_ids)) != len(layout_ids):
            raise ValueError("duplicate zone_layout_id values detected")


def build_zone_layout_contract() -> ZoneLayoutContract:
    topology = build_display_topology_contract()

    entries: list[ZoneLayoutEntry] = []
    for display in topology.entries:
        for index, zone_id in enumerate(display.zone_ids, start=1):
            entries.append(
                ZoneLayoutEntry(
                    zone_layout_id=f"zone_layout_{display.display_id.removeprefix('display_')}_{index:03d}",
                    display_id=display.display_id,
                    display_role=display.display_role,
                    zone_id=zone_id,
                    zone_index=index,
                    zone_class=_zone_class(zone_id),
                    default_panel_ids=display.default_panel_ids,
                    visibility_mode=display.visibility_mode,
                    read_only=True,
                    layout_ready=True,
                    description=f"Read-only zone layout for {display.display_id}:{zone_id}.",
                )
            )

    contract_entries = tuple(entries)

    return ZoneLayoutContract(
        total_zones=len(contract_entries),
        ready_zones=sum(1 for entry in contract_entries if entry.layout_ready),
        private_zones=sum(1 for entry in contract_entries if entry.visibility_mode == "private"),
        shared_zones=sum(1 for entry in contract_entries if entry.visibility_mode == "shared"),
        read_only_zones=sum(1 for entry in contract_entries if entry.read_only),
        entries=contract_entries,
    )
