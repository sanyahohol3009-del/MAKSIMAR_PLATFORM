from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.object_storage_models import (
    ObjectStorageArtifactReference,
    ObjectStorageReadinessReadModel,
)


def build_object_storage_artifact_reference(
    *,
    artifact_ref: str,
    object_storage_uri: str,
    backend_id: str,
    sha256: str,
    size_bytes: int,
    content_type: str,
    producer_layer_id: str,
    trace_id: str,
) -> ObjectStorageArtifactReference:
    return ObjectStorageArtifactReference(
        artifact_ref=artifact_ref,
        object_storage_uri=object_storage_uri,
        backend_id=backend_id,
        sha256=sha256,
        size_bytes=size_bytes,
        content_type=content_type,
        producer_layer_id=producer_layer_id,
        trace_id=trace_id,
    )


def build_object_storage_readiness_read_model(
    reference: ObjectStorageArtifactReference,
) -> ObjectStorageReadinessReadModel:
    if not isinstance(reference, ObjectStorageArtifactReference):
        raise TypeError("reference must be ObjectStorageArtifactReference")

    return ObjectStorageReadinessReadModel(
        backend_id=reference.backend_id,
        artifact_ref=reference.artifact_ref,
        object_storage_ready=True,
        reason_codes=("object_storage_artifact_reference_validated",),
    )
