from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import (
    build_regulatory_conflict_drift_supersession_preview,
)


def test_regulatory_conflict_acceptance_smoke() -> None:
    doc = Path("docs/architecture/foundation/regulatory_conflict_drift_supersession_v1.md")
    preview = build_regulatory_conflict_drift_supersession_preview()

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert preview["current_step"] == "STEP 5 — Regulatory Conflict / Drift / Supersession"
    assert preview["next_step"] == "STEP 6 — Compliance Evidence Pack / Audit Read Model"
    assert preview["conflict_candidate_count"] >= 2
    assert preview["drift_signal_count"] >= 3
    assert preview["supersession_candidate_count"] >= 1
    assert preview["human_review_required"] is True
    assert preview["approval_required"] is True
    assert preview["supersession_applied"] is False
    assert preview["automatic_resolution_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed_now"] is False
