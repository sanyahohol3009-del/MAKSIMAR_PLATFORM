from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.retrieval_backend.retrieval_backend_adapter_contract import (
    RetrievalBackendCandidate,
)


ALLOWED_RETRIEVAL_BACKEND_CANDIDATES: tuple[str, ...] = (
    "mgrep",
    "sqlite_vec",
    "qdrant",
    "in_memory_reference",
)
RETRIEVAL_POLICY_MODE = "adapter_contract_only"


def _require_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")
    return value


def _require_non_empty_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    return normalized


def _normalize_backend_candidates(values: tuple[RetrievalBackendCandidate, ...]) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError("allowed_backend_candidates must be a tuple")
    normalized = tuple(_require_non_empty_text(value, "allowed_backend_candidates") for value in values)
    if not normalized:
        raise ValueError("allowed_backend_candidates must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError("allowed_backend_candidates must not contain duplicates")
    unknown = tuple(value for value in normalized if value not in ALLOWED_RETRIEVAL_BACKEND_CANDIDATES)
    if unknown:
        raise ValueError(f"unsupported backend candidates: {unknown}")
    return normalized


@dataclass(frozen=True, slots=True)
class RetrievalPolicyGateContract:
    policy_id: str
    policy_mode: str
    allowed_backend_candidates: tuple[RetrievalBackendCandidate, ...]
    execution_allowed_now: bool = False
    network_allowed_by_default: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    direct_execution_allowed: bool = False
    auto_promotion_allowed: bool = False
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    backend_is_source_of_truth: bool = False
    adapter_output_requires_normalization: bool = True

    def __post_init__(self) -> None:
        policy_id = _require_non_empty_text(self.policy_id, "policy_id")
        policy_mode = _require_non_empty_text(self.policy_mode, "policy_mode")
        allowed_backend_candidates = _normalize_backend_candidates(self.allowed_backend_candidates)
        if policy_mode != RETRIEVAL_POLICY_MODE:
            raise ValueError(f"policy_mode must be {RETRIEVAL_POLICY_MODE}")

        for field_name in (
            "execution_allowed_now",
            "network_allowed_by_default",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "auto_promotion_allowed",
            "source_ref_required",
            "evidence_binding_required",
            "backend_is_source_of_truth",
            "adapter_output_requires_normalization",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if self.execution_allowed_now:
            raise ValueError("execution_allowed_now must be False")
        if self.network_allowed_by_default:
            raise ValueError("network_allowed_by_default must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.auto_promotion_allowed:
            raise ValueError("auto_promotion_allowed must be False")
        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if self.backend_is_source_of_truth:
            raise ValueError("backend_is_source_of_truth must be False")
        if not self.adapter_output_requires_normalization:
            raise ValueError("adapter_output_requires_normalization must be True")

        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "policy_mode", policy_mode)
        object.__setattr__(self, "allowed_backend_candidates", allowed_backend_candidates)

    def to_read_model(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "policy_mode": self.policy_mode,
            "allowed_backend_candidates": self.allowed_backend_candidates,
            "execution_allowed_now": self.execution_allowed_now,
            "network_allowed_by_default": self.network_allowed_by_default,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "auto_promotion_allowed": self.auto_promotion_allowed,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "backend_is_source_of_truth": self.backend_is_source_of_truth,
            "adapter_output_requires_normalization": self.adapter_output_requires_normalization,
        }


def build_default_retrieval_policy_gate_contract() -> RetrievalPolicyGateContract:
    return RetrievalPolicyGateContract(
        policy_id="retrieval_policy_gate_contract_phase_7_2",
        policy_mode=RETRIEVAL_POLICY_MODE,
        allowed_backend_candidates=ALLOWED_RETRIEVAL_BACKEND_CANDIDATES,
    )


__all__ = [
    "ALLOWED_RETRIEVAL_BACKEND_CANDIDATES",
    "RETRIEVAL_POLICY_MODE",
    "RetrievalPolicyGateContract",
    "build_default_retrieval_policy_gate_contract",
]
