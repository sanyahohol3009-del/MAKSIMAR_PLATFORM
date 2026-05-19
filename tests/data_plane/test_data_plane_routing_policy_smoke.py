from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)
from MAKSIMAR_CORE_LIB.data_plane.data_plane_routing_policy import (
    DataPlaneRouteTarget,
    resolve_data_plane_route,
)

ONE = "1" * 64


def test_data_plane_route_accepts_matching_reference_kind() -> None:
    reference = DataPlanePayloadReference(
        reference_id="payload-object-1",
        reference_kind=DataPlanePayloadReferenceKind.OBJECT_ARTIFACT,
        uri="object://payload/1",
        sha256=ONE,
        size_bytes=128,
        producer_layer_id="CONTROL_PLANE",
        trace_id="trace-route-1",
        backend_id="object_storage_primary",
        content_type="application/json",
    )

    decision = resolve_data_plane_route(
        route_id="route-object-1",
        target=DataPlaneRouteTarget.OBJECT_STORAGE,
        payload_reference=reference,
    )

    assert decision.accepted is True
    assert decision.heavy_payload_in_control_path_allowed is False
    assert decision.canonical_write_allowed is False


def test_data_plane_route_rejects_mismatched_reference_kind() -> None:
    reference = DataPlanePayloadReference(
        reference_id="payload-vector-1",
        reference_kind=DataPlanePayloadReferenceKind.VECTOR_RECORD,
        uri="vector://payload/1",
        sha256=ONE,
        size_bytes=128,
        producer_layer_id="CONTROL_PLANE",
        trace_id="trace-route-1",
        backend_id="vector_store_policy_surface",
        content_type="application/vector-ref",
    )

    with pytest.raises(ValueError, match="does not match"):
        resolve_data_plane_route(
            route_id="route-bad-1",
            target=DataPlaneRouteTarget.OBJECT_STORAGE,
            payload_reference=reference,
        )
