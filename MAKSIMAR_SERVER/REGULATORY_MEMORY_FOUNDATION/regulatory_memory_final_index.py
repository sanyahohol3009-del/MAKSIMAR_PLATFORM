from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_routing_preview_builder import (
    build_regulatory_routing_preview,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REGULATORY_ACCEPTANCE_DOCS: Tuple[str, ...] = (
    "docs/architecture/foundation/regulatory_track_entry_surface_inventory_v1.md",
    "docs/architecture/foundation/country_jurisdiction_registry_binding_v1.md",
    "docs/architecture/foundation/tenant_regulatory_scope_isolation_v1.md",
    "docs/architecture/foundation/regulatory_source_version_effective_date_precedence_v1.md",
    "docs/architecture/foundation/regulatory_conflict_drift_supersession_v1.md",
    "docs/architecture/foundation/compliance_evidence_pack_audit_read_model_v1.md",
    "docs/architecture/foundation/regulatory_update_approval_gate_v1.md",
    "docs/architecture/foundation/regulatory_memory_routing_no_cross_tenant_leak_v1.md",
    "docs/architecture/roadmap_index/regulatory_memory_final_closure_v1.md",
    "docs/architecture/roadmap_index/memory_foundation_complete_final_closure_v1.md",
)

CLOSED_REGULATORY_STEPS: Tuple[str, ...] = (
    "STEP 1 — Regulatory Track Entry / Surface Inventory",
    "STEP 2 — Country / Jurisdiction Registry Binding",
    "STEP 3 — Tenant Regulatory Scope & Isolation",
    "STEP 4 — Source Version / Effective Date / Precedence",
    "STEP 5 — Regulatory Conflict / Drift / Supersession",
    "STEP 6 — Compliance Evidence Pack / Audit Read Model",
    "STEP 7 — Regulatory Update Approval Gate",
    "STEP 8 — Regulatory Routing / No Cross-Tenant Leak",
    "STEP 9 — Regulatory Memory Final Closure",
)


@dataclass(frozen=True, slots=True)
class RegulatoryMemoryFinalIndex:
    index_id: str
    roadmap_family: str
    closed_steps: Tuple[str, ...]
    acceptance_docs: Tuple[str, ...]
    missing_acceptance_docs: Tuple[str, ...]
    routing_preview_ready: bool
    final_index_ready: bool
    runtime_mutation_allowed: bool
    direct_core_write_allowed: bool
    deployment_allowed_now: bool
    external_release_allowed_now: bool

    def __post_init__(self) -> None:
        if not self.index_id:
            raise ValueError("index_id must be non-empty")
        if self.roadmap_family != "regulatory_memory_foundation":
            raise ValueError("roadmap_family must be regulatory_memory_foundation")
        if len(self.closed_steps) != 9:
            raise ValueError("closed_steps must contain exactly 9 steps")
        if len(self.acceptance_docs) != 10:
            raise ValueError("acceptance_docs must contain exactly 10 docs")
        if self.missing_acceptance_docs:
            raise ValueError(f"missing acceptance docs: {self.missing_acceptance_docs}")
        if self.routing_preview_ready is not True:
            raise ValueError("routing_preview_ready must be True")
        if self.final_index_ready is not True:
            raise ValueError("final_index_ready must be True")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if self.external_release_allowed_now:
            raise ValueError("external_release_allowed_now must be False")


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_regulatory_memory_final_index() -> RegulatoryMemoryFinalIndex:
    routing = build_regulatory_routing_preview()
    missing = _missing(REGULATORY_ACCEPTANCE_DOCS)

    return RegulatoryMemoryFinalIndex(
        index_id="regulatory_memory_final_index_001",
        roadmap_family="regulatory_memory_foundation",
        closed_steps=CLOSED_REGULATORY_STEPS,
        acceptance_docs=REGULATORY_ACCEPTANCE_DOCS,
        missing_acceptance_docs=missing,
        routing_preview_ready=routing["preview_ready"],
        final_index_ready=routing["preview_ready"] is True and missing == (),
        runtime_mutation_allowed=False,
        direct_core_write_allowed=False,
        deployment_allowed_now=False,
        external_release_allowed_now=False,
    )


def build_regulatory_memory_final_index_preview() -> Dict[str, object]:
    index = build_regulatory_memory_final_index()

    return {
        "preview_id": "regulatory_memory_final_index_preview_001",
        "preview_ready": index.final_index_ready,
        "index_id": index.index_id,
        "roadmap_family": index.roadmap_family,
        "closed_step_count": len(index.closed_steps),
        "closed_steps": index.closed_steps,
        "acceptance_doc_count": len(index.acceptance_docs),
        "acceptance_docs": index.acceptance_docs,
        "missing_acceptance_docs": index.missing_acceptance_docs,
        "routing_preview_ready": index.routing_preview_ready,
        "runtime_mutation_allowed": index.runtime_mutation_allowed,
        "direct_core_write_allowed": index.direct_core_write_allowed,
        "deployment_allowed_now": index.deployment_allowed_now,
        "external_release_allowed_now": index.external_release_allowed_now,
    }
