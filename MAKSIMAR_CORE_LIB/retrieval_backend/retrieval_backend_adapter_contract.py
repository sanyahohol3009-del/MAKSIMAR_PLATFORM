from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.retrieval_backend.evidence_binding_contract import (
    EvidenceBoundRetrievalResult,
)


RetrievalBackendCandidate = Literal["mgrep", "sqlite_vec", "qdrant", "in_memory_reference"]
RetrievalAdapterMode = Literal["adapter_only"]
RetrievalTruthStatus = Literal["not_source_of_truth"]


_ADAPTER_ID_PATTERN = re.compile(r"^retrieval_backend_adapter_[a-z][a-z0-9_]*$")


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
class RetrievalBackendAdapterContract:
    adapter_id: str
    backend_kind: RetrievalBackendCandidate
    adapter_mode: RetrievalAdapterMode
    truth_status: RetrievalTruthStatus
    allowed_domains: tuple[str, ...]
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    adapter_only: bool = True
    source_of_truth: bool = False
    direct_canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    network_allowed_by_default: bool = False
    auto_promotion_allowed: bool = False
    direct_execution_allowed: bool = False

    def __post_init__(self) -> None:
        adapter_id = _require_non_empty_text(self.adapter_id, "adapter_id")
        backend_kind = _require_non_empty_text(self.backend_kind, "backend_kind")
        adapter_mode = _require_non_empty_text(self.adapter_mode, "adapter_mode")
        truth_status = _require_non_empty_text(self.truth_status, "truth_status")
        allowed_domains = _normalize_text_tuple(self.allowed_domains, "allowed_domains")

        if not _ADAPTER_ID_PATTERN.fullmatch(adapter_id):
            raise ValueError(f"Invalid adapter_id: {adapter_id}")
        if backend_kind not in RetrievalBackendCandidate.__args__:
            raise ValueError(f"unsupported backend_kind: {backend_kind}")
        if adapter_mode != "adapter_only":
            raise ValueError("adapter_mode must be adapter_only")
        if truth_status != "not_source_of_truth":
            raise ValueError("truth_status must be not_source_of_truth")

        for field_name in (
            "source_ref_required",
            "evidence_binding_required",
            "adapter_only",
            "source_of_truth",
            "direct_canonical_write_allowed",
            "runtime_mutation_allowed",
            "network_allowed_by_default",
            "auto_promotion_allowed",
            "direct_execution_allowed",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if not self.adapter_only:
            raise ValueError("adapter_only must be True")
        if self.source_of_truth:
            raise ValueError("retrieval backend must not be source of truth")
        if self.direct_canonical_write_allowed:
            raise ValueError("direct_canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.network_allowed_by_default:
            raise ValueError("network_allowed_by_default must be False")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")

        object.__setattr__(self, "adapter_id", adapter_id)
        object.__setattr__(self, "backend_kind", backend_kind)
        object.__setattr__(self, "adapter_mode", adapter_mode)
        object.__setattr__(self, "truth_status", truth_status)
        object.__setattr__(self, "allowed_domains", allowed_domains)

    def validate_result(self, result: EvidenceBoundRetrievalResult) -> EvidenceBoundRetrievalResult:
        if not isinstance(result, EvidenceBoundRetrievalResult):
            raise TypeError("adapter result must be EvidenceBoundRetrievalResult")
        if result.source_of_truth:
            raise ValueError("adapter result must not be source of truth")
        if result.direct_canonical_write_allowed or result.runtime_mutation_allowed:
            raise ValueError("adapter result must be read-only")
        return result

    def to_read_model(self) -> dict[str, object]:
        return {
            "adapter_id": self.adapter_id,
            "backend_kind": self.backend_kind,
            "adapter_mode": self.adapter_mode,
            "truth_status": self.truth_status,
            "allowed_domains": self.allowed_domains,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "adapter_only": self.adapter_only,
            "source_of_truth": self.source_of_truth,
            "direct_canonical_write_allowed": self.direct_canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
            "auto_promotion_allowed": self.auto_promotion_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
        }


def build_default_retrieval_backend_adapter_contract() -> RetrievalBackendAdapterContract:
    return RetrievalBackendAdapterContract(
        adapter_id="retrieval_backend_adapter_in_memory_reference",
        backend_kind="in_memory_reference",
        adapter_mode="adapter_only",
        truth_status="not_source_of_truth",
        allowed_domains=("project_history", "technical_memory", "regulatory_memory"),
    )


__all__ = [
    "RetrievalAdapterMode",
    "RetrievalBackendAdapterContract",
    "RetrievalBackendCandidate",
    "RetrievalTruthStatus",
    "build_default_retrieval_backend_adapter_contract",
]
