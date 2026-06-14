from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


EvidenceKind = Literal[
    "source_ref",
    "retrieval_preview",
    "semantic_match",
    "vector_match",
    "memory_record",
    "regulatory_source",
]


_EVIDENCE_ID_PATTERN = re.compile(r"^evidence_[a-z][a-z0-9_]*$")
_RESULT_ID_PATTERN = re.compile(r"^retrieval_result_[a-z][a-z0-9_]*$")
_TRACE_ID_PATTERN = re.compile(r"^trace_[a-z][a-z0-9_]*$")


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


def _require_confidence(value: float, field_name: str) -> float:
    if not isinstance(value, (float, int)) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be numeric")
    normalized = float(value)
    if normalized < 0.0 or normalized > 1.0:
        raise ValueError(f"{field_name} must be between 0.0 and 1.0")
    return normalized


@dataclass(frozen=True, slots=True)
class EvidenceBindingContract:
    source_ref: str
    evidence_id: str
    evidence_kind: EvidenceKind
    confidence: float
    trace_id: str
    source_version: str = "v1"
    source_ref_required: bool = True
    evidence_id_required: bool = True
    trace_required: bool = True
    citation_required: bool = True
    source_bound: bool = True
    canonical_truth_claim_allowed: bool = False

    def __post_init__(self) -> None:
        source_ref = _require_non_empty_text(self.source_ref, "source_ref")
        evidence_id = _require_non_empty_text(self.evidence_id, "evidence_id")
        evidence_kind = _require_non_empty_text(self.evidence_kind, "evidence_kind")
        trace_id = _require_non_empty_text(self.trace_id, "trace_id")
        source_version = _require_non_empty_text(self.source_version, "source_version")
        confidence = _require_confidence(self.confidence, "confidence")

        if not _EVIDENCE_ID_PATTERN.fullmatch(evidence_id):
            raise ValueError(f"Invalid evidence_id: {evidence_id}")
        if not _TRACE_ID_PATTERN.fullmatch(trace_id):
            raise ValueError(f"Invalid trace_id: {trace_id}")
        if evidence_kind not in EvidenceKind.__args__:
            raise ValueError(f"unsupported evidence_kind: {evidence_kind}")

        for field_name in (
            "source_ref_required",
            "evidence_id_required",
            "trace_required",
            "citation_required",
            "source_bound",
            "canonical_truth_claim_allowed",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_id_required:
            raise ValueError("evidence_id_required must be True")
        if not self.trace_required:
            raise ValueError("trace_required must be True")
        if not self.citation_required:
            raise ValueError("citation_required must be True")
        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if self.canonical_truth_claim_allowed:
            raise ValueError("retrieval evidence must not claim canonical truth")

        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "evidence_id", evidence_id)
        object.__setattr__(self, "evidence_kind", evidence_kind)
        object.__setattr__(self, "confidence", confidence)
        object.__setattr__(self, "trace_id", trace_id)
        object.__setattr__(self, "source_version", source_version)

    def to_read_model(self) -> dict[str, object]:
        return {
            "source_ref": self.source_ref,
            "evidence_id": self.evidence_id,
            "evidence_kind": self.evidence_kind,
            "confidence": self.confidence,
            "trace_id": self.trace_id,
            "source_version": self.source_version,
            "source_ref_required": self.source_ref_required,
            "evidence_id_required": self.evidence_id_required,
            "trace_required": self.trace_required,
            "citation_required": self.citation_required,
            "source_bound": self.source_bound,
            "canonical_truth_claim_allowed": self.canonical_truth_claim_allowed,
        }


@dataclass(frozen=True, slots=True)
class EvidenceBoundRetrievalResult:
    result_id: str
    result_text: str
    score: float
    evidence_binding: EvidenceBindingContract
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    adapter_result_only: bool = True
    source_of_truth: bool = False
    direct_canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        result_id = _require_non_empty_text(self.result_id, "result_id")
        result_text = _require_non_empty_text(self.result_text, "result_text")
        score = _require_confidence(self.score, "score")
        if not _RESULT_ID_PATTERN.fullmatch(result_id):
            raise ValueError(f"Invalid result_id: {result_id}")
        if not isinstance(self.evidence_binding, EvidenceBindingContract):
            raise TypeError("evidence_binding must be EvidenceBindingContract")

        for field_name in (
            "source_ref_required",
            "evidence_binding_required",
            "adapter_result_only",
            "source_of_truth",
            "direct_canonical_write_allowed",
            "runtime_mutation_allowed",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if not self.adapter_result_only:
            raise ValueError("adapter_result_only must be True")
        if self.source_of_truth:
            raise ValueError("retrieval result must not be source of truth")
        if self.direct_canonical_write_allowed:
            raise ValueError("direct_canonical_write_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")

        object.__setattr__(self, "result_id", result_id)
        object.__setattr__(self, "result_text", result_text)
        object.__setattr__(self, "score", score)

    def to_read_model(self) -> dict[str, object]:
        return {
            "result_id": self.result_id,
            "result_text": self.result_text,
            "score": self.score,
            "evidence_binding": self.evidence_binding.to_read_model(),
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "adapter_result_only": self.adapter_result_only,
            "source_of_truth": self.source_of_truth,
            "direct_canonical_write_allowed": self.direct_canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
        }


def build_default_evidence_binding_contract() -> EvidenceBindingContract:
    return EvidenceBindingContract(
        source_ref="MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_evidence_pack_models.py",
        evidence_id="evidence_retrieval_backend_contract",
        evidence_kind="retrieval_preview",
        confidence=1.0,
        trace_id="trace_retrieval_backend_contract",
    )


def build_default_evidence_bound_retrieval_result() -> EvidenceBoundRetrievalResult:
    return EvidenceBoundRetrievalResult(
        result_id="retrieval_result_retrieval_backend_contract",
        result_text="PHASE 7.1 retrieval backend adapter result is evidence-bound and adapter-only.",
        score=1.0,
        evidence_binding=build_default_evidence_binding_contract(),
    )


__all__ = [
    "EvidenceBindingContract",
    "EvidenceBoundRetrievalResult",
    "EvidenceKind",
    "build_default_evidence_binding_contract",
    "build_default_evidence_bound_retrieval_result",
]
