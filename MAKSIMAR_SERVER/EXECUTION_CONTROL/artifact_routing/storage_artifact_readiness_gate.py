from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_phase_readiness,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.storage_registry_artifact_binding_preview import (
    build_storage_artifact_routing_binding_preview,
)


_EXPECTED_ARTIFACT_BINDING_FLOW = (
    "payload_classification",
    "artifact_routing",
    "storage_registry_lookup",
    "artifact_collection_binding",
    "data_plane_route_readiness",
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
class StorageArtifactPhaseReadiness:
    """Final SERVER-side readiness gate for PHASE 1.5 storage/artifact binding."""

    storage_core_entries: int
    artifact_binding_entries: int
    storage_required_entries: int
    storage_ready_entries: int
    data_plane_ready_entries: int
    dashboard_visible_entries: int
    artifact_flow: tuple[str, ...]
    storage_core_ready: bool
    artifact_binding_ready: bool
    data_plane_route_ready: bool
    dashboard_preview_ready: bool
    phase_ready: bool

    def __post_init__(self) -> None:
        storage_core_entries = _ensure_non_negative_int(
            self.storage_core_entries,
            "storage_core_entries",
        )
        artifact_binding_entries = _ensure_non_negative_int(
            self.artifact_binding_entries,
            "artifact_binding_entries",
        )
        storage_required_entries = _ensure_non_negative_int(
            self.storage_required_entries,
            "storage_required_entries",
        )
        storage_ready_entries = _ensure_non_negative_int(
            self.storage_ready_entries,
            "storage_ready_entries",
        )
        data_plane_ready_entries = _ensure_non_negative_int(
            self.data_plane_ready_entries,
            "data_plane_ready_entries",
        )
        dashboard_visible_entries = _ensure_non_negative_int(
            self.dashboard_visible_entries,
            "dashboard_visible_entries",
        )

        if tuple(self.artifact_flow) != _EXPECTED_ARTIFACT_BINDING_FLOW:
            raise ValueError("artifact_flow must match expected artifact binding flow")

        storage_core_ready = _ensure_bool(self.storage_core_ready, "storage_core_ready")
        artifact_binding_ready = _ensure_bool(
            self.artifact_binding_ready,
            "artifact_binding_ready",
        )
        data_plane_route_ready = _ensure_bool(
            self.data_plane_route_ready,
            "data_plane_route_ready",
        )
        dashboard_preview_ready = _ensure_bool(
            self.dashboard_preview_ready,
            "dashboard_preview_ready",
        )
        phase_ready = _ensure_bool(self.phase_ready, "phase_ready")

        if storage_core_entries <= 0:
            raise ValueError("storage_core_entries must be >= 1")
        if artifact_binding_entries <= 0:
            raise ValueError("artifact_binding_entries must be >= 1")
        if storage_required_entries <= 0:
            raise ValueError("storage_required_entries must be >= 1")
        if storage_ready_entries != storage_required_entries:
            raise ValueError("storage_ready_entries must match required entries")
        if data_plane_ready_entries != storage_required_entries:
            raise ValueError("data_plane_ready_entries must match required entries")
        if dashboard_visible_entries <= 0:
            raise ValueError("dashboard_visible_entries must be >= 1")
        if not storage_core_ready:
            raise ValueError("storage_core_ready must be True")
        if not artifact_binding_ready:
            raise ValueError("artifact_binding_ready must be True")
        if not data_plane_route_ready:
            raise ValueError("data_plane_route_ready must be True")
        if not dashboard_preview_ready:
            raise ValueError("dashboard_preview_ready must be True")
        if not phase_ready:
            raise ValueError("phase_ready must be True")

        object.__setattr__(self, "storage_core_entries", storage_core_entries)
        object.__setattr__(self, "artifact_binding_entries", artifact_binding_entries)
        object.__setattr__(self, "storage_required_entries", storage_required_entries)
        object.__setattr__(self, "storage_ready_entries", storage_ready_entries)
        object.__setattr__(self, "data_plane_ready_entries", data_plane_ready_entries)
        object.__setattr__(self, "dashboard_visible_entries", dashboard_visible_entries)


def build_storage_artifact_phase_readiness() -> StorageArtifactPhaseReadiness:
    """Build final SERVER-side PHASE 1.5 readiness gate."""

    storage_core = build_storage_registry_phase_readiness()
    binding_preview = build_storage_artifact_routing_binding_preview()

    storage_required_entries = int(binding_preview["storage_required_entries"])
    storage_ready_entries = int(binding_preview["storage_ready_entries"])
    data_plane_ready_entries = int(binding_preview["data_plane_ready_entries"])

    data_plane_route_ready = (
        storage_required_entries >= 1
        and storage_ready_entries == storage_required_entries
        and data_plane_ready_entries == storage_required_entries
    )

    phase_ready = (
        storage_core.phase_core_ready
        and bool(binding_preview["binding_ready"])
        and bool(binding_preview["preview_ready"])
        and data_plane_route_ready
    )

    return StorageArtifactPhaseReadiness(
        storage_core_entries=storage_core.total_entries,
        artifact_binding_entries=int(binding_preview["total_entries"]),
        storage_required_entries=storage_required_entries,
        storage_ready_entries=storage_ready_entries,
        data_plane_ready_entries=data_plane_ready_entries,
        dashboard_visible_entries=int(binding_preview["dashboard_visible_entries"]),
        artifact_flow=tuple(binding_preview["flow"]),
        storage_core_ready=storage_core.phase_core_ready,
        artifact_binding_ready=bool(binding_preview["binding_ready"]),
        data_plane_route_ready=data_plane_route_ready,
        dashboard_preview_ready=bool(binding_preview["preview_ready"]),
        phase_ready=phase_ready,
    )
