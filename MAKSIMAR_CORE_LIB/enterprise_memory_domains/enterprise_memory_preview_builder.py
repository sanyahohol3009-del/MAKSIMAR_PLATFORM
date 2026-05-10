from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.enterprise_memory_domains.customer_metrics_memory_models import (
    build_customer_metrics_memory_contract,
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


_ENTERPRISE_MEMORY_PREVIEW_FLOW = (
    "tenant_memory_scope",
    "legal_jurisdiction",
    "regulatory_memory",
    "memory_isolation",
    "enterprise_policy_memory",
    "customer_metrics_memory",
    "enterprise_memory_summary",
    "enterprise_memory_preview",
)


def build_enterprise_memory_preview() -> Dict[str, object]:
    tenants = build_tenant_memory_scope_contract()
    jurisdictions = build_legal_jurisdiction_contract()
    regulatory = build_regulatory_memory_contract()
    isolation = build_memory_isolation_contract()
    policies = build_enterprise_policy_memory_contract()
    metrics = build_customer_metrics_memory_contract()
    summary = build_enterprise_memory_summary()

    return {
        "flow": _ENTERPRISE_MEMORY_PREVIEW_FLOW,
        "preview_ready": bool(summary["summary_ready"]),
        "summary_ready": summary["summary_ready"],
        "tenant_scopes": summary["tenant_scopes"],
        "legal_jurisdictions": summary["legal_jurisdictions"],
        "regulatory_records": summary["regulatory_records"],
        "memory_isolations": summary["memory_isolations"],
        "enterprise_policy_records": summary["enterprise_policy_records"],
        "customer_metrics_records": summary["customer_metrics_records"],
        "country_bound_records": summary["country_bound_records"],
        "runtime_policy_binding_allowed": summary["runtime_policy_binding_allowed"],
        "cross_boundary_merge_allowed": summary["cross_boundary_merge_allowed"],
        "pii_exposure_allowed_metrics": summary["pii_exposure_allowed_metrics"],
        "tenant_ids": tuple(entry.tenant_id for entry in tenants.entries),
        "business_ids": tuple(entry.business_id for entry in tenants.entries),
        "client_ids": tuple(entry.client_id for entry in tenants.entries),
        "country_codes": tuple(entry.country_code for entry in tenants.entries),
        "jurisdiction_ids": tuple(entry.jurisdiction_id for entry in jurisdictions.entries),
        "regulatory_record_ids": tuple(entry.regulatory_record_id for entry in regulatory.entries),
        "isolation_ids": tuple(entry.isolation_id for entry in isolation.entries),
        "policy_record_ids": tuple(entry.policy_record_id for entry in policies.entries),
        "metrics_record_ids": tuple(entry.metrics_record_id for entry in metrics.entries),
    }
