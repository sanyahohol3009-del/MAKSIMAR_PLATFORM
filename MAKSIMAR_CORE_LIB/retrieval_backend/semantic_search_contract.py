from __future__ import annotations

import re
from dataclasses import dataclass


_QUERY_ID_PATTERN = re.compile(r"^semantic_search_query_[a-z][a-z0-9_]*$")
_MAX_TOP_K = 50


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


def _require_top_k(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError("top_k must be int")
    if value <= 0:
        raise ValueError("top_k must be > 0")
    if value > _MAX_TOP_K:
        raise ValueError(f"top_k must be <= {_MAX_TOP_K}")
    return value


def _normalize_text_tuple(values: tuple[str, ...], field_name: str, *, required: bool) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    normalized = tuple(_require_non_empty_text(value, field_name) for value in values)
    if required and not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


@dataclass(frozen=True, slots=True)
class SemanticSearchContract:
    query_id: str
    query_text: str
    requested_domains: tuple[str, ...]
    top_k: int
    filters: tuple[str, ...]
    source_scope: tuple[str, ...]
    evidence_required: bool = True
    source_ref_required: bool = True
    evidence_binding_required: bool = True
    normalized_request_metadata_only: bool = True
    backend_execution_allowed: bool = False
    direct_execution_allowed: bool = False
    source_of_truth: bool = False

    def __post_init__(self) -> None:
        query_id = _require_non_empty_text(self.query_id, "query_id")
        query_text = _require_non_empty_text(self.query_text, "query_text")
        requested_domains = _normalize_text_tuple(
            self.requested_domains,
            "requested_domains",
            required=True,
        )
        top_k = _require_top_k(self.top_k)
        filters = _normalize_text_tuple(self.filters, "filters", required=False)
        source_scope = _normalize_text_tuple(self.source_scope, "source_scope", required=True)

        if not _QUERY_ID_PATTERN.fullmatch(query_id):
            raise ValueError(f"Invalid query_id: {query_id}")

        for field_name in (
            "evidence_required",
            "source_ref_required",
            "evidence_binding_required",
            "normalized_request_metadata_only",
            "backend_execution_allowed",
            "direct_execution_allowed",
            "source_of_truth",
        ):
            _require_bool(getattr(self, field_name), field_name)

        if not self.evidence_required:
            raise ValueError("evidence_required must be True")
        if not self.source_ref_required:
            raise ValueError("source_ref_required must be True")
        if not self.evidence_binding_required:
            raise ValueError("evidence_binding_required must be True")
        if not self.normalized_request_metadata_only:
            raise ValueError("normalized_request_metadata_only must be True")
        if self.backend_execution_allowed:
            raise ValueError("backend_execution_allowed must be False")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.source_of_truth:
            raise ValueError("source_of_truth must be False")

        object.__setattr__(self, "query_id", query_id)
        object.__setattr__(self, "query_text", query_text)
        object.__setattr__(self, "requested_domains", requested_domains)
        object.__setattr__(self, "top_k", top_k)
        object.__setattr__(self, "filters", filters)
        object.__setattr__(self, "source_scope", source_scope)

    def to_retrieval_request_metadata(self) -> dict[str, object]:
        return {
            "query_id": self.query_id,
            "query_text": self.query_text,
            "requested_domains": self.requested_domains,
            "top_k": self.top_k,
            "filters": self.filters,
            "source_scope": self.source_scope,
            "evidence_required": self.evidence_required,
            "source_ref_required": self.source_ref_required,
            "evidence_binding_required": self.evidence_binding_required,
            "normalized_request_metadata_only": self.normalized_request_metadata_only,
            "backend_execution_allowed": self.backend_execution_allowed,
            "direct_execution_allowed": self.direct_execution_allowed,
            "source_of_truth": self.source_of_truth,
        }

    def to_read_model(self) -> dict[str, object]:
        return self.to_retrieval_request_metadata()


def build_default_semantic_search_contract() -> SemanticSearchContract:
    return SemanticSearchContract(
        query_id="semantic_search_query_retrieval_backend_contract",
        query_text="retrieval backend contracts must bind source refs and evidence",
        requested_domains=("project_history", "technical_memory"),
        top_k=10,
        filters=("read_only", "source_bound"),
        source_scope=("MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing", "MAKSIMAR_CORE_LIB/evidence_memory"),
    )


__all__ = [
    "SemanticSearchContract",
    "build_default_semantic_search_contract",
]
