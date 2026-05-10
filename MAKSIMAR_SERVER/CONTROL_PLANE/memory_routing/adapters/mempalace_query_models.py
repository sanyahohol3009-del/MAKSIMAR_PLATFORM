from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_capability_builder import (
    MemPalaceDomain,
    build_mempalace_capability_contract,
)

_QUERY_ID_PATTERN = re.compile(r"^mempalace_query_[a-z][a-z0-9_]*_[0-9]{3}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class MemPalaceQueryEntry:
    query_id: str
    domain: MemPalaceDomain
    adapter_id: str
    retrieval_allowed: bool
    evidence_pack_required: bool
    preview_trace_required: bool
    policy_check_required: bool
    source_attribution_required: bool
    canonical_truth_allowed: bool
    runtime_mutation_allowed: bool
    query_ready: bool
    description: str

    def __post_init__(self) -> None:
        query_id = _ensure_non_empty_str(self.query_id, "query_id")
        if not _QUERY_ID_PATTERN.fullmatch(query_id):
            raise ValueError(f"Invalid query_id: {query_id}")

        for field_name in ("adapter_id", "description"):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "retrieval_allowed",
            "evidence_pack_required",
            "preview_trace_required",
            "policy_check_required",
            "source_attribution_required",
            "canonical_truth_allowed",
            "runtime_mutation_allowed",
            "query_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.retrieval_allowed:
            raise ValueError("retrieval_allowed must be True")
        if not self.evidence_pack_required:
            raise ValueError("evidence_pack_required must be True")
        if not self.preview_trace_required:
            raise ValueError("preview_trace_required must be True")
        if not self.policy_check_required:
            raise ValueError("policy_check_required must be True")
        if not self.source_attribution_required:
            raise ValueError("source_attribution_required must be True")
        if self.canonical_truth_allowed:
            raise ValueError("canonical_truth_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if not self.query_ready:
            raise ValueError("query_ready must be True")


@dataclass(frozen=True, slots=True)
class MemPalaceQueryContract:
    total_queries: int
    ready_queries: int
    retrieval_allowed_queries: int
    evidence_pack_required_queries: int
    preview_trace_required_queries: int
    policy_check_required_queries: int
    source_attribution_required_queries: int
    canonical_truth_allowed_queries: int
    runtime_mutation_allowed_queries: int
    entries: tuple[MemPalaceQueryEntry, ...]

    def __post_init__(self) -> None:
        if self.total_queries != len(self.entries):
            raise ValueError("total_queries must match entries length")
        if self.total_queries != 4:
            raise ValueError("MemPalace query contract must contain exactly 4 query entries")

        expected = {
            "ready_queries": sum(1 for entry in self.entries if entry.query_ready),
            "retrieval_allowed_queries": sum(1 for entry in self.entries if entry.retrieval_allowed),
            "evidence_pack_required_queries": sum(1 for entry in self.entries if entry.evidence_pack_required),
            "preview_trace_required_queries": sum(1 for entry in self.entries if entry.preview_trace_required),
            "policy_check_required_queries": sum(1 for entry in self.entries if entry.policy_check_required),
            "source_attribution_required_queries": sum(1 for entry in self.entries if entry.source_attribution_required),
            "canonical_truth_allowed_queries": sum(1 for entry in self.entries if entry.canonical_truth_allowed),
            "runtime_mutation_allowed_queries": sum(1 for entry in self.entries if entry.runtime_mutation_allowed),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_queries != self.total_queries:
            raise ValueError("all MemPalace queries must be ready")
        if self.retrieval_allowed_queries != self.total_queries:
            raise ValueError("all MemPalace queries must allow retrieval")
        if self.evidence_pack_required_queries != self.total_queries:
            raise ValueError("all MemPalace queries must require evidence pack")
        if self.preview_trace_required_queries != self.total_queries:
            raise ValueError("all MemPalace queries must require preview trace")
        if self.policy_check_required_queries != self.total_queries:
            raise ValueError("all MemPalace queries must require policy check")
        if self.source_attribution_required_queries != self.total_queries:
            raise ValueError("all MemPalace queries must require source attribution")
        if self.canonical_truth_allowed_queries != 0:
            raise ValueError("MemPalace canonical truth query must remain blocked")
        if self.runtime_mutation_allowed_queries != 0:
            raise ValueError("MemPalace runtime mutation query must remain blocked")


def build_mempalace_query_contract() -> MemPalaceQueryContract:
    capabilities = build_mempalace_capability_contract()

    entries = tuple(
        MemPalaceQueryEntry(
            query_id=f"mempalace_query_{capability.domain}_001",
            domain=capability.domain,
            adapter_id="mempalace_adapter_memory_routing_001",
            retrieval_allowed=capability.retrieval_allowed,
            evidence_pack_required=True,
            preview_trace_required=True,
            policy_check_required=True,
            source_attribution_required=True,
            canonical_truth_allowed=False,
            runtime_mutation_allowed=False,
            query_ready=capability.capability_ready and capability.retrieval_allowed,
            description=f"Read-only MemPalace query contract for {capability.domain}.",
        )
        for capability in capabilities.entries
    )

    return MemPalaceQueryContract(
        total_queries=len(entries),
        ready_queries=sum(1 for entry in entries if entry.query_ready),
        retrieval_allowed_queries=sum(1 for entry in entries if entry.retrieval_allowed),
        evidence_pack_required_queries=sum(1 for entry in entries if entry.evidence_pack_required),
        preview_trace_required_queries=sum(1 for entry in entries if entry.preview_trace_required),
        policy_check_required_queries=sum(1 for entry in entries if entry.policy_check_required),
        source_attribution_required_queries=sum(1 for entry in entries if entry.source_attribution_required),
        canonical_truth_allowed_queries=sum(1 for entry in entries if entry.canonical_truth_allowed),
        runtime_mutation_allowed_queries=sum(1 for entry in entries if entry.runtime_mutation_allowed),
        entries=entries,
    )
