from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.enterprise_memory_domains.customer_metrics_memory_models import (
    build_customer_metrics_memory_contract,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_memory_preview_builder import (
    build_enterprise_memory_preview,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_memory_summary_builder import (
    build_enterprise_memory_summary,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.enterprise_policy_memory_models import (
    build_enterprise_policy_memory_contract,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.legal_jurisdiction_models import (
    build_legal_jurisdiction_contract,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.memory_isolation_models import (
    build_memory_isolation_contract,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.regulatory_memory_models import (
    build_regulatory_memory_contract,
)
from MAKSIMAR_CORE_LIB.enterprise_memory_domains.tenant_memory_models import (
    build_tenant_memory_scope_contract,
)


_FORBIDDEN_PHASE_ROOTS = (
    "runtime_legal_policy_executor",
    "legal_runtime_executor",
    "regulatory_runtime_executor",
    "tenant_merge_runtime",
    "country_merge_runtime",
)


@dataclass(frozen=True, slots=True)
class EnterpriseMemoryPhaseReadiness:
    tenant_scopes: int
    legal_jurisdictions: int
    regulatory_records: int
    memory_isolations: int
    enterprise_policy_records: int
    customer_metrics_records: int
    country_bound_records: int
    flow: Tuple[str, ...]
    tenant_scope_ready: bool
    jurisdiction_ready: bool
    regulatory_memory_ready: bool
    memory_isolation_ready: bool
    enterprise_policy_ready: bool
    customer_metrics_ready: bool
    source_bound_ready: bool
    versioning_ready: bool
    governance_gate_ready: bool
    pending_approval_ready: bool
    read_only_ready: bool
    no_runtime_policy_binding: bool
    no_cross_boundary_merge: bool
    no_pii_exposure: bool
    no_forbidden_runtime_roots: bool
    phase_ready: bool


def _no_forbidden_runtime_roots() -> bool:
    return not any(Path(root_name).exists() for root_name in _FORBIDDEN_PHASE_ROOTS)


def build_enterprise_memory_phase_readiness() -> EnterpriseMemoryPhaseReadiness:
    tenants = build_tenant_memory_scope_contract()
    jurisdictions = build_legal_jurisdiction_contract()
    regulatory = build_regulatory_memory_contract()
    isolation = build_memory_isolation_contract()
    policies = build_enterprise_policy_memory_contract()
    metrics = build_customer_metrics_memory_contract()
    summary = build_enterprise_memory_summary()
    preview = build_enterprise_memory_preview()

    tenant_scope_ready = tenants.ready_scopes == tenants.total_scopes
    jurisdiction_ready = jurisdictions.ready_jurisdictions == jurisdictions.total_jurisdictions
    regulatory_memory_ready = regulatory.ready_records == regulatory.total_records
    memory_isolation_ready = isolation.ready_isolations == isolation.total_isolations
    enterprise_policy_ready = policies.ready_policies == policies.total_policies
    customer_metrics_ready = metrics.ready_metrics == metrics.total_metrics

    source_bound_ready = (
        jurisdictions.source_bound_jurisdictions == jurisdictions.total_jurisdictions
        and regulatory.source_bound_records == regulatory.total_records
        and policies.source_bound_policies == policies.total_policies
    )
    versioning_ready = (
        jurisdictions.versioned_jurisdictions == jurisdictions.total_jurisdictions
        and regulatory.versioned_records == regulatory.total_records
        and policies.versioned_policies == policies.total_policies
    )
    governance_gate_ready = (
        jurisdictions.approval_required_jurisdictions == jurisdictions.total_jurisdictions
        and policies.governance_gate_required_policies == policies.total_policies
        and policies.approval_required_policies == policies.total_policies
    )
    pending_approval_ready = (
        regulatory.pending_approval_records == regulatory.total_records
        and policies.pending_approval_policies == policies.total_policies
    )
    read_only_ready = (
        tenants.read_only_scopes == tenants.total_scopes
        and jurisdictions.read_only_jurisdictions == jurisdictions.total_jurisdictions
        and regulatory.read_only_records == regulatory.total_records
        and isolation.read_only_isolations == isolation.total_isolations
        and policies.read_only_policies == policies.total_policies
        and metrics.read_only_metrics == metrics.total_metrics
    )

    no_runtime_policy_binding = int(summary["runtime_policy_binding_allowed"]) == 0
    no_cross_boundary_merge = int(summary["cross_boundary_merge_allowed"]) == 0
    no_pii_exposure = int(summary["pii_exposure_allowed_metrics"]) == 0
    no_forbidden_runtime_roots = _no_forbidden_runtime_roots()

    phase_ready = (
        bool(summary["summary_ready"])
        and bool(preview["preview_ready"])
        and tenant_scope_ready
        and jurisdiction_ready
        and regulatory_memory_ready
        and memory_isolation_ready
        and enterprise_policy_ready
        and customer_metrics_ready
        and source_bound_ready
        and versioning_ready
        and governance_gate_ready
        and pending_approval_ready
        and read_only_ready
        and no_runtime_policy_binding
        and no_cross_boundary_merge
        and no_pii_exposure
        and no_forbidden_runtime_roots
    )

    return EnterpriseMemoryPhaseReadiness(
        tenant_scopes=tenants.total_scopes,
        legal_jurisdictions=jurisdictions.total_jurisdictions,
        regulatory_records=regulatory.total_records,
        memory_isolations=isolation.total_isolations,
        enterprise_policy_records=policies.total_policies,
        customer_metrics_records=metrics.total_metrics,
        country_bound_records=regulatory.country_bound_records,
        flow=tuple(str(item) for item in preview["flow"]),
        tenant_scope_ready=tenant_scope_ready,
        jurisdiction_ready=jurisdiction_ready,
        regulatory_memory_ready=regulatory_memory_ready,
        memory_isolation_ready=memory_isolation_ready,
        enterprise_policy_ready=enterprise_policy_ready,
        customer_metrics_ready=customer_metrics_ready,
        source_bound_ready=source_bound_ready,
        versioning_ready=versioning_ready,
        governance_gate_ready=governance_gate_ready,
        pending_approval_ready=pending_approval_ready,
        read_only_ready=read_only_ready,
        no_runtime_policy_binding=no_runtime_policy_binding,
        no_cross_boundary_merge=no_cross_boundary_merge,
        no_pii_exposure=no_pii_exposure,
        no_forbidden_runtime_roots=no_forbidden_runtime_roots,
        phase_ready=phase_ready,
    )


def build_enterprise_memory_phase_preview() -> Dict[str, object]:
    readiness = build_enterprise_memory_phase_readiness()

    return {
        "flow": readiness.flow,
        "preview_ready": readiness.phase_ready,
        "phase_ready": readiness.phase_ready,
        "tenant_scopes": readiness.tenant_scopes,
        "legal_jurisdictions": readiness.legal_jurisdictions,
        "regulatory_records": readiness.regulatory_records,
        "memory_isolations": readiness.memory_isolations,
        "enterprise_policy_records": readiness.enterprise_policy_records,
        "customer_metrics_records": readiness.customer_metrics_records,
        "country_bound_records": readiness.country_bound_records,
        "tenant_scope_ready": readiness.tenant_scope_ready,
        "jurisdiction_ready": readiness.jurisdiction_ready,
        "regulatory_memory_ready": readiness.regulatory_memory_ready,
        "memory_isolation_ready": readiness.memory_isolation_ready,
        "enterprise_policy_ready": readiness.enterprise_policy_ready,
        "customer_metrics_ready": readiness.customer_metrics_ready,
        "source_bound_ready": readiness.source_bound_ready,
        "versioning_ready": readiness.versioning_ready,
        "governance_gate_ready": readiness.governance_gate_ready,
        "pending_approval_ready": readiness.pending_approval_ready,
        "read_only_ready": readiness.read_only_ready,
        "no_runtime_policy_binding": readiness.no_runtime_policy_binding,
        "no_cross_boundary_merge": readiness.no_cross_boundary_merge,
        "no_pii_exposure": readiness.no_pii_exposure,
        "no_forbidden_runtime_roots": readiness.no_forbidden_runtime_roots,
    }
