from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.retrieval_backend.evidence_binding_contract import EvidenceBindingContract


RetrievalToolKind = Literal["mgrep_readonly", "sqlite_vec_readonly", "qdrant_readonly"]


_TOOL_RESULT_ID_PATTERN = re.compile(r"^retrieval_tool_result_[a-z][a-z0-9_]*$")


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


@dataclass(frozen=True, slots=True)
class RetrievalToolResultContract:
    result_id: str
    tool_kind: RetrievalToolKind
    source_ref: str
    evidence_binding: EvidenceBindingContract
    output_text: str
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    output_requires_normalization: bool = True
    normalized_output_required: bool = True
    read_only: bool = True
    source_of_truth: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    direct_execution_allowed: bool = False
    network_allowed_by_default: bool = False

    def __post_init__(self) -> None:
        result_id = _require_text(self.result_id, "result_id")
        tool_kind = _require_text(self.tool_kind, "tool_kind")
        source_ref = _require_text(self.source_ref, "source_ref")
        output_text = _require_text(self.output_text, "output_text")
        if not _TOOL_RESULT_ID_PATTERN.fullmatch(result_id):
            raise ValueError(f"Invalid result_id: {result_id}")
        if tool_kind not in RetrievalToolKind.__args__:
            raise ValueError(f"unsupported tool_kind: {tool_kind}")
        if not isinstance(self.evidence_binding, EvidenceBindingContract):
            raise TypeError("evidence_binding must be EvidenceBindingContract")

        for field_name in (
            "source_ref_required",
            "evidence_binding_required",
            "output_requires_normalization",
            "normalized_output_required",
            "read_only",
            "source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
        ):
            _require_bool(getattr(self, field_name), field_name)

        for field_name in (
            "source_ref_required",
            "evidence_binding_required",
            "output_requires_normalization",
            "normalized_output_required",
            "read_only",
        ):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must be True")
        for field_name in (
            "source_of_truth",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "direct_execution_allowed",
            "network_allowed_by_default",
        ):
            if getattr(self, field_name):
                raise ValueError(f"{field_name} must be False")

        object.__setattr__(self, "result_id", result_id)
        object.__setattr__(self, "tool_kind", tool_kind)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "output_text", output_text)

    def to_read_model(self) -> dict[str, object]:
        return {
            "result_id": self.result_id,
            "tool_kind": self.tool_kind,
            "source_ref": self.source_ref,
            "evidence_binding": self.evidence_binding.to_read_model(),
            "output_text": self.output_text,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "output_requires_normalization": self.output_requires_normalization,
            "normalized_output_required": self.normalized_output_required,
            "read_only": self.read_only,
            "source_of_truth": self.source_of_truth,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "network_allowed_by_default": self.network_allowed_by_default,
        }


__all__ = [
    "RetrievalToolKind",
    "RetrievalToolResultContract",
]
