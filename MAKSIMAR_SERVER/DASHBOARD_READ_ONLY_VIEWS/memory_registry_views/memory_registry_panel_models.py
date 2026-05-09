from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


MemoryRegistryPanelKind = Literal[
    "memory_domain_map",
    "memory_registry_graph",
    "memory_timeline",
    "retrieval_trace",
    "storage_map",
    "media_artifact_flow",
    "model_store_status",
    "history_flow",
]

MemoryRegistryPanelStatus = Literal["ready", "degraded", "hidden"]


_PANEL_ID_PATTERN = re.compile(r"^panel_memory_[a-z][a-z0-9_]*$")


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
class MemoryRegistryPanelEntry:
    panel_id: str
    panel_kind: MemoryRegistryPanelKind
    title: str
    source_component: str
    source_entries: int
    visible_entries: int
    read_only: bool
    action_exposure_allowed: bool
    display_orchestration_allowed: bool
    status: MemoryRegistryPanelStatus

    def __post_init__(self) -> None:
        panel_id = _ensure_non_empty_str(self.panel_id, "panel_id")
        title = _ensure_non_empty_str(self.title, "title")
        source_component = _ensure_non_empty_str(
            self.source_component,
            "source_component",
        )
        source_entries = _ensure_non_negative_int(self.source_entries, "source_entries")
        visible_entries = _ensure_non_negative_int(self.visible_entries, "visible_entries")

        if not _PANEL_ID_PATTERN.fullmatch(panel_id):
            raise ValueError(f"Invalid panel_id: {panel_id}")

        if visible_entries > source_entries:
            raise ValueError("visible_entries must not exceed source_entries")

        for field_name in (
            "read_only",
            "action_exposure_allowed",
            "display_orchestration_allowed",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.action_exposure_allowed:
            raise ValueError("action_exposure_allowed must be False")
        if self.display_orchestration_allowed:
            raise ValueError("display_orchestration_allowed must be False")
        if self.status != "ready":
            raise ValueError("status must be ready for PHASE 1.8 Batch 1")

        object.__setattr__(self, "panel_id", panel_id)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "source_component", source_component)
        object.__setattr__(self, "source_entries", source_entries)
        object.__setattr__(self, "visible_entries", visible_entries)


@dataclass(frozen=True, slots=True)
class MemoryRegistryPanelContract:
    total_panels: int
    ready_panels: int
    read_only_panels: int
    action_exposure_allowed_panels: int
    display_orchestration_allowed_panels: int
    entries: tuple[MemoryRegistryPanelEntry, ...]

    def __post_init__(self) -> None:
        total_panels = _ensure_non_negative_int(self.total_panels, "total_panels")
        ready_panels = _ensure_non_negative_int(self.ready_panels, "ready_panels")
        read_only_panels = _ensure_non_negative_int(self.read_only_panels, "read_only_panels")
        action_exposure_allowed_panels = _ensure_non_negative_int(
            self.action_exposure_allowed_panels,
            "action_exposure_allowed_panels",
        )
        display_orchestration_allowed_panels = _ensure_non_negative_int(
            self.display_orchestration_allowed_panels,
            "display_orchestration_allowed_panels",
        )

        if total_panels != len(self.entries):
            raise ValueError("total_panels must match entries length")
        if total_panels <= 0:
            raise ValueError("total_panels must be >= 1")
        if ready_panels != sum(1 for entry in self.entries if entry.status == "ready"):
            raise ValueError("ready_panels must match computed count")
        if read_only_panels != sum(1 for entry in self.entries if entry.read_only):
            raise ValueError("read_only_panels must match computed count")
        if action_exposure_allowed_panels != sum(
            1 for entry in self.entries if entry.action_exposure_allowed
        ):
            raise ValueError("action_exposure_allowed_panels must match computed count")
        if display_orchestration_allowed_panels != sum(
            1 for entry in self.entries if entry.display_orchestration_allowed
        ):
            raise ValueError("display_orchestration_allowed_panels must match computed count")

        if ready_panels != total_panels:
            raise ValueError("all panels must be ready")
        if read_only_panels != total_panels:
            raise ValueError("all panels must be read-only")
        if action_exposure_allowed_panels != 0:
            raise ValueError("no action exposure is allowed in read-only views")
        if display_orchestration_allowed_panels != 0:
            raise ValueError("display orchestration is not allowed in PHASE 1.8")

        panel_ids = tuple(entry.panel_id for entry in self.entries)
        if len(set(panel_ids)) != len(panel_ids):
            raise ValueError("duplicate panel_id values detected")

        object.__setattr__(self, "total_panels", total_panels)
        object.__setattr__(self, "ready_panels", ready_panels)
        object.__setattr__(self, "read_only_panels", read_only_panels)
        object.__setattr__(
            self,
            "action_exposure_allowed_panels",
            action_exposure_allowed_panels,
        )
        object.__setattr__(
            self,
            "display_orchestration_allowed_panels",
            display_orchestration_allowed_panels,
        )
