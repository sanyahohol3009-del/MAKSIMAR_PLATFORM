from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from MAKSIMAR_SERVER.PRODUCTIZATION import build_productization_preview
from MAKSIMAR_SERVER.ROADMAP_CLOSURE.final_acceptance_index import (
    build_final_acceptance_index_preview,
)


CLOSED_BLOCKS: Tuple[str, ...] = (
    "Four-Roadmap Consolidated Audit / Provenance Batch",
    "PHASE 6.0 Product-Ready Hardening",
    "PHASE 6.1 Governance / Federation Gap Pass",
    "PHASE 6.2 Proposal / Audit / Approval Spine",
    "PHASE 6.3 Controlled Codegen Context",
    "PHASE 6.4 Sandbox / Simulation / Owner Review",
    "PHASE 6.5 Bootstrapped Self-Expansion Gate",
    "PHASE 6.6 Client Metrics / Learning Input",
    "PHASE 6.7 Polyglot / Model / Worker Bridge",
    "PHASE 6.8 Productization / Sale-Ready Sovereign AI",
)

NEXT_ENTRYPOINTS: Tuple[str, ...] = (
    "visual/operator roadmap continuation",
    "multi-tenant/multi-country regulatory memory foundation",
    "network/security deployment boundary hardening",
    "real product packaging and operator documentation",
    "repository/document intelligence ingestion for project history",
)


@dataclass(frozen=True, slots=True)
class FinalContinuitySummary:
    summary_id: str
    roadmap_family: str
    closed_blocks: Tuple[str, ...]
    next_entrypoints: Tuple[str, ...]
    productization_ready: bool
    final_acceptance_index_ready: bool
    direct_core_write_allowed: bool
    auto_apply_allowed: bool
    runtime_mutation_allowed: bool
    deployment_allowed_now: bool
    external_release_allowed_now: bool
    continuity_summary_ready: bool

    def __post_init__(self) -> None:
        if not self.summary_id:
            raise ValueError("summary_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if not self.closed_blocks:
            raise ValueError("closed_blocks must be non-empty")
        if not self.next_entrypoints:
            raise ValueError("next_entrypoints must be non-empty")
        if self.productization_ready is not True:
            raise ValueError("productization_ready must be True")
        if self.final_acceptance_index_ready is not True:
            raise ValueError("final_acceptance_index_ready must be True")
        if self.direct_core_write_allowed:
            raise ValueError("direct_core_write_allowed must be False")
        if self.auto_apply_allowed:
            raise ValueError("auto_apply_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.deployment_allowed_now:
            raise ValueError("deployment_allowed_now must be False")
        if self.external_release_allowed_now:
            raise ValueError("external_release_allowed_now must be False")
        if self.continuity_summary_ready is not True:
            raise ValueError("continuity_summary_ready must be True")


def build_final_continuity_summary() -> FinalContinuitySummary:
    productization = build_productization_preview()
    index = build_final_acceptance_index_preview()

    return FinalContinuitySummary(
        summary_id="final_continuity_summary_memory_roadmap_v5_1_001",
        roadmap_family="memory_roadmap_v5_1",
        closed_blocks=CLOSED_BLOCKS,
        next_entrypoints=NEXT_ENTRYPOINTS,
        productization_ready=productization["preview_ready"],
        final_acceptance_index_ready=index["preview_ready"],
        direct_core_write_allowed=productization["direct_core_write_allowed"],
        auto_apply_allowed=productization["auto_apply_allowed"],
        runtime_mutation_allowed=productization["runtime_mutation_allowed"],
        deployment_allowed_now=productization["deployment_allowed_now"],
        external_release_allowed_now=productization["external_release_allowed_now"],
        continuity_summary_ready=productization["preview_ready"] is True and index["preview_ready"] is True,
    )


def build_final_continuity_preview() -> Dict[str, object]:
    summary = build_final_continuity_summary()

    return {
        "preview_id": "final_continuity_preview_memory_roadmap_v5_1_001",
        "preview_ready": summary.continuity_summary_ready,
        "roadmap_family": summary.roadmap_family,
        "closed_block_count": len(summary.closed_blocks),
        "closed_blocks": summary.closed_blocks,
        "next_entrypoints": summary.next_entrypoints,
        "productization_ready": summary.productization_ready,
        "final_acceptance_index_ready": summary.final_acceptance_index_ready,
        "direct_core_write_allowed": summary.direct_core_write_allowed,
        "auto_apply_allowed": summary.auto_apply_allowed,
        "runtime_mutation_allowed": summary.runtime_mutation_allowed,
        "deployment_allowed_now": summary.deployment_allowed_now,
        "external_release_allowed_now": summary.external_release_allowed_now,
    }
