from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_probe_result_binding import (
    build_mempalace_probe_result_binding_preview,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_query_models import (
    build_mempalace_query_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_write_models import (
    build_mempalace_write_request_contract,
)

_ROUTING_REPORT = Path("EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_read_only_routing_integration_report.json")


@dataclass(frozen=True, slots=True)
class MemPalaceReadOnlyRoutingIntegration:
    integration_id: str
    adapter_id: str
    subordinate_backend: bool
    read_only_routing_enabled: bool
    query_domains: Tuple[str, ...]
    query_count: int
    write_request_count: int
    write_request_allowed_count: int
    write_routing_enabled: bool
    full_real_backend_enablement_allowed: bool
    general_real_backend_query_allowed: bool
    canonical_write_allowed: bool
    runtime_mutation_allowed: bool
    auto_promotion_allowed: bool
    auto_conflict_resolution_allowed: bool
    evidence_pack: Tuple[str, ...]
    routing_integration_ready: bool

    def __post_init__(self) -> None:
        if not self.integration_id:
            raise ValueError("integration_id must be non-empty")
        if not self.adapter_id:
            raise ValueError("adapter_id must be non-empty")
        if not self.query_domains:
            raise ValueError("query_domains must be non-empty")
        if not self.evidence_pack:
            raise ValueError("evidence_pack must be non-empty")

        required_true = (
            "subordinate_backend",
            "read_only_routing_enabled",
            "routing_integration_ready",
        )
        for field_name in required_true:
            if getattr(self, field_name) is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = (
            "write_routing_enabled",
            "full_real_backend_enablement_allowed",
            "general_real_backend_query_allowed",
            "canonical_write_allowed",
            "runtime_mutation_allowed",
            "auto_promotion_allowed",
            "auto_conflict_resolution_allowed",
        )
        for field_name in required_false:
            if getattr(self, field_name) is not False:
                raise ValueError(f"{field_name} must be False")

        if self.query_count != len(self.query_domains):
            raise ValueError("query_count must match query_domains length")
        if self.write_request_allowed_count != 0:
            raise ValueError("write_request_allowed_count must be 0 for read-only routing")


def build_mempalace_read_only_routing_integration() -> MemPalaceReadOnlyRoutingIntegration:
    binding = build_mempalace_probe_result_binding_preview()
    queries = build_mempalace_query_contract()
    writes = build_mempalace_write_request_contract()

    query_domains = tuple(entry.domain for entry in queries.entries)

    routing_ready = (
        binding["binding_ready"] is True
        and binding["read_only_adapter_binding_allowed"] is True
        and binding["full_real_backend_enablement_allowed"] is False
        and binding["general_real_backend_query_allowed"] is False
        and binding["canonical_write_allowed"] is False
        and binding["runtime_mutation_allowed"] is False
        and queries.ready_queries == queries.total_queries
        and queries.retrieval_allowed_queries == queries.total_queries
        and queries.evidence_pack_required_queries == queries.total_queries
        and queries.preview_trace_required_queries == queries.total_queries
        and queries.policy_check_required_queries == queries.total_queries
        and queries.source_attribution_required_queries == queries.total_queries
        and queries.canonical_truth_allowed_queries == 0
        and queries.runtime_mutation_allowed_queries == 0
    )

    return MemPalaceReadOnlyRoutingIntegration(
        integration_id="mempalace_read_only_routing_integration_001",
        adapter_id="mempalace_adapter_memory_routing_001",
        subordinate_backend=True,
        read_only_routing_enabled=True,
        query_domains=query_domains,
        query_count=queries.total_queries,
        write_request_count=writes.total_write_requests,
        write_request_allowed_count=0,
        write_routing_enabled=False,
        full_real_backend_enablement_allowed=False,
        general_real_backend_query_allowed=False,
        canonical_write_allowed=False,
        runtime_mutation_allowed=False,
        auto_promotion_allowed=False,
        auto_conflict_resolution_allowed=False,
        evidence_pack=(
            "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_probe_result_binding_report.json",
            "EXTERNAL_BACKENDS/mempalace/smoke_reports/mempalace_controlled_real_backend_probe_report.json",
            "EXTERNAL_BACKENDS/mempalace/security_reports/mempalace_real_backend_approval_envelope_report.json",
        ),
        routing_integration_ready=routing_ready,
    )


def build_mempalace_read_only_routing_integration_preview() -> dict[str, object]:
    integration = build_mempalace_read_only_routing_integration()

    return {
        "integration_id": integration.integration_id,
        "adapter_id": integration.adapter_id,
        "subordinate_backend": integration.subordinate_backend,
        "read_only_routing_enabled": integration.read_only_routing_enabled,
        "query_domains": integration.query_domains,
        "query_count": integration.query_count,
        "write_request_count": integration.write_request_count,
        "write_request_allowed_count": integration.write_request_allowed_count,
        "write_routing_enabled": integration.write_routing_enabled,
        "full_real_backend_enablement_allowed": integration.full_real_backend_enablement_allowed,
        "general_real_backend_query_allowed": integration.general_real_backend_query_allowed,
        "canonical_write_allowed": integration.canonical_write_allowed,
        "runtime_mutation_allowed": integration.runtime_mutation_allowed,
        "auto_promotion_allowed": integration.auto_promotion_allowed,
        "auto_conflict_resolution_allowed": integration.auto_conflict_resolution_allowed,
        "evidence_pack": integration.evidence_pack,
        "routing_integration_ready": integration.routing_integration_ready,
    }


def write_mempalace_read_only_routing_integration_report() -> Path:
    payload = build_mempalace_read_only_routing_integration_preview()
    _ROUTING_REPORT.parent.mkdir(parents=True, exist_ok=True)
    _ROUTING_REPORT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return _ROUTING_REPORT
