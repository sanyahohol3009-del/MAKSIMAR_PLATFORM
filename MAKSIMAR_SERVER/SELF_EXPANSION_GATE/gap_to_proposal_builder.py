from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.drift_detection import build_memory_drift_preview
from MAKSIMAR_SERVER.PROPOSAL_AUDIT import build_proposal_audit_preview
from MAKSIMAR_SERVER.SELF_EXPANSION_GATE.self_expansion_readiness_models import (
    build_self_expansion_readiness_contract,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_GAP_PROPOSAL_SURFACES: Tuple[str, ...] = (
    "MAKSIMAR_CORE_LIB/memory_engine/drift_detection/memory_drift_preview_builder.py",
    "MAKSIMAR_CORE_LIB/memory_engine/drift_detection/memory_contradiction_candidate_models.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/proposal_package_builder.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/proposal_package_models.py",
    "MAKSIMAR_CORE_LIB/evolution_loop/proposal_registry.py",
    "MAKSIMAR_SERVER/PROPOSAL_AUDIT/proposal_audit_preview_builder.py",
    "docs/security_governance/governed_action_model/PROPOSAL_TO_ACTION_TRANSITION_v1.md",
)


def _missing(paths: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(path for path in paths if not (PROJECT_ROOT / path).exists())


def build_gap_to_proposal_context() -> Dict[str, object]:
    readiness = build_self_expansion_readiness_contract()
    drift = build_memory_drift_preview()
    proposal_audit = build_proposal_audit_preview()
    missing = _missing(REQUIRED_GAP_PROPOSAL_SURFACES)

    gap_to_proposal_ready = (
        readiness.readiness_ready
        and drift["preview_ready"] is True
        and drift["auto_resolution_allowed"] is False
        and drift["canonical_truth_change_allowed"] is False
        and proposal_audit["preview_ready"] is True
        and missing == ()
    )

    return {
        "gap_to_proposal_context_id": "gap_to_proposal_context_phase_6_5_001",
        "gap_to_proposal_ready": gap_to_proposal_ready,
        "required_surfaces": REQUIRED_GAP_PROPOSAL_SURFACES,
        "missing_surfaces": missing,
        "source_drift_report_id": drift["report_id"],
        "candidate_ids": drift["candidate_ids"],
        "total_candidates": drift["total_candidates"],
        "human_review_required": drift["human_review_required"],
        "auto_resolution_allowed": drift["auto_resolution_allowed"],
        "canonical_truth_change_allowed": drift["canonical_truth_change_allowed"],
        "proposal_audit_preview_ready": proposal_audit["preview_ready"],
        "proposal_package_allowed": True,
        "direct_core_write_allowed": readiness.direct_core_write_allowed,
        "auto_apply_allowed": readiness.auto_apply_allowed,
        "deployment_allowed": readiness.deployment_allowed,
        "runtime_mutation_allowed": readiness.runtime_mutation_allowed,
    }
