from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_memory_preview_builder import (
    build_media_memory_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_memory_read_model import (
    build_media_artifact_memory_read_model,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_storage_binding_preview_builder import (
    build_media_storage_binding_preview,
)


_EXPECTED_MEDIA_MEMORY_FLOW = (
    "media_memory_read_model",
    "media_memory_preview",
    "media_storage_binding",
    "dashboard_rag_read_only_preview",
    "no_binary_payload_gate",
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
class MediaMemoryPhaseReadiness:
    """Final CORE-side readiness gate for PHASE 1.6 media memory."""

    total_records: int
    dashboard_visible_records: int
    retrieval_visible_records: int
    binary_external_records: int
    provenance_required_records: int
    traceability_required_records: int
    approval_required_records: int
    storage_bindings: int
    storage_ready_bindings: int
    binary_external_bindings: int
    flow: tuple[str, ...]
    preview_ready: bool
    media_memory_ready: bool
    storage_binding_ready: bool
    no_binary_payloads: bool
    provenance_traceability_ready: bool
    dashboard_rag_ready: bool
    phase_core_ready: bool

    def __post_init__(self) -> None:
        total_records = _ensure_non_negative_int(self.total_records, "total_records")
        dashboard_visible_records = _ensure_non_negative_int(
            self.dashboard_visible_records,
            "dashboard_visible_records",
        )
        retrieval_visible_records = _ensure_non_negative_int(
            self.retrieval_visible_records,
            "retrieval_visible_records",
        )
        binary_external_records = _ensure_non_negative_int(
            self.binary_external_records,
            "binary_external_records",
        )
        provenance_required_records = _ensure_non_negative_int(
            self.provenance_required_records,
            "provenance_required_records",
        )
        traceability_required_records = _ensure_non_negative_int(
            self.traceability_required_records,
            "traceability_required_records",
        )
        approval_required_records = _ensure_non_negative_int(
            self.approval_required_records,
            "approval_required_records",
        )
        storage_bindings = _ensure_non_negative_int(
            self.storage_bindings,
            "storage_bindings",
        )
        storage_ready_bindings = _ensure_non_negative_int(
            self.storage_ready_bindings,
            "storage_ready_bindings",
        )
        binary_external_bindings = _ensure_non_negative_int(
            self.binary_external_bindings,
            "binary_external_bindings",
        )

        if tuple(self.flow) != _EXPECTED_MEDIA_MEMORY_FLOW:
            raise ValueError("flow must match expected PHASE 1.6 CORE flow")

        preview_ready = _ensure_bool(self.preview_ready, "preview_ready")
        media_memory_ready = _ensure_bool(
            self.media_memory_ready,
            "media_memory_ready",
        )
        storage_binding_ready = _ensure_bool(
            self.storage_binding_ready,
            "storage_binding_ready",
        )
        no_binary_payloads = _ensure_bool(
            self.no_binary_payloads,
            "no_binary_payloads",
        )
        provenance_traceability_ready = _ensure_bool(
            self.provenance_traceability_ready,
            "provenance_traceability_ready",
        )
        dashboard_rag_ready = _ensure_bool(
            self.dashboard_rag_ready,
            "dashboard_rag_ready",
        )
        phase_core_ready = _ensure_bool(self.phase_core_ready, "phase_core_ready")

        if total_records <= 0:
            raise ValueError("total_records must be >= 1")
        if dashboard_visible_records != total_records:
            raise ValueError("all media records must be dashboard-visible")
        if retrieval_visible_records <= 0:
            raise ValueError("at least one media record must be retrieval-visible")
        if binary_external_records != total_records:
            raise ValueError("all media records must be binary_external")
        if provenance_required_records != total_records:
            raise ValueError("all media records must require provenance")
        if traceability_required_records != total_records:
            raise ValueError("all media records must require traceability")
        if approval_required_records <= 0:
            raise ValueError("at least one media record must require approval")
        if storage_bindings != total_records:
            raise ValueError("storage bindings must match total records")
        if storage_ready_bindings != storage_bindings:
            raise ValueError("all storage bindings must be ready")
        if binary_external_bindings != storage_bindings:
            raise ValueError("all storage bindings must remain binary_external")
        if not preview_ready:
            raise ValueError("preview_ready must be True")
        if not media_memory_ready:
            raise ValueError("media_memory_ready must be True")
        if not storage_binding_ready:
            raise ValueError("storage_binding_ready must be True")
        if not no_binary_payloads:
            raise ValueError("no_binary_payloads must be True")
        if not provenance_traceability_ready:
            raise ValueError("provenance_traceability_ready must be True")
        if not dashboard_rag_ready:
            raise ValueError("dashboard_rag_ready must be True")
        if not phase_core_ready:
            raise ValueError("phase_core_ready must be True")

        object.__setattr__(self, "total_records", total_records)
        object.__setattr__(self, "dashboard_visible_records", dashboard_visible_records)
        object.__setattr__(self, "retrieval_visible_records", retrieval_visible_records)
        object.__setattr__(self, "binary_external_records", binary_external_records)
        object.__setattr__(self, "provenance_required_records", provenance_required_records)
        object.__setattr__(self, "traceability_required_records", traceability_required_records)
        object.__setattr__(self, "approval_required_records", approval_required_records)
        object.__setattr__(self, "storage_bindings", storage_bindings)
        object.__setattr__(self, "storage_ready_bindings", storage_ready_bindings)
        object.__setattr__(self, "binary_external_bindings", binary_external_bindings)


def build_media_memory_phase_readiness() -> MediaMemoryPhaseReadiness:
    """Build final CORE-side PHASE 1.6 readiness gate."""

    read_model = build_media_artifact_memory_read_model()
    media_preview = build_media_memory_preview()
    storage_preview = build_media_storage_binding_preview()

    no_binary_payloads = (
        read_model.binary_external_records == read_model.total_records
        and storage_preview["binary_external_bindings"] == storage_preview["total_bindings"]
        and all(record.binary_external for record in read_model.records)
    )

    provenance_traceability_ready = (
        read_model.provenance_required_records == read_model.total_records
        and read_model.traceability_required_records == read_model.total_records
    )

    dashboard_rag_ready = (
        read_model.dashboard_visible_records == read_model.total_records
        and read_model.retrieval_visible_records >= 1
        and int(storage_preview["dashboard_visible_bindings"]) == read_model.total_records
        and int(storage_preview["retrieval_visible_bindings"]) >= 1
    )

    storage_binding_ready = (
        bool(storage_preview["binding_ready"])
        and int(storage_preview["total_bindings"]) == read_model.total_records
        and int(storage_preview["storage_ready_bindings"]) == read_model.total_records
    )

    phase_core_ready = (
        bool(media_preview["preview_ready"])
        and bool(media_preview["media_memory_ready"])
        and storage_binding_ready
        and no_binary_payloads
        and provenance_traceability_ready
        and dashboard_rag_ready
    )

    return MediaMemoryPhaseReadiness(
        total_records=read_model.total_records,
        dashboard_visible_records=read_model.dashboard_visible_records,
        retrieval_visible_records=read_model.retrieval_visible_records,
        binary_external_records=read_model.binary_external_records,
        provenance_required_records=read_model.provenance_required_records,
        traceability_required_records=read_model.traceability_required_records,
        approval_required_records=read_model.approval_required_records,
        storage_bindings=int(storage_preview["total_bindings"]),
        storage_ready_bindings=int(storage_preview["storage_ready_bindings"]),
        binary_external_bindings=int(storage_preview["binary_external_bindings"]),
        flow=_EXPECTED_MEDIA_MEMORY_FLOW,
        preview_ready=bool(media_preview["preview_ready"]),
        media_memory_ready=bool(media_preview["media_memory_ready"]),
        storage_binding_ready=storage_binding_ready,
        no_binary_payloads=no_binary_payloads,
        provenance_traceability_ready=provenance_traceability_ready,
        dashboard_rag_ready=dashboard_rag_ready,
        phase_core_ready=phase_core_ready,
    )
