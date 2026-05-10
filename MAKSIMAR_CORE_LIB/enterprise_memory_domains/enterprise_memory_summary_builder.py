from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.enterprise_memory_domains.customer_metrics_memory_models import (
    build_customer_metrics_memory_contract,
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


def build_enterprise_memory_summary() -> Dict[str, object]:
    tenants = build_tenant_memory_scope_contract()
    jurisdictions = build_legal_jurisdiction_contract()
    regulatory = build_regulatory_memory_contract()
    isolation = build_memory_isolation_contract()
    policies = build_enterprise_policy_memory_contract()
    metrics = build_customer_metrics_memory_contract()

    runtime_policy_binding_allowed = (
        tenants.runtime_policy_approved_scopes
        + regulatory.runtime_policy_binding_allowed_records
        + isolation.runtime_policy_binding_allowed_isolations
        + policies.runtime_policy_binding_allowed_policies
        + metrics.runtime_policy_binding_allowed_metrics
    )

    cross_boundary_merge_allowed = (
        isolation.cross_tenant_merge_allowed_isolations
        + isolation.cross_business_merge_allowed_isolations
        + isolation.cross_country_merge_allowed_isolations
        + metrics.cross_tenant_aggregation_allowed_metrics
    )

    summary_ready = (
        tenants.ready_scopes == tenants.total_scopes
        and jurisdictions.ready_jurisdictions == jurisdictions.total_jurisdictions
        and regulatory.ready_records == regulatory.total_records
        and isolation.ready_isolations == isolation.total_isolations
        and policies.ready_policies == policies.total_policies
        and metrics.ready_metrics == metrics.total_metrics
        and regulatory.pending_approval_records == regulatory.total_records
        and policies.pending_approval_policies == policies.total_policies
        and runtime_policy_binding_allowed == 0
        and cross_boundary_merge_allowed == 0
        and metrics.pii_exposure_allowed_metrics == 0
    )

    return {
        "tenant_scopes": tenants.total_scopes,
        "tenant_ready_scopes": tenants.ready_scopes,
        "legal_jurisdictions": jurisdictions.total_jurisdictions,
        "legal_ready_jurisdictions": jurisdictions.ready_jurisdictions,
        "regulatory_records": regulatory.total_records,
        "regulatory_ready_records": regulatory.ready_records,
        "regulatory_pending_approval_records": regulatory.pending_approval_records,
        "memory_isolations": isolation.total_isolations,
        "memory_ready_isolations": isolation.ready_isolations,
        "enterprise_policy_records": policies.total_policies,
        "enterprise_policy_ready_records": policies.ready_policies,
        "enterprise_policy_pending_approval_records": policies.pending_approval_policies,
        "customer_metrics_records": metrics.total_metrics,
        "customer_metrics_ready_records": metrics.ready_metrics,
        "country_bound_records": regulatory.country_bound_records,
        "runtime_policy_binding_allowed": runtime_policy_binding_allowed,
        "cross_boundary_merge_allowed": cross_boundary_merge_allowed,
        "pii_exposure_allowed_metrics": metrics.pii_exposure_allowed_metrics,
        "summary_ready": summary_ready,
    }
