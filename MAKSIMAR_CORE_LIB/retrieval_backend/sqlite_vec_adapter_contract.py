from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.retrieval_backend.evidence_binding_contract import (
    EvidenceBoundRetrievalResult,
)
from MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_backend_adapter_contract import (
    RetrievalBackendAdapterContract,
)
from MAKSIMAR_CORE_LIB.retrieval_backend.vector_backend_contract import VectorBackendContract


SQLITE_VEC_BACKEND_KIND = "sqlite_vec"
RETRIEVAL_ADAPTER_CONTRACT_MODE = "adapter_only"


def _require_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")
    return value


def _require_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


@dataclass(frozen=True, slots=True)
class SqliteVecAdapterContract:
    adapter_id: str = "retrieval_backend_adapter_sqlite_vec"
    backend_kind: str = SQLITE_VEC_BACKEND_KIND
    contract_mode: str = RETRIEVAL_ADAPTER_CONTRACT_MODE
    vector_metadata_adapter: bool = True
    database_runtime_enabled: bool = False
    direct_database_write_allowed: bool = False
    direct_write_allowed: bool = False
    source_of_truth: bool = False
    output_requires_normalization: bool = True
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    runtime_mutation_allowed: bool = False
    network_allowed_by_default: bool = False

    def __post_init__(self) -> None:
        adapter_id = _require_text(self.adapter_id, "adapter_id")
        backend_kind = _require_text(self.backend_kind, "backend_kind")
        contract_mode = _require_text(self.contract_mode, "contract_mode")
        if backend_kind != SQLITE_VEC_BACKEND_KIND:
            raise ValueError("backend_kind must be sqlite_vec")
        if contract_mode != RETRIEVAL_ADAPTER_CONTRACT_MODE:
            raise ValueError(f"contract_mode must be {RETRIEVAL_ADAPTER_CONTRACT_MODE}")

        for field_name in (
            "vector_metadata_adapter",
            "database_runtime_enabled",
            "direct_database_write_allowed",
            "direct_write_allowed",
            "source_of_truth",
            "output_requires_normalization",
            "source_ref_required",
            "evidence_binding_required",
            "runtime_mutation_allowed",
            "network_allowed_by_default",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if not self.vector_metadata_adapter:
            raise ValueError("vector_metadata_adapter must be True")
        if self.database_runtime_enabled:
            raise ValueError("database_runtime_enabled must be False")
        if self.direct_database_write_allowed:
            raise ValueError("direct_database_write_allowed must be False")
        if self.direct_write_allowed:
            raise ValueError("direct_write_allowed must be False")
        if self.source_of_truth:
            raise ValueError("source_of_truth must be False")
        if not self.output_requires_normalization:
            raise ValueError("output_requires_normalization must be True")
        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.network_allowed_by_default:
            raise ValueError("network_allowed_by_default must be False")

        object.__setattr__(self, "adapter_id", adapter_id)
        object.__setattr__(self, "backend_kind", backend_kind)
        object.__setattr__(self, "contract_mode", contract_mode)

    def to_base_adapter_contract(self) -> RetrievalBackendAdapterContract:
        return RetrievalBackendAdapterContract(
            adapter_id=self.adapter_id,
            backend_kind="sqlite_vec",
            adapter_mode="adapter_only",
            truth_status="not_source_of_truth",
            allowed_domains=("project_history", "technical_memory"),
        )

    def to_vector_backend_contract(self) -> VectorBackendContract:
        return VectorBackendContract(
            vector_backend_id="vector_backend_sqlite_vec",
            backend_kind="sqlite_vec",
            namespace_id="retrieval_backend_contracts",
            embedding_model_ref="model://retrieval-backend/metadata-only",
            dimension=384,
            supported_capabilities=("embedding_metadata", "search_metadata"),
        )

    def validate_output(self, result: EvidenceBoundRetrievalResult) -> EvidenceBoundRetrievalResult:
        return self.to_base_adapter_contract().validate_result(result)

    def to_read_model(self) -> dict[str, object]:
        return {
            "adapter_id": self.adapter_id,
            "backend_kind": self.backend_kind,
            "contract_mode": self.contract_mode,
            "vector_metadata_adapter": self.vector_metadata_adapter,
            "database_runtime_enabled": self.database_runtime_enabled,
            "direct_database_write_allowed": self.direct_database_write_allowed,
            "direct_write_allowed": self.direct_write_allowed,
            "source_of_truth": self.source_of_truth,
            "output_requires_normalization": self.output_requires_normalization,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "vector_backend": self.to_vector_backend_contract().to_read_model(),
        }


def build_sqlite_vec_adapter_contract() -> SqliteVecAdapterContract:
    return SqliteVecAdapterContract()


__all__ = [
    "SQLITE_VEC_BACKEND_KIND",
    "SqliteVecAdapterContract",
    "build_sqlite_vec_adapter_contract",
]
