from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
    build_memory_registry_view_summary,
)


def test_memory_registry_summary_builder_smoke() -> None:
    summary = build_memory_registry_view_summary()

    assert summary["summary_ready"] is True
    assert summary["read_only"] is True
    assert summary["action_exposure_allowed"] is False
    assert summary["display_orchestration_allowed"] is False
    assert summary["retrieval_phase_ready"] is True


def test_historical_preview_readiness_does_not_claim_live_acceptance() -> None:
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
        build_memory_registry_panel_contract, build_memory_registry_view_contract,
    )
    summary = build_memory_registry_view_summary()
    assert summary["readiness_scope"] == "HISTORICAL_METADATA_CONTRACT_PREVIEW"
    assert summary["live_runtime_acceptance"] is False
    for entry in (*build_memory_registry_panel_contract().entries,
                  *build_memory_registry_view_contract().entries):
        assert entry.readiness_scope == summary["readiness_scope"]


def test_registry_preview_reuses_jarvis_truth_without_completeness_promotion(monkeypatch) -> None:
    from MAKSIMAR_SERVER.AI_ORCHESTRATION import jarvis_live_read_models
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
        build_memory_registry_view_preview,
    )
    calls = []
    source = {"inventory_coverage": "REGISTERED_NATIVE_SURFACES_ONLY",
              "whole_organism_inventory_complete": False,
              "memory_surfaces_detected_count": 17, "physical_store_count": 7,
              "surfaces": [{"owner": "actual_owner", "writer": "actual_writer"}]}
    def read_canonical():
        calls.append(True)
        return source
    monkeypatch.setattr(jarvis_live_read_models, "build_jarvis_live_memory_federation_status", read_canonical)
    preview = build_memory_registry_view_preview()
    assert calls == [True]
    assert preview["overview"] is source
    assert preview["inventory_coverage"] == source["inventory_coverage"]
    assert preview["whole_organism_inventory_complete"] is False
    assert preview["live_runtime_acceptance"] is False
    # Dynamic counts and identities are forwarded, never inferred from sample panels.
    assert preview["overview"]["physical_store_count"] == 7
    assert preview["overview"]["memory_surfaces_detected_count"] == 17


def test_preview_entry_cannot_promote_readiness_scope_to_runtime_acceptance() -> None:
    import pytest
    from dataclasses import replace
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.memory_registry_views import (
        build_memory_registry_panel_contract, build_memory_registry_view_contract,
    )
    for entry in (build_memory_registry_panel_contract().entries[0],
                  build_memory_registry_view_contract().entries[0]):
        with pytest.raises(ValueError, match="cannot claim runtime acceptance"):
            replace(entry, readiness_scope="LIVE_VERIFIED")
