from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import MediaArtifactMemoryRecord


def test_media_artifact_models_smoke() -> None:
    record = MediaArtifactMemoryRecord(
        artifact_id="media_artifact_generated_image",
        artifact_ref="artifact://media/generated/image_001.png",
        artifact_kind="generated_image",
        title="Generated Image Artifact",
        source_ref="prompt://content_media/image_001",
        storage_registry_id="storage_registry_media_artifact_store",
        storage_node_id="storage_node_media_store",
        provenance_required=True,
        traceability_required=True,
        approval_required=False,
        binary_external=True,
        dashboard_visible=True,
        retrieval_visible=True,
    )

    assert record.binary_external is True
    assert record.dashboard_visible is True
