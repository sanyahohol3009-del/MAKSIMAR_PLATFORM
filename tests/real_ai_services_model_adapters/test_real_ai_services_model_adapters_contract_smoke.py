from __future__ import annotations

from MAKSIMAR_CORE_LIB.real_ai_services_model_adapters import (
    build_real_ai_services_model_adapters_contract,
)


def test_real_ai_services_model_adapters_contract_builds() -> None:
    """Real AI services / model adapters contract should build successfully."""
    contract = build_real_ai_services_model_adapters_contract()

    assert contract.total_entries == 3
    assert contract.reasoning_entries == 1
    assert contract.coding_entries == 1
    assert contract.visual_entries == 1
    assert contract.active_entries == 3


def test_real_ai_services_model_adapters_contract_contains_expected_reasoning_entry() -> None:
    """Real AI services / model adapters should expose expected reasoning entry."""
    contract = build_real_ai_services_model_adapters_contract()
    entry = contract.entries[0]

    assert entry.real_ai_service_entry_id == "aiservice_reasoning_001"
    assert entry.service_kind == "reasoning_service"
    assert entry.model_adapter_kind == "glm_adapter"
    assert entry.linked_real_backend_id == "realbackend_simulation_native_001"
    assert entry.linked_voice_runtime_entry_id == "realvoice_show_simulation_001"


def test_real_ai_services_model_adapters_contract_contains_expected_coding_entry() -> None:
    """Real AI services / model adapters should expose expected coding entry."""
    contract = build_real_ai_services_model_adapters_contract()
    entry = contract.entries[1]

    assert entry.real_ai_service_entry_id == "aiservice_coding_001"
    assert entry.service_kind == "coding_service"
    assert entry.model_adapter_kind == "qwen_adapter"
    assert entry.linked_real_backend_id == "realbackend_display_python_001"
    assert entry.linked_voice_runtime_entry_id == "realvoice_show_memory_001"


def test_real_ai_services_model_adapters_contract_contains_expected_visual_entry() -> None:
    """Real AI services / model adapters should expose expected visual entry."""
    contract = build_real_ai_services_model_adapters_contract()
    entry = contract.entries[2]

    assert entry.real_ai_service_entry_id == "aiservice_visual_001"
    assert entry.service_kind == "visual_service"
    assert entry.model_adapter_kind == "deepseek_adapter"
    assert entry.linked_real_backend_id == "realbackend_optics_gpu_001"
    assert entry.linked_voice_runtime_entry_id == "realvoice_show_monitoring_001"
