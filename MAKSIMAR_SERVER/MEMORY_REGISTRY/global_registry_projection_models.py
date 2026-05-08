from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


GlobalRegistryEntryKind = Literal[
    "module",
    "skill",
    "memory_tier",
    "worker",
    "storage_node",
    "retrieval_source",
    "dashboard_view",
]

_REGISTRY_ID_PATTERN = re.compile(
    r"^(module|skill|memory|worker|storage_node|retrieval_source|panel)_[a-z][a-z0-9_]*$"
)
_MODULE_ID_PATTERN = re.compile(r"^module_[a-z][a-z0-9_]*_[a-z][a-z0-9_]*$")
_FLOW_STAGE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


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


def _ensure_unique_non_empty_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    normalized = tuple(_ensure_non_empty_str(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must contain unique values")
    return normalized


@dataclass(frozen=True, slots=True)
class GlobalRegistryProjectionEntry:
    """Read-only global registry projection entry.

    This is a projection over existing manifest/id/registry layers. It is not a
    new source of truth and does not write registry state.
    """

    entry_kind: GlobalRegistryEntryKind
    registry_id: str
    module_slug: str
    module_id: str
    source_layer: str
    dashboard_visible: bool
    retrieval_visible: bool
    observability_visible: bool
    flow_stages: tuple[str, ...]

    def __post_init__(self) -> None:
        registry_id = _ensure_non_empty_str(self.registry_id, "registry_id")
        module_slug = _ensure_non_empty_str(self.module_slug, "module_slug")
        module_id = _ensure_non_empty_str(self.module_id, "module_id")
        source_layer = _ensure_non_empty_str(self.source_layer, "source_layer")
        flow_stages = _ensure_unique_non_empty_tuple(self.flow_stages, "flow_stages")

        if not _REGISTRY_ID_PATTERN.fullmatch(registry_id):
            raise ValueError(f"Invalid registry_id: {registry_id}")

        if not _MODULE_ID_PATTERN.fullmatch(module_id):
            raise ValueError(f"Invalid module_id: {module_id}")

        for stage in flow_stages:
            if not _FLOW_STAGE_PATTERN.fullmatch(stage):
                raise ValueError(f"Invalid flow stage: {stage}")

        if not isinstance(self.dashboard_visible, bool):
            raise ValueError("dashboard_visible must be bool")

        if not isinstance(self.retrieval_visible, bool):
            raise ValueError("retrieval_visible must be bool")

        if not isinstance(self.observability_visible, bool):
            raise ValueError("observability_visible must be bool")

        object.__setattr__(self, "registry_id", registry_id)
        object.__setattr__(self, "module_slug", module_slug)
        object.__setattr__(self, "module_id", module_id)
        object.__setattr__(self, "source_layer", source_layer)
        object.__setattr__(self, "flow_stages", flow_stages)


@dataclass(frozen=True, slots=True)
class GlobalRegistryProjectionContract:
    """Read-only global registry projection contract."""

    total_entries: int
    dashboard_visible_entries: int
    retrieval_visible_entries: int
    observability_visible_entries: int
    entries: tuple[GlobalRegistryProjectionEntry, ...]

    def __post_init__(self) -> None:
        total_entries = _ensure_non_negative_int(self.total_entries, "total_entries")
        dashboard_visible_entries = _ensure_non_negative_int(
            self.dashboard_visible_entries,
            "dashboard_visible_entries",
        )
        retrieval_visible_entries = _ensure_non_negative_int(
            self.retrieval_visible_entries,
            "retrieval_visible_entries",
        )
        observability_visible_entries = _ensure_non_negative_int(
            self.observability_visible_entries,
            "observability_visible_entries",
        )

        if total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        computed_dashboard = sum(1 for entry in self.entries if entry.dashboard_visible)
        computed_retrieval = sum(1 for entry in self.entries if entry.retrieval_visible)
        computed_observability = sum(
            1 for entry in self.entries if entry.observability_visible
        )

        if dashboard_visible_entries != computed_dashboard:
            raise ValueError("dashboard_visible_entries must match computed count")

        if retrieval_visible_entries != computed_retrieval:
            raise ValueError("retrieval_visible_entries must match computed count")

        if observability_visible_entries != computed_observability:
            raise ValueError("observability_visible_entries must match computed count")

        registry_ids = tuple(entry.registry_id for entry in self.entries)
        if len(set(registry_ids)) != len(registry_ids):
            raise ValueError("Duplicate registry_id values detected")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "dashboard_visible_entries", dashboard_visible_entries)
        object.__setattr__(self, "retrieval_visible_entries", retrieval_visible_entries)
        object.__setattr__(self, "observability_visible_entries", observability_visible_entries)
