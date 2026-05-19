from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)


class DataPlaneRouteTarget(str, Enum):
    STORAGE_BACKEND = "storage_backend"
    OBJECT_STORAGE = "object_storage"
    VECTOR_STORE = "vector_store"
    MEMORY_INDEX = "memory_index"


@dataclass(frozen=True, slots=True)
class DataPlaneRouteDecision:
    route_id: str
    target: DataPlaneRouteTarget
    payload_reference: DataPlanePayloadReference
    accepted: bool
    reason_codes: tuple[str, ...]
    dashboard_safe: bool = True
    heavy_payload_in_control_path_allowed: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        if not self.route_id:
            raise ValueError("route_id must not be empty")
        if not isinstance(self.target, DataPlaneRouteTarget):
            raise TypeError("target must be DataPlaneRouteTarget")
        if not isinstance(self.payload_reference, DataPlanePayloadReference):
            raise TypeError("payload_reference must be DataPlanePayloadReference")
        if not isinstance(self.reason_codes, tuple):
            raise TypeError("reason_codes must be a tuple")
        if not self.reason_codes:
            raise ValueError("reason_codes must not be empty")
        if not self.accepted:
            raise ValueError("route decision must be accepted only after reference validation")
        if not self.dashboard_safe:
            raise ValueError("dashboard_safe must remain true")
        if self.heavy_payload_in_control_path_allowed:
            raise ValueError("heavy_payload_in_control_path_allowed must remain false")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must remain false")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must remain false")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["target"] = self.target.value
        payload["payload_reference"] = self.payload_reference.to_dict()
        return payload


def resolve_data_plane_route(
    *,
    route_id: str,
    target: DataPlaneRouteTarget,
    payload_reference: DataPlanePayloadReference,
) -> DataPlaneRouteDecision:
    if target is DataPlaneRouteTarget.STORAGE_BACKEND:
        expected_kind = DataPlanePayloadReferenceKind.STORAGE_BACKEND
    elif target is DataPlaneRouteTarget.OBJECT_STORAGE:
        expected_kind = DataPlanePayloadReferenceKind.OBJECT_ARTIFACT
    elif target is DataPlaneRouteTarget.VECTOR_STORE:
        expected_kind = DataPlanePayloadReferenceKind.VECTOR_RECORD
    elif target is DataPlaneRouteTarget.MEMORY_INDEX:
        expected_kind = DataPlanePayloadReferenceKind.MEMORY_INDEX_ENTRY
    else:
        raise ValueError("unsupported data plane route target")

    if payload_reference.reference_kind is not expected_kind:
        raise ValueError("payload reference kind does not match route target")

    return DataPlaneRouteDecision(
        route_id=route_id,
        target=target,
        payload_reference=payload_reference,
        accepted=True,
        reason_codes=("data_plane_route_accepted_reference_only",),
    )
