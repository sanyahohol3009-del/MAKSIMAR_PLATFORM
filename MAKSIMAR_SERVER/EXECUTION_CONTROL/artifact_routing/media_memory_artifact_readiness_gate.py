from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_memory_phase_readiness,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing.media_memory_artifact_routing_binding_preview import (
    build_media_memory_artifact_routing_binding_preview,
)


_EXPECTED_MEDIA_ARTIFACT_ROUTING_FLOW = (
    "media_memory_read_model",
    "storage_registry_binding",
    "artifact_routing_binding",
    "data_plane_route_reference",
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
class MediaMemoryArtifactPhaseReadiness:
    """Final SERVER-side readiness gate for PHASE 1.6 media/artifact routing."""

    media_core_records: int
    artifact_route_entries: int
    route_required_entries: int
    route_ready_entries: int
    dashboard_visible_entries: int
    artifact_flow: tuple[str, ...]
    media_core_ready: bool
    artifact_routing_ready: bool
    data_plane_route_reference_ready: bool
    dashboard_preview_ready: bool
    no_manufacturing_authority: bool
    phase_ready: bool

    def __post_init__(self) -> None:
        media_core_records = _ensure_non_negative_int(
            self.media_core_records,
            "media_core_records",
        )
        artifact_route_entries = _ensure_non_negative_int(
            self.artifact_route_entries,
            "artifact_route_entries",
        )
        route_required_entries = _ensure_non_negative_int(
            self.route_required_entries,
            "route_required_entries",
        )
        route_ready_entries = _ensure_non_negative_int(
            self.route_ready_entries,
            "route_ready_entries",
        )
        dashboard_visible_entries = _ensure_non_negative_int(
            self.dashboard_visible_entries,
            "dashboard_visible_entries",
        )

        if tuple(self.artifact_flow) != _EXPECTED_MEDIA_ARTIFACT_ROUTING_FLOW:
            raise ValueError("artifact_flow must match expected PHASE 1.6 SERVER flow")

        media_core_ready = _ensure_bool(self.media_core_ready, "media_core_ready")
        artifact_routing_ready = _ensure_bool(
            self.artifact_routing_ready,
            "artifact_routing_ready",
        )
        data_plane_route_reference_ready = _ensure_bool(
            self.data_plane_route_reference_ready,
            "data_plane_route_reference_ready",
        )
        dashboard_preview_ready = _ensure_bool(
            self.dashboard_preview_ready,
            "dashboard_preview_ready",
        )
        no_manufacturing_authority = _ensure_bool(
            self.no_manufacturing_authority,
            "no_manufacturing_authority",
        )
        phase_ready = _ensure_bool(self.phase_ready, "phase_ready")

        if media_core_records <= 0:
            raise ValueError("media_core_records must be >= 1")
        if artifact_route_entries != media_core_records:
            raise ValueError("artifact_route_entries must match media_core_records")
        if route_required_entries <= 0:
            raise ValueError("route_required_entries must be >= 1")
        if route_ready_entries != route_required_entries:
            raise ValueError("all required routes must be ready")
        if dashboard_visible_entries != artifact_route_entries:
            raise ValueError("all artifact route entries must be dashboard-visible")
        if not media_core_ready:
            raise ValueError("media_core_ready must be True")
        if not artifact_routing_ready:
            raise ValueError("artifact_routing_ready must be True")
        if not data_plane_route_reference_ready:
            raise ValueError("data_plane_route_reference_ready must be True")
        if not dashboard_preview_ready:
            raise ValueError("dashboard_preview_ready must be True")
        if not no_manufacturing_authority:
            raise ValueError("no_manufacturing_authority must be True")
        if not phase_ready:
            raise ValueError("phase_ready must be True")

        object.__setattr__(self, "media_core_records", media_core_records)
        object.__setattr__(self, "artifact_route_entries", artifact_route_entries)
        object.__setattr__(self, "route_required_entries", route_required_entries)
        object.__setattr__(self, "route_ready_entries", route_ready_entries)
        object.__setattr__(self, "dashboard_visible_entries", dashboard_visible_entries)


def build_media_memory_artifact_phase_readiness() -> MediaMemoryArtifactPhaseReadiness:
    """Build final SERVER-side PHASE 1.6 readiness gate."""

    media_core = build_media_memory_phase_readiness()
    routing_preview = build_media_memory_artifact_routing_binding_preview()

    route_required_entries = int(routing_preview["route_required_entries"])
    route_ready_entries = int(routing_preview["route_ready_entries"])

    data_plane_route_reference_ready = (
        route_required_entries >= 1
        and route_ready_entries == route_required_entries
    )

    no_manufacturing_authority = True

    phase_ready = (
        media_core.phase_core_ready
        and bool(routing_preview["binding_ready"])
        and bool(routing_preview["preview_ready"])
        and data_plane_route_reference_ready
        and no_manufacturing_authority
    )

    return MediaMemoryArtifactPhaseReadiness(
        media_core_records=media_core.total_records,
        artifact_route_entries=int(routing_preview["total_entries"]),
        route_required_entries=route_required_entries,
        route_ready_entries=route_ready_entries,
        dashboard_visible_entries=int(routing_preview["dashboard_visible_entries"]),
        artifact_flow=tuple(routing_preview["flow"]),
        media_core_ready=media_core.phase_core_ready,
        artifact_routing_ready=bool(routing_preview["binding_ready"]),
        data_plane_route_reference_ready=data_plane_route_reference_ready,
        dashboard_preview_ready=bool(routing_preview["preview_ready"]),
        no_manufacturing_authority=no_manufacturing_authority,
        phase_ready=phase_ready,
    )
