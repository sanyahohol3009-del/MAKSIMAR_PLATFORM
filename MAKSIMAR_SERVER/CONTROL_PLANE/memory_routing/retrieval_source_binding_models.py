from __future__ import annotations

import re
from dataclasses import dataclass


_SOURCE_ID_PATTERN = re.compile(r"^retrieval_source_[a-z][a-z0-9_]*$")


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
class RetrievalSourceBinding:
    """Binding between retrieval routing and an approved memory/storage source."""

    source_id: str
    source_kind: str
    memory_domain: str
    registry_ref: str
    priority: int
    evidence_supported: bool
    trace_supported: bool
    policy_allowed: bool
    backend_adapter_required: bool

    def __post_init__(self) -> None:
        source_id = _ensure_non_empty_str(self.source_id, "source_id")
        source_kind = _ensure_non_empty_str(self.source_kind, "source_kind")
        memory_domain = _ensure_non_empty_str(self.memory_domain, "memory_domain")
        registry_ref = _ensure_non_empty_str(self.registry_ref, "registry_ref")
        priority = _ensure_positive_int(self.priority, "priority")

        if not _SOURCE_ID_PATTERN.fullmatch(source_id):
            raise ValueError(f"Invalid source_id: {source_id}")

        for field_name in (
            "evidence_supported",
            "trace_supported",
            "policy_allowed",
            "backend_adapter_required",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.evidence_supported:
            raise ValueError("evidence_supported must be True")
        if not self.trace_supported:
            raise ValueError("trace_supported must be True")
        if not self.policy_allowed:
            raise ValueError("policy_allowed must be True")

        object.__setattr__(self, "source_id", source_id)
        object.__setattr__(self, "source_kind", source_kind)
        object.__setattr__(self, "memory_domain", memory_domain)
        object.__setattr__(self, "registry_ref", registry_ref)
        object.__setattr__(self, "priority", priority)
