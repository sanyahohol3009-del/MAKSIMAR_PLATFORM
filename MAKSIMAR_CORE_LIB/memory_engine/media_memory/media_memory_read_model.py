from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_artifact_models import (
    MediaArtifactMemoryRecord,
)


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True, slots=True)
class MediaArtifactMemoryReadModel:
    """Read-only model for media/model/artifact memory dashboard and retrieval."""

    total_records: int
    dashboard_visible_records: int
    retrieval_visible_records: int
    binary_external_records: int
    provenance_required_records: int
    traceability_required_records: int
    approval_required_records: int
    records: tuple[MediaArtifactMemoryRecord, ...]

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

        if total_records != len(self.records):
            raise ValueError("total_records must match records length")

        if dashboard_visible_records != sum(1 for record in self.records if record.dashboard_visible):
            raise ValueError("dashboard_visible_records must match computed count")

        if retrieval_visible_records != sum(1 for record in self.records if record.retrieval_visible):
            raise ValueError("retrieval_visible_records must match computed count")

        if binary_external_records != sum(1 for record in self.records if record.binary_external):
            raise ValueError("binary_external_records must match computed count")

        if provenance_required_records != sum(1 for record in self.records if record.provenance_required):
            raise ValueError("provenance_required_records must match computed count")

        if traceability_required_records != sum(1 for record in self.records if record.traceability_required):
            raise ValueError("traceability_required_records must match computed count")

        if approval_required_records != sum(1 for record in self.records if record.approval_required):
            raise ValueError("approval_required_records must match computed count")

        artifact_ids = tuple(record.artifact_id for record in self.records)
        if len(set(artifact_ids)) != len(artifact_ids):
            raise ValueError("duplicate artifact_id values detected")

        object.__setattr__(self, "total_records", total_records)
        object.__setattr__(self, "dashboard_visible_records", dashboard_visible_records)
        object.__setattr__(self, "retrieval_visible_records", retrieval_visible_records)
        object.__setattr__(self, "binary_external_records", binary_external_records)
        object.__setattr__(self, "provenance_required_records", provenance_required_records)
        object.__setattr__(self, "traceability_required_records", traceability_required_records)
        object.__setattr__(self, "approval_required_records", approval_required_records)


def build_media_artifact_memory_records() -> tuple[MediaArtifactMemoryRecord, ...]:
    return (
        MediaArtifactMemoryRecord(
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
        ),
        MediaArtifactMemoryRecord(
            artifact_id="media_artifact_generated_video",
            artifact_ref="artifact://media/generated/video_001.mp4",
            artifact_kind="generated_video",
            title="Generated Video Artifact",
            source_ref="prompt://content_media/video_001",
            storage_registry_id="storage_registry_media_artifact_store",
            storage_node_id="storage_node_media_store",
            provenance_required=True,
            traceability_required=True,
            approval_required=True,
            binary_external=True,
            dashboard_visible=True,
            retrieval_visible=True,
        ),
        MediaArtifactMemoryRecord(
            artifact_id="media_artifact_model_weight",
            artifact_ref="artifact://models/local/qwen_coder.gguf",
            artifact_kind="model_weight",
            title="Local Model Weight Artifact",
            source_ref="model_source://local/qwen_coder",
            storage_registry_id="storage_registry_model_store",
            storage_node_id="storage_node_model_store",
            provenance_required=True,
            traceability_required=True,
            approval_required=True,
            binary_external=True,
            dashboard_visible=True,
            retrieval_visible=False,
        ),
        MediaArtifactMemoryRecord(
            artifact_id="media_artifact_dataset_visual",
            artifact_ref="artifact://datasets/visual/source_dataset_001",
            artifact_kind="dataset_asset",
            title="Visual Dataset Artifact",
            source_ref="dataset_source://visual/imported_001",
            storage_registry_id="storage_registry_retrieval_index",
            storage_node_id="storage_node_retrieval_index",
            provenance_required=True,
            traceability_required=True,
            approval_required=True,
            binary_external=True,
            dashboard_visible=True,
            retrieval_visible=True,
        ),
        MediaArtifactMemoryRecord(
            artifact_id="media_artifact_project_stl",
            artifact_ref="artifact://engineering/stl/part_001.stl",
            artifact_kind="stl_file",
            title="Project STL Artifact",
            source_ref="visual_engineering://image_to_3d/proposal_001",
            storage_registry_id="storage_registry_artifact_collection",
            storage_node_id="storage_node_artifact_store",
            provenance_required=True,
            traceability_required=True,
            approval_required=True,
            binary_external=True,
            dashboard_visible=True,
            retrieval_visible=True,
        ),
        MediaArtifactMemoryRecord(
            artifact_id="media_artifact_simulation_output",
            artifact_ref="artifact://simulation/output/run_001.json",
            artifact_kind="simulation_output",
            title="Simulation Output Artifact",
            source_ref="simulation://candidate/run_001",
            storage_registry_id="storage_registry_artifact_collection",
            storage_node_id="storage_node_artifact_store",
            provenance_required=True,
            traceability_required=True,
            approval_required=False,
            binary_external=True,
            dashboard_visible=True,
            retrieval_visible=True,
        ),
    )


def build_media_artifact_memory_read_model() -> MediaArtifactMemoryReadModel:
    records = build_media_artifact_memory_records()

    return MediaArtifactMemoryReadModel(
        total_records=len(records),
        dashboard_visible_records=sum(1 for record in records if record.dashboard_visible),
        retrieval_visible_records=sum(1 for record in records if record.retrieval_visible),
        binary_external_records=sum(1 for record in records if record.binary_external),
        provenance_required_records=sum(1 for record in records if record.provenance_required),
        traceability_required_records=sum(1 for record in records if record.traceability_required),
        approval_required_records=sum(1 for record in records if record.approval_required),
        records=records,
    )
