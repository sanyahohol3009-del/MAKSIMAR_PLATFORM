from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.effective_date_precedence_models import (
    build_effective_date_precedence_matrix,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.legal_precedence_resolver import (
    build_legal_precedence_resolver_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_source_version_models import (
    build_regulatory_source_version_registry,
)


def build_source_version_precedence_preview() -> Dict[str, object]:
    registry = build_regulatory_source_version_registry()
    matrix = build_effective_date_precedence_matrix()
    resolver = build_legal_precedence_resolver_preview()

    preview_path = (
        "regulatory_source_version_models",
        "effective_date_precedence_models",
        "legal_precedence_resolver",
        "regulatory_conflict_drift_supersession_next",
    )

    preview_ready = (
        registry.registry_ready
        and matrix.matrix_ready
        and resolver["preview_ready"] is True
        and registry.source_version_required
        and registry.effective_date_required
        and registry.precedence_required
    )

    return {
        "preview_id": "source_version_precedence_preview_step_4_001",
        "preview_ready": preview_ready,
        "roadmap_family": "regulatory_memory_foundation",
        "current_step": "STEP 4 — Source Version / Effective Date / Precedence",
        "next_step": "STEP 5 — Regulatory Conflict / Drift / Supersession",
        "preview_path": preview_path,
        "registry_id": registry.registry_id,
        "source_count": len(registry.sources),
        "precedence_entry_count": len(matrix.entries),
        "applicable_source_refs": resolver["applicable_source_refs"],
        "draft_review_source_refs": resolver["draft_review_source_refs"],
        "source_version_required": registry.source_version_required,
        "effective_date_required": registry.effective_date_required,
        "jurisdiction_id_required": registry.jurisdiction_id_required,
        "tenant_scope_id_required": registry.tenant_scope_id_required,
        "precedence_required": registry.precedence_required,
        "approval_required": registry.approval_required,
        "human_review_required": resolver["human_review_required"],
        "automatic_resolution_allowed": resolver["automatic_resolution_allowed"],
        "canonical_truth_update_allowed": registry.canonical_truth_update_allowed,
        "runtime_mutation_allowed": registry.runtime_mutation_allowed,
        "direct_core_write_allowed": registry.direct_core_write_allowed,
        "deployment_allowed_now": registry.deployment_allowed_now,
    }
