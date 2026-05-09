from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


RetrievalIntent = Literal[
    "project_history",
    "technical_memory",
    "media_artifact",
    "model_artifact",
    "storage_lookup",
    "dashboard_preview",
]

RetrievalLanguageCode = Literal["ru", "en", "de", "mixed"]


_REQUEST_ID_PATTERN = re.compile(r"^retrieval_req_[a-z0-9_]+$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_positive_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value <= 0:
        raise ValueError(f"{field_name} must be > 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalRequest:
    """Canonical retrieval request for memory routing.

    This request does not execute search. It defines routing intent, scope,
    evidence requirements and preview/audit expectations.
    """

    request_id: str
    query: str
    intent: RetrievalIntent
    language_code: RetrievalLanguageCode
    requested_domain: str
    max_results: int
    evidence_required: bool
    preview_required: bool
    policy_gate_required: bool

    def __post_init__(self) -> None:
        request_id = _ensure_non_empty_str(self.request_id, "request_id")
        query = _ensure_non_empty_str(self.query, "query")
        requested_domain = _ensure_non_empty_str(
            self.requested_domain,
            "requested_domain",
        )
        max_results = _ensure_positive_int(self.max_results, "max_results")

        if not _REQUEST_ID_PATTERN.fullmatch(request_id):
            raise ValueError(f"Invalid request_id: {request_id}")

        for field_name in (
            "evidence_required",
            "preview_required",
            "policy_gate_required",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.evidence_required:
            raise ValueError("evidence_required must be True")
        if not self.preview_required:
            raise ValueError("preview_required must be True")
        if not self.policy_gate_required:
            raise ValueError("policy_gate_required must be True")

        object.__setattr__(self, "request_id", request_id)
        object.__setattr__(self, "query", query)
        object.__setattr__(self, "requested_domain", requested_domain)
        object.__setattr__(self, "max_results", max_results)
