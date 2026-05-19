from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.data_plane.object_storage_contract import (
    build_object_storage_artifact_reference,
    build_object_storage_readiness_read_model,
)
from MAKSIMAR_CORE_LIB.data_plane.object_storage_models import ObjectStorageArtifactReference

ONE = "1" * 64


def test_object_storage_reference_is_reference_only() -> None:
    reference = build_object_storage_artifact_reference(
        artifact_ref="artifact://payload/1",
        object_storage_uri="object://bucket/payload/1",
        backend_id="object_storage_primary",
        sha256=ONE,
        size_bytes=128,
        content_type="application/json",
        producer_layer_id="DATA_PLANE",
        trace_id="trace-object-1",
    )
    read_model = build_object_storage_readiness_read_model(reference)

    assert reference.inline_payload_allowed is False
    assert reference.control_path_payload_allowed is False
    assert reference.canonical_write_allowed is False
    assert read_model.object_storage_ready is True


def test_object_storage_rejects_inline_payload() -> None:
    with pytest.raises(ValueError, match="inline_payload_allowed"):
        ObjectStorageArtifactReference(
            artifact_ref="artifact://bad",
            object_storage_uri="object://bad",
            backend_id="object_storage_primary",
            sha256=ONE,
            size_bytes=1,
            content_type="text/plain",
            producer_layer_id="DATA_PLANE",
            trace_id="trace-bad",
            inline_payload_allowed=True,
        )
