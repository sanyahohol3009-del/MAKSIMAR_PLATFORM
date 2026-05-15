from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_conflict_models import (
    build_regulatory_conflict_registry,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_drift_detector import (
    build_regulatory_drift_preview,
)
from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION.regulatory_supersession_models import (
    build_regulatory_supersession_preview,
)


def build_regulatory_conflict_drift_supersession_preview() -> Dict[str, object]:
    conflict = build_regulatory_conflict_registry()
    drift = build_regulatory_drift_preview()
    supersession = build_regulatory_supersession_preview()

    preview_path = (
        "regulatory_conflict_models",
        "regulatory_drift_detector",
        "regulatory_supersession_models",
        "compliance_evidence_pack_next",
    )

    preview_ready = (
        conflict.conflict_detection_ready
        and drift["preview_ready"] is True
        and supersession["preview_ready"] is True
        and conflict.automatic_resolution_allowed is False
        and conflict.canonical_truth_update_allowed is False
    )

    return {
        "preview_id": "regulatory_conflict_drift_supersession_preview_step_5_001",
        "preview_ready": preview_ready,
        "roadmap_family": "regulatory_memory_foundation",
        "current_step": "STEP 5 — Regulatory Conflict / Drift / Supersession",
        "next_step": "STEP 6 — Compliance Evidence Pack / Audit Read Model",
        "preview_path": preview_path,
        "conflict_candidate_count": len(conflict.candidates),
        "conflict_candidate_ids": tuple(candidate.candidate_id for candidate in conflict.candidates),
        "drift_signal_count": drift["signal_count"],
        "drift_kinds": drift["drift_kinds"],
        "supersession_candidate_count": supersession["candidate_count"],
        "supersession_candidate_ids": supersession["candidate_ids"],
        "human_review_required": conflict.human_review_required,
        "approval_required": supersession["approval_required"],
        "supersession_applied": supersession["supersession_applied"],
        "automatic_resolution_allowed": conflict.automatic_resolution_allowed,
        "canonical_truth_update_allowed": conflict.canonical_truth_update_allowed,
        "runtime_mutation_allowed": conflict.runtime_mutation_allowed,
        "direct_core_write_allowed": conflict.direct_core_write_allowed,
        "deployment_allowed_now": conflict.deployment_allowed_now,
    }
