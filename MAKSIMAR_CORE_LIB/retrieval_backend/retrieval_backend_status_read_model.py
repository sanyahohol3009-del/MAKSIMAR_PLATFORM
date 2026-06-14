from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_CORE_LIB.retrieval_backend.mgrep_adapter_contract import (
    MgrepAdapterContract,
    build_mgrep_adapter_contract,
)
from MAKSIMAR_CORE_LIB.retrieval_backend.qdrant_adapter_contract import (
    QdrantAdapterContract,
    build_qdrant_adapter_contract,
)
from MAKSIMAR_CORE_LIB.retrieval_backend.sqlite_vec_adapter_contract import (
    SqliteVecAdapterContract,
    build_sqlite_vec_adapter_contract,
)


SUPPORTED_RETRIEVAL_BACKEND_KINDS: tuple[str, ...] = ("mgrep", "sqlite_vec", "qdrant")
RETRIEVAL_BACKEND_STATUS_MODEL_ID = "retrieval_backend_status_read_model_phase_7_3"
RETRIEVAL_BACKEND_STATUS_MODE = "read_model_preview_only"


def _require_text(value: str, field_name: str) -> str:
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


def _normalize_adapter_statuses(values: tuple["RetrievalBackendAdapterStatus", ...]) -> tuple["RetrievalBackendAdapterStatus", ...]:
    if not isinstance(values, tuple):
        raise TypeError("adapter_statuses must be a tuple")
    if not values:
        raise ValueError("adapter_statuses must not be empty")
    for value in values:
        if not isinstance(value, RetrievalBackendAdapterStatus):
            raise TypeError("adapter_statuses entries must be RetrievalBackendAdapterStatus")
    backend_kinds = tuple(value.backend_kind for value in values)
    if backend_kinds != SUPPORTED_RETRIEVAL_BACKEND_KINDS:
        raise ValueError(f"adapter_statuses must be ordered as {SUPPORTED_RETRIEVAL_BACKEND_KINDS}")
    if len({value.adapter_id for value in values}) != len(values):
        raise ValueError("adapter_statuses must not contain duplicate adapter_id values")
    return values


