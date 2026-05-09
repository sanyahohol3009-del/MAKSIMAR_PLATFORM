from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.storage_registry_flow_builder import (
    build_storage_registry_flow_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.storage_registry_preview_builder import (
    build_storage_registry_preview,
)


_EXPECTED_STORAGE_FLOW = (
    "history_ingestion_storage_primitives",
    "storage_registry_contract",
    "artifact_collection_reference",
    "model_store_reference",
    "media_artifact_reference",
    "retrieval_index_reference",
    "portability_policy",
    "dashboard_read_only_preview",
)


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
class StorageRegistryPhaseReadiness:
    """Final CORE-side readiness gate for PHASE 1.5 storage registry."""

    total_entries: int
    dashboard_visible_entries: int
    retrieval_visible_entries: int
    relocation_ready_entries: int
    nas_ready_entries: int
    flow: tuple[str, ...]
    preview_ready: bool
    flow_ready: bool
    m2_nas_ready: bool
    artifact_collection_ready: bool
    model_store_ready: bool
    media_store_ready: bool
    retrieval_index_ready: bool
    phase_core_ready: bool

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

        if tuple(self.flow) != _EXPECTED_STORAGE_FLOW:
            raise ValueError("flow must match expected storage registry flow")

        preview_ready = _ensure_bool(self.preview_ready, "preview_ready")
        flow_ready = _ensure_bool(self.flow_ready, "flow_ready")
        m2_nas_ready = _ensure_bool(self.m2_nas_ready, "m2_nas_ready")
        artifact_collection_ready = _ensure_bool(
            self.artifact_collection_ready,
            "artifact_collection_ready",
        )
        model_store_ready = _ensure_bool(self.model_store_ready, "model_store_ready")
        media_store_ready = _ensure_bool(self.media_store_ready, "media_store_ready")
        retrieval_index_ready = _ensure_bool(
            self.retrieval_index_ready,
            "retrieval_index_ready",
        )
        phase_core_ready = _ensure_bool(self.phase_core_ready, "phase_core_ready")

        if total_entries <= 0:
            raise ValueError("total_entries must be >= 1")
        if dashboard_visible_entries <= 0:
            raise ValueError("dashboard_visible_entries must be >= 1")
        if relocation_ready_entries != total_entries:
            raise ValueError("all storage registry entries must be relocation-ready")
        if nas_ready_entries != total_entries:
            raise ValueError("all storage registry entries must be NAS-ready")
        if not preview_ready:
            raise ValueError("preview_ready must be True")
        if not flow_ready:
            raise ValueError("flow_ready must be True")
        if not m2_nas_ready:
            raise ValueError("m2_nas_ready must be True")
        if not artifact_collection_ready:
            raise ValueError("artifact_collection_ready must be True")
        if not model_store_ready:
            raise ValueError("model_store_ready must be True")
        if not media_store_ready:
            raise ValueError("media_store_ready must be True")
        if not retrieval_index_ready:
            raise ValueError("retrieval_index_ready must be True")
        if not phase_core_ready:
            raise ValueError("phase_core_ready must be True")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "dashboard_visible_entries", dashboard_visible_entries)
        object.__setattr__(self, "retrieval_visible_entries", retrieval_visible_entries)
        object.__setattr__(self, "relocation_ready_entries", relocation_ready_entries)
        object.__setattr__(self, "nas_ready_entries", nas_ready_entries)


def build_storage_registry_phase_readiness() -> StorageRegistryPhaseReadiness:
    """Build final read-only CORE-side PHASE 1.5 storage readiness gate."""

    preview = build_storage_registry_preview()
    flow = build_storage_registry_flow_preview()

    entry_kinds = set(preview["entry_kinds"])

    artifact_collection_ready = bool(preview["artifact_collection_id"])
    model_store_ready = bool(preview["model_store_id"])
    media_store_ready = bool(preview["media_store_id"])
    retrieval_index_ready = bool(preview["retrieval_index_id"])

    phase_core_ready = (
        bool(preview["preview_ready"])
        and bool(flow["flow_ready"])
        and bool(preview["storage_ready_for_m2_nas"])
        and artifact_collection_ready
        and model_store_ready
        and media_store_ready
        and retrieval_index_ready
        and "artifact_collection" in entry_kinds
        and "model_store" in entry_kinds
        and "media_artifact_store" in entry_kinds
        and "retrieval_index" in entry_kinds
    )

    return StorageRegistryPhaseReadiness(
        total_entries=int(preview["total_entries"]),
        dashboard_visible_entries=int(preview["dashboard_visible_entries"]),
        retrieval_visible_entries=int(preview["retrieval_visible_entries"]),
        relocation_ready_entries=int(preview["relocation_ready_entries"]),
        nas_ready_entries=int(preview["nas_ready_entries"]),
        flow=tuple(flow["flow"]),
        preview_ready=bool(preview["preview_ready"]),
        flow_ready=bool(flow["flow_ready"]),
        m2_nas_ready=bool(preview["storage_ready_for_m2_nas"]),
        artifact_collection_ready=artifact_collection_ready,
        model_store_ready=model_store_ready,
        media_store_ready=media_store_ready,
        retrieval_index_ready=retrieval_index_ready,
        phase_core_ready=phase_core_ready,
    )
