from __future__ import annotations

from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import (
    build_skill_adapter_registry_contract,
)


def test_skill_adapter_registry_contract_builds() -> None:
    """Skill adapter registry contract should build successfully."""
    contract = build_skill_adapter_registry_contract()

    assert contract.total_entries == 1
    assert contract.active_entries == 1
    assert contract.sandboxed_entries == 1
    assert contract.engine_adapter_entries == 1


def test_skill_adapter_registry_contract_contains_expected_entry() -> None:
    """Skill adapter registry contract should expose expected skill adapter."""
    contract = build_skill_adapter_registry_contract()
    entry = contract.entries[0]

    assert entry.module_slug == "simulation_analysis"
    assert entry.module_id == "module_skill_simulation_analysis"
    assert entry.skill_id == "skill_simulation_simulation_analysis"
    assert entry.worker_id == "worker_simulation_analysis_001"
    assert entry.domain_class == "simulation"
    assert entry.adapter_execution_mode == "sandboxed"


def test_skill_adapter_registry_contract_preserves_contracts_and_metadata() -> None:
    """Skill adapter registry should preserve manifest contracts and metadata."""
    contract = build_skill_adapter_registry_contract()
    entry = contract.entries[0]

    assert entry.input_contract_ids == (
        "simulation_engine_request",
        "validation_context",
    )
    assert entry.output_contract_ids == (
        "simulation_engine_result",
        "proposal_package",
    )
    assert entry.panel_ids == ("panel_simulation_skill_overview",)
    assert entry.supported_languages == ("en", "ru", "uk", "de")
    assert entry.supported_scripts == ("Latin", "Cyrillic")
    assert entry.engine_adapter_required is True
    assert entry.registration_status == "registered"
