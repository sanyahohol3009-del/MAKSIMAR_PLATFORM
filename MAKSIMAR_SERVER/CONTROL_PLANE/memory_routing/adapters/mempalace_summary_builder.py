from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_adapter_models import (
    build_mempalace_adapter_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_capability_builder import (
    build_mempalace_capability_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_guard_validators import (
    build_mempalace_guard_validation_report,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_query_models import (
    build_mempalace_query_contract,
)
from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters.mempalace_write_models import (
    build_mempalace_write_request_contract,
)


def build_mempalace_summary() -> Dict[str, object]:
    adapter = build_mempalace_adapter_contract()
    capabilities = build_mempalace_capability_contract()
    queries = build_mempalace_query_contract()
    writes = build_mempalace_write_request_contract()
    guards = build_mempalace_guard_validation_report()

    summary_ready = (
        adapter.ready_adapters == adapter.total_adapters
        and capabilities.ready_capabilities == capabilities.total_capabilities
        and queries.ready_queries == queries.total_queries
        and writes.ready_write_requests == writes.total_write_requests
        and guards.guard_validation_ready
    )

    return {
        "adapters": adapter.total_adapters,
        "ready_adapters": adapter.ready_adapters,
        "capabilities": capabilities.total_capabilities,
        "ready_capabilities": capabilities.ready_capabilities,
        "queries": queries.total_queries,
        "ready_queries": queries.ready_queries,
        "write_requests": writes.total_write_requests,
        "ready_write_requests": writes.ready_write_requests,
        "allowed_write_requests": writes.allowed_write_requests,
        "approval_required_write_requests": writes.approval_required_write_requests,
        "approval_granted_write_requests": writes.approval_granted_write_requests,
        "sandbox_stage_required_write_requests": writes.sandbox_stage_required_write_requests,
        "diff_preview_required_write_requests": writes.diff_preview_required_write_requests,
        "risk_summary_required_write_requests": writes.risk_summary_required_write_requests,
        "source_of_truth_adapters": adapter.source_of_truth_adapters,
        "canonical_truth_allowed_capabilities": capabilities.canonical_truth_allowed_capabilities,
        "regulatory_memory_allowed_capabilities": capabilities.regulatory_memory_allowed_capabilities,
        "enterprise_policy_memory_allowed_capabilities": capabilities.enterprise_policy_memory_allowed_capabilities,
        "technical_truth_allowed_capabilities": capabilities.technical_truth_allowed_capabilities,
        "audit_truth_allowed_capabilities": capabilities.audit_truth_allowed_capabilities,
        "approval_truth_allowed_capabilities": capabilities.approval_truth_allowed_capabilities,
        "canonical_write_allowed": adapter.canonical_write_allowed_adapters + writes.canonical_write_allowed_write_requests,
        "auto_promotion_allowed": capabilities.auto_promotion_allowed_capabilities + writes.auto_promotion_allowed_write_requests,
        "auto_conflict_resolution_allowed": capabilities.auto_conflict_resolution_allowed_capabilities,
        "runtime_mutation_allowed": (
            adapter.runtime_mutation_allowed_adapters
            + capabilities.runtime_mutation_allowed_capabilities
            + queries.runtime_mutation_allowed_queries
            + writes.runtime_mutation_allowed_write_requests
        ),
        "guard_validation_ready": guards.guard_validation_ready,
        "summary_ready": summary_ready,
    }
