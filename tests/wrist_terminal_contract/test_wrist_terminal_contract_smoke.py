from __future__ import annotations

from MAKSIMAR_CORE_LIB.wrist_terminal_contract import (
    build_wrist_terminal_contract,
)


def test_wrist_terminal_contract_builds() -> None:
    """Wrist terminal contract should build successfully."""
    contract = build_wrist_terminal_contract()

    assert contract.total_entries == 1
    assert contract.secure_element_entries == 1
    assert contract.production_allowed_entries == 1
    assert contract.hybrid_ready_entries == 1
    assert contract.defined_entries == 1


def test_wrist_terminal_contract_contains_expected_entry() -> None:
    """Wrist terminal contract should expose expected entry."""
    contract = build_wrist_terminal_contract()
    entry = contract.entries[0]

    assert entry.wrist_terminal_id == "wrist_terminal_core_001"
    assert entry.role_stack == (
        "sensor_node",
        "control_node",
        "display_proxy",
        "future_autonomous_ai_node",
    )
    assert entry.communication_channels == ("wifi", "uwb", "bluetooth")
    assert entry.secure_element_required is True
    assert entry.identity_binding_required is True
    assert entry.haptic_feedback_required is True
    assert entry.gesture_input_required is True
    assert entry.microphone_array_required is True
    assert entry.local_display_logic_required is True
    assert entry.heavy_compute_local is False
    assert entry.display_engine_entry_id == "opticsengine_ar_glasses_projection_001"
    assert entry.security_binding == "owner_bound"
    assert entry.autonomy_stage == "hybrid_ready"
    assert entry.production_path_allowed is True
    assert entry.contract_status == "defined"
