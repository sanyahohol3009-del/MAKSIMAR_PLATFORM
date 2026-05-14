from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple


PROJECT_ROOT = Path(__file__).resolve().parents[2]

ACCEPTANCE_DOCS: Tuple[str, ...] = (
    "docs/architecture/roadmap_index/four_roadmap_consolidated_audit_v1.md",
    "docs/architecture/foundation/phase_5_2_final_dashboard_memory_map_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_0_product_ready_hardening_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_1_governance_federation_gap_pass_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_2_proposal_audit_approval_spine_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_3_controlled_codegen_context_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_4_sandbox_simulation_owner_review_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_5_bootstrapped_self_expansion_gate_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_6_client_metrics_learning_input_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_7_polyglot_model_worker_bridge_acceptance_v1.md",
    "docs/architecture/foundation/phase_6_8_productization_sale_ready_sovereign_ai_acceptance_v1.md",
)


@dataclass(frozen=True, slots=True)
class FinalAcceptanceIndex:
    index_id: str
    roadmap_family: str
    closed_phase: str
    acceptance_docs: Tuple[str, ...]
    missing_acceptance_docs: Tuple[str, ...]
    acceptance_index_ready: bool
    final_closure_allowed: bool

    def __post_init__(self) -> None:
        if not self.index_id:
            raise ValueError("index_id must be non-empty")
        if self.roadmap_family != "memory_roadmap_v5_1":
            raise ValueError("roadmap_family must be memory_roadmap_v5_1")
        if self.closed_phase != "PHASE 6.8":
            raise ValueError("closed_phase must be PHASE 6.8")
        if not self.acceptance_docs:
            raise ValueError("acceptance_docs must be non-empty")
        if self.missing_acceptance_docs:
            raise ValueError(f"missing acceptance docs: {self.missing_acceptance_docs}")
        if self.acceptance_index_ready is not True:
            raise ValueError("acceptance_index_ready must be True")
        if self.final_closure_allowed is not True:
            raise ValueError("final_closure_allowed must be True")


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_final_acceptance_index() -> FinalAcceptanceIndex:
    missing = _missing(ACCEPTANCE_DOCS)

    return FinalAcceptanceIndex(
        index_id="final_acceptance_index_memory_roadmap_v5_1_001",
        roadmap_family="memory_roadmap_v5_1",
        closed_phase="PHASE 6.8",
        acceptance_docs=ACCEPTANCE_DOCS,
        missing_acceptance_docs=missing,
        acceptance_index_ready=missing == (),
        final_closure_allowed=missing == (),
    )


def build_final_acceptance_index_preview() -> Dict[str, object]:
    index = build_final_acceptance_index()

    return {
        "preview_id": "final_acceptance_index_preview_memory_roadmap_v5_1_001",
        "preview_ready": index.acceptance_index_ready,
        "roadmap_family": index.roadmap_family,
        "closed_phase": index.closed_phase,
        "acceptance_doc_count": len(index.acceptance_docs),
        "acceptance_docs": index.acceptance_docs,
        "missing_acceptance_docs": index.missing_acceptance_docs,
        "final_closure_allowed": index.final_closure_allowed,
    }
