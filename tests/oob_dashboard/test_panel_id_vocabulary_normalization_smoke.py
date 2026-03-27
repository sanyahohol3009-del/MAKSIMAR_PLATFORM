from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_id_vocabulary_normalization import (
    build_panel_id_vocabulary_normalization_model,
    is_canonical_panel_id,
    normalize_panel_id,
)


def test_panel_id_vocabulary_normalization_counts() -> None:
    """Panel-id vocabulary normalization model should expose expected counts."""
    model = build_panel_id_vocabulary_normalization_model()

    assert model.total_entries == 19
    assert model.foundation_status_entries == 4
    assert model.read_only_monitoring_entries == 2
    assert model.diagnostics_entries == 2
    assert model.interaction_entries == 2
    assert model.control_entries == 1
    assert model.execution_observability_entries == 7
    assert model.navigation_entries == 1
    assert model.total_aliases == 2


def test_panel_id_vocabulary_normalization_aliases() -> None:
    """Panel-id vocabulary normalization should normalize known drift aliases."""
    assert normalize_panel_id("dashboard_consistency_panel") == "panel_consistency"
    assert normalize_panel_id("panel_gesture") == "panel_gesture_control"


def test_panel_id_vocabulary_normalization_keeps_canonical_ids() -> None:
    """Canonical panel ids should remain unchanged after normalization."""
    assert normalize_panel_id("panel_consistency") == "panel_consistency"
    assert normalize_panel_id("panel_queue_load") == "panel_queue_load"


def test_panel_id_vocabulary_normalization_canonical_checks() -> None:
    """Canonical check should identify canonical ids and reject alias ids."""
    assert is_canonical_panel_id("panel_consistency") is True
    assert is_canonical_panel_id("panel_gesture_control") is True
    assert is_canonical_panel_id("dashboard_consistency_panel") is False
    assert is_canonical_panel_id("panel_gesture") is False


def test_panel_id_vocabulary_normalization_foundation_entries_order() -> None:
    """Foundation status panel ids should preserve canonical order."""
    model = build_panel_id_vocabulary_normalization_model()

    foundation_ids = [
        entry.canonical_panel_id
        for entry in model.entries
        if entry.panel_family == "foundation_status"
    ]

    assert foundation_ids == [
        "panel_foundation_runtime_status_001",
        "panel_foundation_guard_status_001",
        "panel_foundation_core_guard_status_001",
        "panel_foundation_kernel_guard_status_001",
    ]
