from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.portable_storage_reference_models import (
    PortableStorageReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_id_models import (
    StorageNodeId,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_models import (
    StorageNode,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_root_models import (
    StorageRoot,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.artifact_collection_models import (
    ArtifactCollectionReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.media_artifact_reference_models import (
    MediaArtifactReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.model_store_reference_models import (
    ModelStoreReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.retrieval_index_reference_models import (
    RetrievalIndexReference,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.storage_portability_policy_models import (
    StoragePortabilityPolicy,
)
from MAKSIMAR_CORE_LIB.memory_engine.storage_registry.storage_registry_models import (
    StorageRegistryContract,
    StorageRegistryEntry,
)


def _build_node(
    *,
    node_id: str,
    title: str,
    node_type: str,
    path_role: str,
) -> StorageNode:
    return StorageNode(
        storage_node_id=StorageNodeId(value=node_id),
        storage_node_type=node_type,
        title=title,
        path_role=path_role,
        readable_by_jarvis=True,
        writable_by_ingestion=False,
        portable=True,
        dashboard_ready=True,
    )


def build_storage_registry_contract() -> StorageRegistryContract:
    """Build read-only storage registry using existing storage primitives.

    The accepted history_ingestion StorageNodeId format is preserved. New logical
    stores are represented through PortableStorageReference metadata instead of
    inventing new StorageNodeId values.
    """

    history_node = _build_node(
        node_id="HSTORE-NORM-001",
        title="History Runtime Store",
        node_type="history_store",
        path_role="runtime_history_store",
    )

    history_root = StorageRoot(
        root_id="root_history_runtime_store",
        root_type="runtime_storage",
        root_path="runtime_history_store",
        portable=True,
        relocation_ready=True,
        nas_ready=True,
    )

    history_portable_ref = PortableStorageReference(
        storage_node_id="HSTORE-NORM-001",
        root_id="root_history_runtime_store",
        relative_path="normalized_history",
        portable=True,
        manifest_safe=True,
        nas_ready=True,
    )

    artifact_portable_ref = PortableStorageReference(
        storage_node_id="storage_node_artifact_store",
        root_id="root_artifact_store",
        relative_path="artifact_collections",
        portable=True,
        manifest_safe=True,
        nas_ready=True,
    )

    model_portable_ref = PortableStorageReference(
        storage_node_id="storage_node_model_store",
        root_id="root_model_store",
        relative_path="model_weights",
        portable=True,
        manifest_safe=True,
        nas_ready=True,
    )

    media_portable_ref = PortableStorageReference(
        storage_node_id="storage_node_media_store",
        root_id="root_media_store",
        relative_path="generated_media",
        portable=True,
        manifest_safe=True,
        nas_ready=True,
    )

    retrieval_portable_ref = PortableStorageReference(
        storage_node_id="storage_node_retrieval_index",
        root_id="root_retrieval_index",
        relative_path="retrieval_indexes",
        portable=True,
        manifest_safe=True,
        nas_ready=True,
    )

    entries = (
        StorageRegistryEntry(
            registry_id="storage_registry_history_store",
            entry_kind="history_storage_node",
            title="History Storage Node",
            storage_node=history_node,
            storage_root=history_root,
            portable_reference=history_portable_ref,
            dashboard_visible=True,
            retrieval_visible=True,
            relocation_ready=True,
            nas_ready=True,
        ),
        StorageRegistryEntry(
            registry_id="storage_registry_artifact_collection",
            entry_kind="artifact_collection",
            title="Artifact Collection Storage",
            storage_node=None,
            storage_root=None,
            portable_reference=artifact_portable_ref,
            dashboard_visible=True,
            retrieval_visible=False,
            relocation_ready=True,
            nas_ready=True,
        ),
        StorageRegistryEntry(
            registry_id="storage_registry_model_store",
            entry_kind="model_store",
            title="Model Store Storage",
            storage_node=None,
            storage_root=None,
            portable_reference=model_portable_ref,
            dashboard_visible=True,
            retrieval_visible=False,
            relocation_ready=True,
            nas_ready=True,
        ),
        StorageRegistryEntry(
            registry_id="storage_registry_media_artifact_store",
            entry_kind="media_artifact_store",
            title="Generated Media Storage",
            storage_node=None,
            storage_root=None,
            portable_reference=media_portable_ref,
            dashboard_visible=True,
            retrieval_visible=True,
            relocation_ready=True,
            nas_ready=True,
        ),
        StorageRegistryEntry(
            registry_id="storage_registry_retrieval_index",
            entry_kind="retrieval_index",
            title="Retrieval Index Storage",
            storage_node=None,
            storage_root=None,
            portable_reference=retrieval_portable_ref,
            dashboard_visible=True,
            retrieval_visible=True,
            relocation_ready=True,
            nas_ready=True,
        ),
    )

    return StorageRegistryContract(
        total_entries=len(entries),
        dashboard_visible_entries=sum(1 for entry in entries if entry.dashboard_visible),
        retrieval_visible_entries=sum(1 for entry in entries if entry.retrieval_visible),
        relocation_ready_entries=sum(1 for entry in entries if entry.relocation_ready),
        nas_ready_entries=sum(1 for entry in entries if entry.nas_ready),
        entries=entries,
    )


def build_artifact_collection_reference() -> ArtifactCollectionReference:
    return ArtifactCollectionReference(
        collection_id="artifact_collection_domain_artifacts",
        title="Domain Artifacts",
        storage_node_id="storage_node_artifact_store",
        artifact_kind="domain_artifacts",
        portable=True,
        dashboard_ready=True,
    )


def build_model_store_reference() -> ModelStoreReference:
    return ModelStoreReference(
        model_store_id="model_store_local_weights",
        title="Local Model Weights",
        storage_node_id="storage_node_model_store",
        model_family="local_llm",
        weights_external=True,
        portable=True,
    )


def build_media_artifact_reference() -> MediaArtifactReference:
    return MediaArtifactReference(
        media_store_id="media_store_generated_media",
        title="Generated Media Artifacts",
        storage_node_id="storage_node_media_store",
        media_kind="image_video_audio",
        raw_binary_external=True,
        retrieval_indexed=True,
    )


def build_retrieval_index_reference() -> RetrievalIndexReference:
    return RetrievalIndexReference(
        retrieval_index_id="retrieval_index_semantic_memory",
        title="Semantic Memory Retrieval Index",
        storage_node_id="storage_node_retrieval_index",
        backend_kind="sqlite_vec_or_vector_backend",
        rebuild_required=False,
        portable=True,
    )


def build_storage_portability_policy() -> StoragePortabilityPolicy:
    return StoragePortabilityPolicy(
        policy_id="storage_policy_portable_memory_artifacts",
        storage_node_portable=True,
        root_relocation_allowed=True,
        nas_ready_required=True,
        external_media_allowed=True,
        model_weights_external=True,
        retrieval_index_rebuild_allowed=True,
        atomic_snapshot_required=True,
    )


def build_storage_registry_preview() -> Dict[str, object]:
    contract = build_storage_registry_contract()
    artifact_collection = build_artifact_collection_reference()
    model_store = build_model_store_reference()
    media_store = build_media_artifact_reference()
    retrieval_index = build_retrieval_index_reference()
    policy = build_storage_portability_policy()

    return {
        "total_entries": contract.total_entries,
        "dashboard_visible_entries": contract.dashboard_visible_entries,
        "retrieval_visible_entries": contract.retrieval_visible_entries,
        "relocation_ready_entries": contract.relocation_ready_entries,
        "nas_ready_entries": contract.nas_ready_entries,
        "entry_kinds": tuple(sorted({entry.entry_kind for entry in contract.entries})),
        "artifact_collection_id": artifact_collection.collection_id,
        "model_store_id": model_store.model_store_id,
        "media_store_id": media_store.media_store_id,
        "retrieval_index_id": retrieval_index.retrieval_index_id,
        "portability_policy_id": policy.policy_id,
        "storage_ready_for_m2_nas": all(entry.nas_ready for entry in contract.entries),
        "preview_ready": True,
        "entries": tuple(
            {
                "registry_id": entry.registry_id,
                "entry_kind": entry.entry_kind,
                "title": entry.title,
                "dashboard_visible": entry.dashboard_visible,
                "retrieval_visible": entry.retrieval_visible,
                "relocation_ready": entry.relocation_ready,
                "nas_ready": entry.nas_ready,
            }
            for entry in contract.entries
        ),
    }
