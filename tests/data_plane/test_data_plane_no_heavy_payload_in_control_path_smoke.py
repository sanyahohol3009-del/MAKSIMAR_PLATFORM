from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.data_plane_payload_reference_models import (
    DataPlanePayloadReference,
    DataPlanePayloadReferenceKind,
)

ONE = "1" * 64


def test_payload_reference_blocks_heavy_payload_in_control_path() -> None:
    reference = DataPlanePayloadReference(
        reference_id="payload-storage-1",
        reference_kind=DataPlanePayloadReferenceKind.STORAGE_BACKEND,
        uri="storage://payload/1",
        sha256=ONE,
        size_bytes=2048,
        producer_layer_id="CONTROL_PLANE",
        trace_id="trace-payload-1",
        backend_id="postgres_main_metadata",
        content_type="application/json",
    )

    assert reference.heavy_payload_inline_allowed is False
    assert reference.control_path_payload_allowed is False
    assert reference.canonical_write_allowed is False


def test_payload_reference_rejects_control_path_payload() -> None:
    with pytest.raises(ValueError, match="control_path_payload_allowed"):
        DataPlanePayloadReference(
            reference_id="payload-bad-1",
            reference_kind=DataPlanePayloadReferenceKind.STORAGE_BACKEND,
            uri="storage://payload/1",
            sha256=ONE,
            size_bytes=2048,
            producer_layer_id="CONTROL_PLANE",
            trace_id="trace-bad",
            backend_id="postgres_main_metadata",
            content_type="application/json",
            control_path_payload_allowed=True,
        )
