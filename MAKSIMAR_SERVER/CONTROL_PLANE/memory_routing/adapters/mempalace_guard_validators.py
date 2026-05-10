from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_adapter_models import (
    build_mempalace_adapter_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_capability_builder import (
    build_mempalace_capability_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_query_models import (
    build_mempalace_query_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_write_models import (
    build_mempalace_write_request_contract,
)


_ALLOWED_DOMAINS = (
    "conversational_memory",
    "project_notes",
    "owner_context",
    "tenant_conversational_context",
)

_FORBIDDEN_CANONICAL_DOMAINS = (
    "constitutional_memory",
    "regulatory_memory",
    "enterprise_policy_memory",
    "technical_truth",
    "audit_truth",
    "approval_truth",
    "mutation_boundary_truth",
    "artifact_canonical_truth",
)


@dataclass(frozen=True, slots=True)
class MemPalaceGuardValidationReport:
    allowed_domains: Tuple[str, ...]
    forbidden_domains: Tuple[str, ...]
    allowed_domains_ready: bool
    forbidden_domains_absent: bool
    adapter_ready: bool
    capability_ready: bool
    query_ready: bool
    write_request_ready: bool
    evidence_pack_required: bool
    preview_trace_required: bool
    policy_check_required: bool
    source_attribution_required: bool
    approval_required_for_allowed_writes: bool
    approval_granted_by_default: bool
    sandbox_stage_required_for_allowed_writes: bool
    diff_preview_required_for_allowed_writes: bool
    risk_summary_required_for_allowed_writes: bool
    no_source_of_truth: bool
    no_canonical_truth: bool
    no_regulatory_memory: bool
    no_enterprise_policy_memory: bool
    no_technical_truth: bool
    no_audit_truth: bool
    no_approval_truth: bool
    no_canonical_write: bool
    no_auto_promotion: bool
    no_auto_conflict_resolution: bool
    no_runtime_mutation: bool
    guard_validation_ready: bool

    def __post_init__(self) -> None:
        if self.allowed_domains != _ALLOWED_DOMAINS:
            raise ValueError("allowed_domains must match MemPalace allowed domains")
        if self.forbidden_domains != _FORBIDDEN_CANONICAL_DOMAINS:
            raise ValueError("forbidden_domains must match blocked canonical domains")

        required_true_fields = (
            "allowed_domains_ready",
            "forbidden_domains_absent",
            "adapter_ready",
            "capability_ready",
            "query_ready",
            "write_request_ready",
            "evidence_pack_required",
            "preview_trace_required",
            "policy_check_required",
            "source_attribution_required",
            "approval_required_for_allowed_writes",
            "approval_granted_by_default",
            "sandbox_stage_required_for_allowed_writes",
            "diff_preview_required_for_allowed_writes",
            "risk_summary_required_for_allowed_writes",
            "no_source_of_truth",
            "no_canonical_truth",
            "no_regulatory_memory",
            "no_enterprise_policy_memory",
            "no_technical_truth",
            "no_audit_truth",
            "no_approval_truth",
            "no_canonical_write",
            "no_auto_promotion",
            "no_auto_conflict_resolution",
            "no_runtime_mutation",
            "guard_validation_ready",
        )

        for field_name in required_true_fields:
            value = getattr(self, field_name)
            if not isinstance(value, bool):
                raise ValueError(f"{field_name} must be bool")
            if not value:
                raise ValueError(f"{field_name} must be True")


def build_mempalace_guard_validation_report() -> MemPalaceGuardValidationReport:
    adapter = build_mempalace_adapter_contract()
    capabilities = build_mempalace_capability_contract()
    queries = build_mempalace_query_contract()
    writes = build_mempalace_write_request_contract()

    allowed_domains = tuple(entry.domain for entry in capabilities.entries)
    forbidden_domains_absent = not any(domain in allowed_domains for domain in _FORBIDDEN_CANONICAL_DOMAINS)

    adapter_ready = adapter.ready_adapters == adapter.total_adapters
    capability_ready = capabilities.ready_capabilities == capabilities.total_capabilities
    query_ready = queries.ready_queries == queries.total_queries
    write_request_ready = writes.ready_write_requests == writes.total_write_requests

    no_source_of_truth = adapter.source_of_truth_adapters == 0
    no_canonical_truth = capabilities.canonical_truth_allowed_capabilities == 0 and queries.canonical_truth_allowed_queries == 0
    no_regulatory_memory = capabilities.regulatory_memory_allowed_capabilities == 0
    no_enterprise_policy_memory = capabilities.enterprise_policy_memory_allowed_capabilities == 0
    no_technical_truth = capabilities.technical_truth_allowed_capabilities == 0
    no_audit_truth = capabilities.audit_truth_allowed_capabilities == 0
    no_approval_truth = capabilities.approval_truth_allowed_capabilities == 0

    no_canonical_write = (
        adapter.canonical_write_allowed_adapters
        + writes.canonical_write_allowed_write_requests
    ) == 0
    no_auto_promotion = (
        capabilities.auto_promotion_allowed_capabilities
        + writes.auto_promotion_allowed_write_requests
    ) == 0
    no_auto_conflict_resolution = capabilities.auto_conflict_resolution_allowed_capabilities == 0
    no_runtime_mutation = (
        adapter.runtime_mutation_allowed_adapters
        + capabilities.runtime_mutation_allowed_capabilities
        + queries.runtime_mutation_allowed_queries
        + writes.runtime_mutation_allowed_write_requests
    ) == 0

    allowed_write_requests = writes.allowed_write_requests

    evidence_pack_required = queries.evidence_pack_required_queries == queries.total_queries
    preview_trace_required = queries.preview_trace_required_queries == queries.total_queries
    policy_check_required = queries.policy_check_required_queries == queries.total_queries
    source_attribution_required = queries.source_attribution_required_queries == queries.total_queries

    approval_required_for_allowed_writes = writes.approval_required_write_requests == allowed_write_requests
    approval_granted_by_default = writes.approval_granted_write_requests == 0
    sandbox_stage_required_for_allowed_writes = writes.sandbox_stage_required_write_requests == allowed_write_requests
    diff_preview_required_for_allowed_writes = writes.diff_preview_required_write_requests == allowed_write_requests
    risk_summary_required_for_allowed_writes = writes.risk_summary_required_write_requests == allowed_write_requests

    allowed_domains_ready = allowed_domains == _ALLOWED_DOMAINS

    guard_validation_ready = (
        allowed_domains_ready
        and forbidden_domains_absent
        and adapter_ready
        and capability_ready
        and query_ready
        and write_request_ready
        and evidence_pack_required
        and preview_trace_required
        and policy_check_required
        and source_attribution_required
        and approval_required_for_allowed_writes
        and approval_granted_by_default
        and sandbox_stage_required_for_allowed_writes
        and diff_preview_required_for_allowed_writes
        and risk_summary_required_for_allowed_writes
        and no_source_of_truth
        and no_canonical_truth
        and no_regulatory_memory
        and no_enterprise_policy_memory
        and no_technical_truth
        and no_audit_truth
        and no_approval_truth
        and no_canonical_write
        and no_auto_promotion
        and no_auto_conflict_resolution
        and no_runtime_mutation
    )

    return MemPalaceGuardValidationReport(
        allowed_domains=allowed_domains,
        forbidden_domains=_FORBIDDEN_CANONICAL_DOMAINS,
        allowed_domains_ready=allowed_domains_ready,
        forbidden_domains_absent=forbidden_domains_absent,
        adapter_ready=adapter_ready,
        capability_ready=capability_ready,
        query_ready=query_ready,
        write_request_ready=write_request_ready,
        evidence_pack_required=evidence_pack_required,
        preview_trace_required=preview_trace_required,
        policy_check_required=policy_check_required,
        source_attribution_required=source_attribution_required,
        approval_required_for_allowed_writes=approval_required_for_allowed_writes,
        approval_granted_by_default=approval_granted_by_default,
        sandbox_stage_required_for_allowed_writes=sandbox_stage_required_for_allowed_writes,
        diff_preview_required_for_allowed_writes=diff_preview_required_for_allowed_writes,
        risk_summary_required_for_allowed_writes=risk_summary_required_for_allowed_writes,
        no_source_of_truth=no_source_of_truth,
        no_canonical_truth=no_canonical_truth,
        no_regulatory_memory=no_regulatory_memory,
        no_enterprise_policy_memory=no_enterprise_policy_memory,
        no_technical_truth=no_technical_truth,
        no_audit_truth=no_audit_truth,
        no_approval_truth=no_approval_truth,
        no_canonical_write=no_canonical_write,
        no_auto_promotion=no_auto_promotion,
        no_auto_conflict_resolution=no_auto_conflict_resolution,
        no_runtime_mutation=no_runtime_mutation,
        guard_validation_ready=guard_validation_ready,
    )
