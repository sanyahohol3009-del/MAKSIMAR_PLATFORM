from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_source_version_precedence_preview


def test_source_version_precedence_acceptance_smoke() -> None:
    doc = Path("docs/architecture/foundation/regulatory_source_version_effective_date_precedence_v1.md")
    preview = build_source_version_precedence_preview()

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert preview["current_step"] == "STEP 4 — Source Version / Effective Date / Precedence"
    assert preview["next_step"] == "STEP 5 — Regulatory Conflict / Drift / Supersession"
    assert preview["source_version_required"] is True
    assert preview["effective_date_required"] is True
    assert preview["jurisdiction_id_required"] is True
    assert preview["tenant_scope_id_required"] is True
    assert preview["precedence_required"] is True
    assert preview["automatic_resolution_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed_now"] is False
