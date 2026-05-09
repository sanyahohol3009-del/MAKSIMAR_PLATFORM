from __future__ import annotations

import re
from dataclasses import dataclass


_SCOPE_ID_PATTERN = re.compile(r"^retrieval_scope_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_empty_tuple(values: tuple[str, ...], field_name: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise ValueError(f"{field_name} must be a tuple")
    if not values:
        raise ValueError(f"{field_name} must be non-empty")
    normalized = tuple(_ensure_non_empty_str(value, field_name) for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must not contain duplicates")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalScope:
    """Allowed retrieval scope for one request."""

    scope_id: str
    allowed_memory_domains: tuple[str, ...]
    allowed_source_kinds: tuple[str, ...]
    forbidden_source_kinds: tuple[str, ...]
    tenant_boundary_required: bool
    policy_gate_required: bool
    cross_domain_allowed: bool

    def __post_init__(self) -> None:
        scope_id = _ensure_non_empty_str(self.scope_id, "scope_id")
        allowed_memory_domains = _ensure_non_empty_tuple(
            self.allowed_memory_domains,
            "allowed_memory_domains",
        )
        allowed_source_kinds = _ensure_non_empty_tuple(
            self.allowed_source_kinds,
            "allowed_source_kinds",
        )

        if not isinstance(self.forbidden_source_kinds, tuple):
            raise ValueError("forbidden_source_kinds must be a tuple")
        forbidden_source_kinds = tuple(
            _ensure_non_empty_str(value, "forbidden_source_kinds")
            for value in self.forbidden_source_kinds
        )
        if len(set(forbidden_source_kinds)) != len(forbidden_source_kinds):
            raise ValueError("forbidden_source_kinds must not contain duplicates")

        if not _SCOPE_ID_PATTERN.fullmatch(scope_id):
            raise ValueError(f"Invalid scope_id: {scope_id}")

        for field_name in (
            "tenant_boundary_required",
            "policy_gate_required",
            "cross_domain_allowed",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.tenant_boundary_required:
            raise ValueError("tenant_boundary_required must be True")
        if not self.policy_gate_required:
            raise ValueError("policy_gate_required must be True")

        overlap = set(allowed_source_kinds).intersection(forbidden_source_kinds)
        if overlap:
            raise ValueError("allowed and forbidden source kinds must not overlap")

        object.__setattr__(self, "scope_id", scope_id)
        object.__setattr__(self, "allowed_memory_domains", allowed_memory_domains)
        object.__setattr__(self, "allowed_source_kinds", allowed_source_kinds)
        object.__setattr__(self, "forbidden_source_kinds", forbidden_source_kinds)
