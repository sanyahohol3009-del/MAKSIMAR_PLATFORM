from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.media_memory.artifact_dedup_models import (
    ArtifactDedupContract,
    ArtifactDedupDecision,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.dataset_artifact_models import (
    DatasetArtifactMemory,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.generated_media_metadata_models import (
    GeneratedMediaMetadata,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.media_memory_read_model import (
    build_media_artifact_memory_read_model,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.model_weight_artifact_models import (
    ModelWeightArtifactMemory,
)
from MAKSIMAR_CORE_LIB.memory_engine.media_memory.project_output_artifact_models import (
    ProjectOutputArtifactMemory,
)


def build_generated_media_metadata() -> GeneratedMediaMetadata:
    return GeneratedMediaMetadata(
        generated_media_id="generated_media_image_001",
        prompt_ref="prompt://content_media/image_001",
        template_ref="template://content_media/visual_template_001",
        render_trace_ref="trace://render/image_001",
        output_artifact_ref="artifact://media/generated/image_001.png",
        template_binding_required=True,
        render_artifact_logging_required=True,
        provenance_visible=True,
    )


def build_model_weight_artifact_memory() -> ModelWeightArtifactMemory:
    return ModelWeightArtifactMemory(
        model_weight_id="model_weight_qwen_coder",
        model_family="qwen",
        model_role="local_code_generation",
        weight_artifact_ref="artifact://models/local/qwen_coder.gguf",
        model_store_id="model_store_local_weights",
        binary_external=True,
        checksum_required=True,
        license_review_required=True,
    )


def build_dataset_artifact_memory() -> DatasetArtifactMemory:
    return DatasetArtifactMemory(
        dataset_artifact_id="dataset_artifact_visual_sources",
        dataset_ref="artifact://datasets/visual/source_dataset_001",
        source_type="imported_dataset",
        provenance_ref="provenance://datasets/visual/source_dataset_001",
        imported_dataset=True,
        review_required_before_trust=True,
        retrieval_index_allowed=True,
    )


def build_project_output_artifact_memory() -> ProjectOutputArtifactMemory:
    return ProjectOutputArtifactMemory(
        project_output_id="project_output_image_to_3d_proposal",
        output_kind="image_to_3d_proposal",
        artifact_ref="artifact://engineering/stl/part_001.stl",
        source_ref="visual_engineering://image_to_3d/proposal_001",
        validation_ref="validation://geometry/proposal_001",
        geometry_validation_required=True,
        simulation_recommended=True,
        manufacturing_authority_granted=False,
    )


def build_artifact_dedup_contract() -> ArtifactDedupContract:
    decisions = (
        ArtifactDedupDecision(
            artifact_id="media_artifact_generated_image",
            artifact_fingerprint="sha256:" + "a" * 64,
            status="existing_artifact",
            existing_record_ref="media_memory://media_artifact_generated_image",
            write_allowed=False,
            rewrite_forbidden=True,
        ),
        ArtifactDedupDecision(
            artifact_id="media_artifact_generated_video",
            artifact_fingerprint="sha256:" + "b" * 64,
            status="new_artifact_candidate",
            existing_record_ref="",
            write_allowed=True,
            rewrite_forbidden=False,
        ),
    )

    return ArtifactDedupContract(
        total_decisions=len(decisions),
        existing_artifacts=sum(1 for decision in decisions if decision.status == "existing_artifact"),
        new_artifact_candidates=sum(1 for decision in decisions if decision.status == "new_artifact_candidate"),
        write_allowed_candidates=sum(1 for decision in decisions if decision.write_allowed),
        rewrite_forbidden_existing=sum(1 for decision in decisions if decision.rewrite_forbidden),
        decisions=decisions,
    )


def build_media_memory_summary() -> Dict[str, object]:
    read_model = build_media_artifact_memory_read_model()
    generated = build_generated_media_metadata()
    model_weight = build_model_weight_artifact_memory()
    dataset = build_dataset_artifact_memory()
    project_output = build_project_output_artifact_memory()
    dedup = build_artifact_dedup_contract()

    return {
        "total_records": read_model.total_records,
        "dashboard_visible_records": read_model.dashboard_visible_records,
        "retrieval_visible_records": read_model.retrieval_visible_records,
        "binary_external_records": read_model.binary_external_records,
        "provenance_required_records": read_model.provenance_required_records,
        "traceability_required_records": read_model.traceability_required_records,
        "approval_required_records": read_model.approval_required_records,
        "generated_media_id": generated.generated_media_id,
        "model_weight_id": model_weight.model_weight_id,
        "dataset_artifact_id": dataset.dataset_artifact_id,
        "project_output_id": project_output.project_output_id,
        "existing_artifacts": dedup.existing_artifacts,
        "new_artifact_candidates": dedup.new_artifact_candidates,
        "write_allowed_candidates": dedup.write_allowed_candidates,
        "rewrite_forbidden_existing": dedup.rewrite_forbidden_existing,
        "media_memory_summary_ready": True,
    }
