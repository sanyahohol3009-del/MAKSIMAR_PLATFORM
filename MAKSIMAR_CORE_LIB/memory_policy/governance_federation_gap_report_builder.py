from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_policy.memory_federation_policy_models import (
    build_memory_federation_policy,
)
from MAKSIMAR_CORE_LIB.memory_policy.memory_source_priority_models import (
    build_memory_source_priority_policy,
)
from MAKSIMAR_CORE_LIB.memory_policy.memory_trust_scope_models import (
    build_memory_trust_scope_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_EXISTING_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/memory_policy/governance_binding_models.py",
    "MAKSIMAR_CORE_LIB/memory_policy/governance_preview_builder.py",
    "MAKSIMAR_CORE_LIB/memory_policy/governance_summary_builder.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_classification_policy.py",
    "MAKSIMAR_CORE_LIB/memory_policy/memory_policy_scope_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/tenant_memory_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/regulatory_memory_models.py",
    "MAKSIMAR_CORE_LIB/enterprise_memory_domains/enterprise_policy_memory_models.py",
    "MAKSIMAR_SERVER/MEMORY_PROMOTION_PIPELINE/memory_promotion_pipeline_contract.py",
    "MAKSIMAR_SERVER/MEMORY_CONFLICT_RESOLUTION/memory_conflict_resolution_contract.py",
    "MAKSIMAR_SERVER/MEMORY_SYNC/node_memory_scope_models.py",
    "MAKSIMAR_SERVER/CONTROL_PLANE/memory_routing/retrieval_scope_models.py",
)


def _missing_required_surfaces() -> Tuple[str, ...]:
    return tuple(path for path in REQUIRED_EXISTING_SURFACES if not (PROJECT_ROOT / path).exists())


def build_governance_federation_gap_report() -> Dict[str, object]:
    trust = build_memory_trust_scope_contract()
    priority = build_memory_source_priority_policy()
    federation = build_memory_federation_policy()
    missing = _missing_required_surfaces()

    existing_surfaces_reused = len(missing) == 0
    gap_pass_ready = (
        trust.trust_scope_ready
        and priority.source_priority_ready
        and federation.federation_policy_ready
        and existing_surfaces_reused
        and trust.tenant_personal_separation_ready
        and federation.cross_tenant_merge_allowed_without_approval is False
        and federation.automatic_federation_write_allowed is False
        and federation.runtime_mutation_allowed is False
    )

    return {
        "report_id": "governance_federation_gap_report_001",
        "roadmap_family": "memory_roadmap_v5_1",
        "current_step": "Governance / Federation Gap Pass",
        "existing_surfaces_reused": existing_surfaces_reused,
        "required_existing_surfaces": REQUIRED_EXISTING_SURFACES,
        "missing_required_surfaces": missing,
        "trust_scope_ready": trust.trust_scope_ready,
        "source_priority_ready": priority.source_priority_ready,
        "federation_policy_ready": federation.federation_policy_ready,
        "tenant_personal_separation_ready": trust.tenant_personal_separation_ready,
        "cross_tenant_merge_allowed_without_approval": federation.cross_tenant_merge_allowed_without_approval,
        "automatic_federation_write_allowed": federation.automatic_federation_write_allowed,
        "runtime_mutation_allowed": federation.runtime_mutation_allowed,
        "proposal_audit_allowed_next": gap_pass_ready,
        "codegen_allowed_now": False,
        "sandbox_allowed_now": False,
        "self_expansion_allowed_now": False,
        "gap_pass_ready": gap_pass_ready,
    }
