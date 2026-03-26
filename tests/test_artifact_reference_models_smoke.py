from __future__ import annotations

from MAKSIMAR_CORE_LIB.artifact_reference_models import (
    ArtifactReferenceContract,
    ArtifactReferenceEntry,
)


def test_artifact_reference_models_build() -> None:
    """Artifact reference models should build successfully."""
    contract = ArtifactReferenceContract(
        total_references=2,
        references=(
            ArtifactReferenceEntry(
                artifact_ref="artifact://simulation/output_001",
                artifact_type="simulation_output",
                artifact_size_kb=2048,
                owner_task_id="task_sim_001",
                storage_policy="retained",
                integrity_policy="checksum_required",
            ),
            ArtifactReferenceEntry(
                artifact_ref="artifact://logs/runtime_001",
                artifact_type="runtime_log_bundle",
                artifact_size_kb=512,
                owner_task_id="task_runtime_001",
                storage_policy="ephemeral",
                integrity_policy="signature_required",
            ),
        ),
    )

    assert contract.total_references == 2
    assert len(contract.references) == 2
    assert contract.references[0].artifact_type == "simulation_output"
    assert contract.references[-1].artifact_type == "runtime_log_bundle"


def test_artifact_reference_models_preserve_routing_metadata() -> None:
    """Artifact reference models should preserve storage and integrity metadata."""
    contract = ArtifactReferenceContract(
        total_references=1,
        references=(
            ArtifactReferenceEntry(
                artifact_ref="artifact://dataset/chunk_001",
                artifact_type="dataset_chunk",
                artifact_size_kb=8192,
                owner_task_id="task_data_001",
                storage_policy="archival",
                integrity_policy="signature_required",
            ),
        ),
    )

    entry = contract.references[0]

    assert entry.artifact_ref == "artifact://dataset/chunk_001"
    assert entry.storage_policy == "archival"
    assert entry.integrity_policy == "signature_required"
    assert entry.artifact_size_kb == 8192
