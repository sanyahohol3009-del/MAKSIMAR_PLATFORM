from __future__ import annotations

import re
from dataclasses import dataclass


_BINDING_ID_PATTERN = re.compile(r"^retrieval_registry_binding_[a-z][a-z0-9_]*$")


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
class RetrievalRegistryBindingEntry:
    binding_id: str
    component_kind: str
    source_ref: str
    source_total_entries: int
    active_entries: int
    retrieval_visible_entries: int
    observability_visible_entries: int
    selected_by_retrieval: bool
    binding_ready: bool

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(self.binding_id, "binding_id")
        component_kind = _ensure_non_empty_str(self.component_kind, "component_kind")
        source_ref = _ensure_non_empty_str(self.source_ref, "source_ref")
        source_total_entries = _ensure_non_negative_int(
            self.source_total_entries,
            "source_total_entries",
        )
        active_entries = _ensure_non_negative_int(self.active_entries, "active_entries")
        retrieval_visible_entries = _ensure_non_negative_int(
            self.retrieval_visible_entries,
            "retrieval_visible_entries",
        )
        observability_visible_entries = _ensure_non_negative_int(
            self.observability_visible_entries,
            "observability_visible_entries",
        )

        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid binding_id: {binding_id}")

        for field_name in ("selected_by_retrieval", "binding_ready"):
            _ensure_bool(getattr(self, field_name), field_name)

        if source_total_entries <= 0:
            raise ValueError("source_total_entries must be >= 1")
        if active_entries > source_total_entries:
            raise ValueError("active_entries must not exceed source_total_entries")
        if retrieval_visible_entries > source_total_entries:
            raise ValueError("retrieval_visible_entries must not exceed source_total_entries")
        if observability_visible_entries > source_total_entries:
            raise ValueError("observability_visible_entries must not exceed source_total_entries")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")

        object.__setattr__(self, "binding_id", binding_id)
        object.__setattr__(self, "component_kind", component_kind)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "source_total_entries", source_total_entries)
        object.__setattr__(self, "active_entries", active_entries)
        object.__setattr__(self, "retrieval_visible_entries", retrieval_visible_entries)
        object.__setattr__(self, "observability_visible_entries", observability_visible_entries)


@dataclass(frozen=True, slots=True)
class RetrievalRegistryBindingContract:
    total_bindings: int
    ready_bindings: int
    selected_by_retrieval_bindings: int
    retrieval_visible_total: int
    observability_visible_total: int
    binding_ready: bool
    entries: tuple[RetrievalRegistryBindingEntry, ...]

    def __post_init__(self) -> None:
        total_bindings = _ensure_non_negative_int(self.total_bindings, "total_bindings")
        ready_bindings = _ensure_non_negative_int(self.ready_bindings, "ready_bindings")
        selected_by_retrieval_bindings = _ensure_non_negative_int(
            self.selected_by_retrieval_bindings,
            "selected_by_retrieval_bindings",
        )
        retrieval_visible_total = _ensure_non_negative_int(
            self.retrieval_visible_total,
            "retrieval_visible_total",
        )
        observability_visible_total = _ensure_non_negative_int(
            self.observability_visible_total,
            "observability_visible_total",
        )

        if total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if ready_bindings != sum(1 for entry in self.entries if entry.binding_ready):
            raise ValueError("ready_bindings must match computed count")
        if selected_by_retrieval_bindings != sum(
            1 for entry in self.entries if entry.selected_by_retrieval
        ):
            raise ValueError("selected_by_retrieval_bindings must match computed count")
        if retrieval_visible_total != sum(entry.retrieval_visible_entries for entry in self.entries):
            raise ValueError("retrieval_visible_total must match computed count")
        if observability_visible_total != sum(
            entry.observability_visible_entries for entry in self.entries
        ):
            raise ValueError("observability_visible_total must match computed count")

        _ensure_bool(self.binding_ready, "binding_ready")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")
        if ready_bindings != total_bindings:
            raise ValueError("all registry bindings must be ready")
        if selected_by_retrieval_bindings <= 0:
            raise ValueError("at least one registry binding must be selected by retrieval")

        object.__setattr__(self, "total_bindings", total_bindings)
        object.__setattr__(self, "ready_bindings", ready_bindings)
        object.__setattr__(self, "selected_by_retrieval_bindings", selected_by_retrieval_bindings)
        object.__setattr__(self, "retrieval_visible_total", retrieval_visible_total)
        object.__setattr__(self, "observability_visible_total", observability_visible_total)