@dataclass(frozen=True, slots=True)
class RetrievalBackendAdapterStatus:
    adapter_id: str
    backend_kind: str
    contract_mode: str
    source_of_truth: bool
    output_requires_normalization: bool
    source_ref_required: bool
    evidence_binding_required: bool
    execution_allowed_now: bool
    runtime_mutation_allowed: bool
    direct_canonical_write_allowed: bool
    network_allowed_by_default: bool
    direct_execution_allowed: bool = False
    network_service_adapter_candidate: bool = False
    runtime_container_required_now: bool = False
    qdrant_server_required_now: bool = False

    def __post_init__(self) -> None:
        adapter_id = _require_text(self.adapter_id, "adapter_id")
        backend_kind = _require_text(self.backend_kind, "backend_kind")
        contract_mode = _require_text(self.contract_mode, "contract_mode")
        if backend_kind not in SUPPORTED_RETRIEVAL_BACKEND_KINDS:
            raise ValueError(f"unsupported backend_kind: {backend_kind}")
        if contract_mode != "adapter_only":
            raise ValueError("contract_mode must be adapter_only")

        for field_name in (
            "source_of_truth",
            "output_requires_normalization",
            "source_ref_required",
            "evidence_binding_required",
            "execution_allowed_now",
            "runtime_mutation_allowed",
            "direct_canonical_write_allowed",
            "network_allowed_by_default",
            "direct_execution_allowed",
            "network_service_adapter_candidate",
            "runtime_container_required_now",
            "qdrant_server_required_now",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if self.source_of_truth:
            raise ValueError("retrieval backend status must not be source of truth")
        if not self.output_requires_normalization:
            raise ValueError("output_requires_normalization must be True")
        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if self.execution_allowed_now:
            raise ValueError("execution_allowed_now must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_canonical_write_allowed:
            raise ValueError("direct_canonical_write_allowed must be False")
        if self.network_allowed_by_default:
            raise ValueError("network_allowed_by_default must be False")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if backend_kind != "qdrant" and self.network_service_adapter_candidate:
            raise ValueError("network_service_adapter_candidate is only valid for qdrant")
        if backend_kind == "qdrant" and not self.network_service_adapter_candidate:
            raise ValueError("qdrant must remain marked as network service adapter candidate")
        if self.runtime_container_required_now:
            raise ValueError("runtime_container_required_now must be False")
        if self.qdrant_server_required_now:
            raise ValueError("qdrant_server_required_now must be False")

        object.__setattr__(self, "adapter_id", adapter_id)
        object.__setattr__(self, "backend_kind", backend_kind)
        object.__setattr__(self, "contract_mode", contract_mode)

    @classmethod
    def from_contract(
        cls,
        contract: MgrepAdapterContract | SqliteVecAdapterContract | QdrantAdapterContract,
    ) -> "RetrievalBackendAdapterStatus":
        read_model = contract.to_read_model()
        return cls(
            adapter_id=str(read_model["adapter_id"]),
            backend_kind=str(read_model["backend_kind"]),
            contract_mode=str(read_model["contract_mode"]),
            source_of_truth=bool(read_model["source_of_truth"]),
            output_requires_normalization=bool(read_model["output_requires_normalization"]),
            source_ref_required=bool(read_model["source_ref_required"]),
            evidence_binding_required=bool(read_model["evidence_binding_required"]),
            execution_allowed_now=bool(read_model.get("execution_allowed_now", False)),
            runtime_mutation_allowed=bool(read_model["runtime_mutation_allowed"]),
            direct_canonical_write_allowed=bool(read_model.get("direct_canonical_write_allowed", False)),
            network_allowed_by_default=bool(read_model["network_allowed_by_default"]),
            direct_execution_allowed=False,
            network_service_adapter_candidate=bool(read_model.get("network_service_adapter_candidate", False)),
            runtime_container_required_now=bool(read_model.get("runtime_container_required_now", False)),
            qdrant_server_required_now=bool(read_model.get("qdrant_server_required_now", False)),
        )

    def to_read_model(self) -> dict[str, object]:
        return {
            "adapter_id": self.adapter_id,
            "backend_kind": self.backend_kind,
            "contract_mode": self.contract_mode,
            "source_of_truth": self.source_of_truth,
            "output_requires_normalization": self.output_requires_normalization,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "execution_allowed_now": self.execution_allowed_now,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_canonical_write_allowed": self.direct_canonical_write_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "direct_execution_allowed": self.direct_execution_allowed,
            "network_service_adapter_candidate": self.network_service_adapter_candidate,
            "runtime_container_required_now": self.runtime_container_required_now,
            "qdrant_server_required_now": self.qdrant_server_required_now,
        }


@dataclass(frozen=True, slots=True)
class RetrievalBackendStatusReadModel:
    read_model_id: str
    mode: str
    adapter_statuses: tuple[RetrievalBackendAdapterStatus, ...]
    configured_backend_kinds: tuple[str, ...] = SUPPORTED_RETRIEVAL_BACKEND_KINDS
    source_of_truth: bool = False
    output_requires_normalization: bool = True
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    execution_allowed_now: bool = False
    runtime_mutation_allowed: bool = False
    direct_canonical_write_allowed: bool = False
    direct_execution_allowed: bool = False
    network_allowed_by_default: bool = False
    preview_read_only: bool = True

    def __post_init__(self) -> None:
        read_model_id = _require_text(self.read_model_id, "read_model_id")
        mode = _require_text(self.mode, "mode")
        adapter_statuses = _normalize_adapter_statuses(self.adapter_statuses)
        if mode != RETRIEVAL_BACKEND_STATUS_MODE:
            raise ValueError(f"mode must be {RETRIEVAL_BACKEND_STATUS_MODE}")
        if self.configured_backend_kinds != SUPPORTED_RETRIEVAL_BACKEND_KINDS:
            raise ValueError("configured_backend_kinds must match supported retrieval backend kinds")

        for field_name in (
            "source_of_truth",
            "output_requires_normalization",
            "source_ref_required",
            "evidence_binding_required",
            "execution_allowed_now",
            "runtime_mutation_allowed",
            "direct_canonical_write_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
            "preview_read_only",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if self.source_of_truth:
            raise ValueError("retrieval backend status read model must not be source of truth")
        if not self.output_requires_normalization:
            raise ValueError("output_requires_normalization must be True")
        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if self.execution_allowed_now:
            raise ValueError("execution_allowed_now must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_canonical_write_allowed:
            raise ValueError("direct_canonical_write_allowed must be False")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.network_allowed_by_default:
            raise ValueError("network_allowed_by_default must be False")
        if not self.preview_read_only:
            raise ValueError("preview_read_only must be True")

        object.__setattr__(self, "read_model_id", read_model_id)
        object.__setattr__(self, "mode", mode)
        object.__setattr__(self, "adapter_statuses", adapter_statuses)

    def to_read_model(self) -> dict[str, object]:
        return {
            "read_model_id": self.read_model_id,
            "mode": self.mode,
            "configured_backend_kinds": self.configured_backend_kinds,
            "source_of_truth": self.source_of_truth,
            "output_requires_normalization": self.output_requires_normalization,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "execution_allowed_now": self.execution_allowed_now,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_canonical_write_allowed": self.direct_canonical_write_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "preview_read_only": self.preview_read_only,
            "adapter_statuses": tuple(status.to_read_model() for status in self.adapter_statuses),
        }

    def to_json(self) -> str:
        return json.dumps(_json_ready(self.to_read_model()), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _json_ready(value: Any) -> Any:
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready(value[key]) for key in sorted(value)}
    return value


def build_retrieval_backend_status_read_model() -> RetrievalBackendStatusReadModel:
    return RetrievalBackendStatusReadModel(
        read_model_id=RETRIEVAL_BACKEND_STATUS_MODEL_ID,
        mode=RETRIEVAL_BACKEND_STATUS_MODE,
        adapter_statuses=(
            RetrievalBackendAdapterStatus.from_contract(build_mgrep_adapter_contract()),
            RetrievalBackendAdapterStatus.from_contract(build_sqlite_vec_adapter_contract()),
            RetrievalBackendAdapterStatus.from_contract(build_qdrant_adapter_contract()),
        ),
    )


def build_retrieval_backend_status_read_model_json() -> str:
    return build_retrieval_backend_status_read_model().to_json()


__all__ = [
    "RETRIEVAL_BACKEND_STATUS_MODE",
    "RETRIEVAL_BACKEND_STATUS_MODEL_ID",
    "SUPPORTED_RETRIEVAL_BACKEND_KINDS",
    "RetrievalBackendAdapterStatus",
    "RetrievalBackendStatusReadModel",
    "build_retrieval_backend_status_read_model",
    "build_retrieval_backend_status_read_model_json",
]
