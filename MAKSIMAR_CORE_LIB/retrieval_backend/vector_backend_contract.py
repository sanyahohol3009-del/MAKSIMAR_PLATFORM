from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.data_plane.vector_store_models import VectorStoreBackendKind


VectorBackendKind = Literal["qdrant", "sqlite_vec", "in_memory_reference"]


_VECTOR_BACKEND_ID_PATTERN = re.compile(r"^vector_backend_[a-z][a-z0-9_]*$")


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _require_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")
    return value


def _require_positive_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be int")
    if value <= 0:
        raise ValueError(f"{field_name} must be > 0")
    return value


def _normalize_text_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


@dataclass(frozen=True, slots=True)
class VectorBackendContract:
    vector_backend_id: str
    backend_kind: VectorBackendKind
    namespace_id: str
    embedding_model_ref: str
    dimension: int
    supported_capabilities: tuple[str, ...]
    supports_embeddings_metadata: bool = True
    supports_search_metadata: bool = True
    metadata_only: bool = True
    adapter_only: bool = True
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    source_of_truth: bool = False
    direct_write_allowed: bool = False
    network_allowed_by_default: bool = False
    runtime_mutation_allowed: bool = False
    canonical_write_allowed: bool = False

    def __post_init__(self) -> None:
        vector_backend_id = _require_non_empty_text(self.vector_backend_id, "vector_backend_id")
        backend_kind = _require_non_empty_text(self.backend_kind, "backend_kind")
        namespace_id = _require_non_empty_text(self.namespace_id, "namespace_id")
        embedding_model_ref = _require_non_empty_text(self.embedding_model_ref, "embedding_model_ref")
        dimension = _require_positive_int(self.dimension, "dimension")
        supported_capabilities = _normalize_text_tuple(
            self.supported_capabilities,
            "supported_capabilities",
        )

        if not _VECTOR_BACKEND_ID_PATTERN.fullmatch(vector_backend_id):
            raise ValueError(f"Invalid vector_backend_id: {vector_backend_id}")
        if backend_kind not in VectorBackendKind.__args__:
            raise ValueError(f"unsupported backend_kind: {backend_kind}")

        for field_name in (
            "supports_embeddings_metadata",
            "supports_search_metadata",
            "metadata_only",
            "adapter_only",
            "source_ref_required",
            "evidence_binding_required",
            "source_of_truth",
            "direct_write_allowed",
            "network_allowed_by_default",
            "runtime_mutation_allowed",
            "canonical_write_allowed",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if not self.supports_embeddings_metadata:
            raise ValueError("supports_embeddings_metadata must be True")
        if not self.supports_search_metadata:
            raise ValueError("supports_search_metadata must be True")
        if not self.metadata_only:
            raise ValueError("metadata_only must be True")
        if not self.adapter_only:
            raise ValueError("adapter_only must be True")
        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if self.source_of_truth:
            raise ValueError("source_of_truth must be False")
        if self.direct_write_allowed:
            raise ValueError("direct_write_allowed must be False")
        if self.network_allowed_by_default:
            raise ValueError("network_allowed_by_default must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")

        object.__setattr__(self, "vector_backend_id", vector_backend_id)
        object.__setattr__(self, "backend_kind", backend_kind)
        object.__setattr__(self, "namespace_id", namespace_id)
        object.__setattr__(self, "embedding_model_ref", embedding_model_ref)
        object.__setattr__(self, "dimension", dimension)
        object.__setattr__(self, "supported_capabilities", supported_capabilities)

    def vector_store_backend_kind(self) -> VectorStoreBackendKind:
        if self.backend_kind == "qdrant":
            return VectorStoreBackendKind.QDRANT
        if self.backend_kind == "sqlite_vec":
            return VectorStoreBackendKind.SQLITE_VEC
        return VectorStoreBackendKind.CONTRACT_ONLY

    def to_read_model(self) -> dict[str, object]:
        return {
            "vector_backend_id": self.vector_backend_id,
            "backend_kind": self.backend_kind,
            "vector_store_backend_kind": self.vector_store_backend_kind().value,
            "namespace_id": self.namespace_id,
            "embedding_model_ref": self.embedding_model_ref,
            "dimension": self.dimension,
            "supported_capabilities": self.supported_capabilities,
            "supports_embeddings_metadata": self.supports_embeddings_metadata,
            "supports_search_metadata": self.supports_search_metadata,
            "metadata_only": self.metadata_only,
            "adapter_only": self.adapter_only,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "source_of_truth": self.source_of_truth,
            "direct_write_allowed": self.direct_write_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
        }


def build_default_vector_backend_contract() -> VectorBackendContract:
    return VectorBackendContract(
        vector_backend_id="vector_backend_in_memory_reference",
        backend_kind="in_memory_reference",
        namespace_id="retrieval_backend_contracts",
        embedding_model_ref="model://ollama/local/embed-read-model",
        dimension=384,
        supported_capabilities=("embedding_metadata", "search_metadata"),
    )


__all__ = [
    "VectorBackendContract",
    "VectorBackendKind",
    "build_default_vector_backend_contract",
]
