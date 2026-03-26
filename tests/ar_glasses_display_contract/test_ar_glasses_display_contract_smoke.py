from __future__ import annotations

from MAKSIMAR_CORE_LIB.ar_glasses_display_contract import (
    build_ar_glasses_display_contract,
)


def test_ar_glasses_display_contract_builds() -> None:
    """AR glasses display contract should build successfully."""
    contract = build_ar_glasses_display_contract()

    assert contract.total_entries == 1
    assert contract.private_display_entries == 1
    assert contract.anchor_required_entries == 1
    assert contract.production_allowed_entries == 1
    assert contract.defined_entries == 1


def test_ar_glasses_display_contract_contains_expected_entry() -> None:
    """AR glasses display contract should expose expected entry."""
    contract = build_ar_glasses_display_contract()
    entry = contract.entries[0]

    assert entry.ar_display_id == "ar_glasses_display_core_001"
    assert entry.linked_optics_engine_id == "opticsengine_ar_glasses_projection_001"
    assert entry.linked_wrist_terminal_id == "wrist_terminal_core_001"
    assert entry.display_privacy_mode == "private_display"
    assert entry.anchor_mode == "spatial_anchor_required"
    assert entry.overlay_mode == "explanation_overlay_required"
    assert entry.gesture_binding_mode == "gesture_linked_interface"
    assert entry.display_transport_mode == "wrist_proxy_handoff"
    assert entry.private_render_required is True
    assert entry.explanation_overlay_required is True
    assert entry.spatial_anchor_required is True
    assert entry.production_path_allowed is True
    assert entry.display_status == "defined"
