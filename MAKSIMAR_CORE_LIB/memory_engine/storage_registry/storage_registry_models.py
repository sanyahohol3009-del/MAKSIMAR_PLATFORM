from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.portable_storage_reference_models import (
    PortableStorageReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_models import (
    StorageNode,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)


StorageRegistryEntryKind = Literal[
    "history_storage_node",
    "portable_reference",
    "artifact_collection",
    "model_store",
    "media_artifact_store",
    "retrieval_index",
]

_STORAGE_REGISTRY_ID_PATTERN = re.compile(r"^storage_registry_[a-z][a-z0-9_]*$")


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


@dataclass(frozen=True, slots=True)
class StorageRegistryEntry:
    """Read-only registry entry binding existing storage primitives."""

    registry_id: str
    entry_kind: StorageRegistryEntryKind
    title: str
    storage_node: StorageNode | None
    storage_root: StorageRoot | None
    portable_reference: PortableStorageReference | None
    dashboard_visible: bool
    retrieval_visible: bool
    relocation_ready: bool
    nas_ready: bool

    def __post_init__(self) -> None:
        registry_id = _ensure_non_empty_str(self.registry_id, "registry_id")
        title = _ensure_non_empty_str(self.title, "title")

        if not _STORAGE_REGISTRY_ID_PATTERN.fullmatch(registry_id):
            raise ValueError(f"Invalid registry_id: {registry_id}")

        for field_name in (
            "dashboard_visible",
            "retrieval_visible",
            "relocation_ready",
            "nas_ready",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise ValueError(f"{field_name} must be bool")

        if (
            self.storage_node is None
            and self.storage_root is None
            and self.portable_reference is None
        ):
            raise ValueError(
                "At least one storage primitive must be bound to registry entry"
            )

        object.__setattr__(self, "registry_id", registry_id)
        object.__setattr__(self, "title", title)


@dataclass(frozen=True, slots=True)
class StorageRegistryContract:
    """Read-only storage registry contract."""

    total_entries: int
    dashboard_visible_entries: int
    retrieval_visible_entries: int
    relocation_ready_entries: int
    nas_ready_entries: int
    entries: tuple[StorageRegistryEntry, ...]

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
        relocation_ready_entries = _ensure_non_negative_int(
            self.relocation_ready_entries,
            "relocation_ready_entries",
        )
        nas_ready_entries = _ensure_non_negative_int(
            self.nas_ready_entries,
            "nas_ready_entries",
        )

        if total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        if dashboard_visible_entries != sum(
            1 for entry in self.entries if entry.dashboard_visible
        ):
            raise ValueError("dashboard_visible_entries must match computed count")

        if retrieval_visible_entries != sum(
            1 for entry in self.entries if entry.retrieval_visible
        ):
            raise ValueError("retrieval_visible_entries must match computed count")

        if relocation_ready_entries != sum(
            1 for entry in self.entries if entry.relocation_ready
        ):
            raise ValueError("relocation_ready_entries must match computed count")

        if nas_ready_entries != sum(1 for entry in self.entries if entry.nas_ready):
            raise ValueError("nas_ready_entries must match computed count")

        registry_ids = tuple(entry.registry_id for entry in self.entries)
        if len(set(registry_ids)) != len(registry_ids):
            raise ValueError("Duplicate registry_id values detected")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "dashboard_visible_entries", dashboard_visible_entries)
        object.__setattr__(self, "retrieval_visible_entries", retrieval_visible_entries)
        object.__setattr__(self, "relocation_ready_entries", relocation_ready_entries)
        object.__setattr__(self, "nas_ready_entries", nas_ready_entries)
