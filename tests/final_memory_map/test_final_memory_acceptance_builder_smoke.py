from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_acceptance


def test_final_memory_acceptance_builder_smoke() -> None:
    acceptance = build_final_memory_acceptance()

    assert acceptance["acceptance_ready"] is True
    assert acceptance["project_fully_visible_in_memory"] is False
    assert acceptance["inventory_coverage"] == "REGISTERED_NATIVE_SURFACES_ONLY"
    assert acceptance["whole_organism_inventory_complete"] is False
    assert acceptance["all_registered_modules_visible"] is True
    assert acceptance["all_storage_nodes_visible"] is True
    assert acceptance["all_retrieval_sources_visible"] is True



def test_preview_readiness_never_claims_complete_project_inventory(monkeypatch):
    from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import final_memory_acceptance_builder as owner
    preview = {"preview_ready": True, "dashboard_read_only": True,
        "canonical_write_allowed": False, "runtime_mutation_allowed": False,
        "summary": {"all_registered_modules_visible": True, "all_storage_nodes_visible": True,
                    "all_retrieval_sources_visible": True,
                    "inventory_coverage": "REGISTERED_NATIVE_SURFACES_ONLY",
                    "whole_organism_inventory_complete": False}}
    monkeypatch.setattr(owner, "build_final_memory_preview", lambda: preview)
    result = owner.build_final_memory_acceptance()
    assert result["acceptance_ready"] is True
    assert result["project_fully_visible_in_memory"] is False
    assert result["inventory_coverage"] == "REGISTERED_NATIVE_SURFACES_ONLY"
    assert result["whole_organism_inventory_complete"] is False
