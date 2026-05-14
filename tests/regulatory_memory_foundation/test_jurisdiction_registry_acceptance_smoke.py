from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_jurisdiction_registry_preview


def test_jurisdiction_registry_acceptance_smoke() -> None:
    doc = Path("docs/architecture/foundation/country_jurisdiction_registry_binding_v1.md")
    preview = build_jurisdiction_registry_preview()

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert preview["current_step"] == "STEP 2 — Country / Jurisdiction Registry Binding"
    assert preview["next_step"] == "STEP 3 — Tenant Regulatory Scope & Isolation"
    assert preview["country_code_required"] is True
    assert preview["jurisdiction_id_required"] is True
    assert preview["applicability_scope_required"] is True
    assert preview["cross_jurisdiction_merge_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed_now"] is False
