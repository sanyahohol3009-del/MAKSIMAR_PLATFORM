from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_immutable_core_binding_view import (
    build_foundation_immutable_core_binding_view,
)


def test_foundation_immutable_core_binding_view_counts() -> None:
    """Immutable-core binding view should expose expected counts."""
    view = build_foundation_immutable_core_binding_view()

    assert view.view_id == "foundation_immutable_core_binding_view_001"
    assert view.total_entries == 5
    assert view.immutable_candidate_entries == 5
    assert view.integrity_visible_entries == 5
    assert view.dashboard_visible_entries == 5
    assert view.verification_required_entries == 5
    assert view.mutation_forbidden_entries == 5


def test_foundation_immutable_core_binding_view_stop_gate_entry() -> None:
    """Immutable-core binding view should expose STOP-GATE entry."""
    view = build_foundation_immutable_core_binding_view()
    entry = view.entries[0]

    assert entry.binding_entry_id == "foundationimmutable_stop_gate_001"
    assert entry.core_artifact_id == "core_stop_gate_001"
    assert entry.artifact_path == "CORE_ROOT/stop_gate.py"
    assert entry.immutable_candidate is True
    assert entry.integrity_visible is True
    assert entry.dashboard_visible is True
    assert entry.mutation_allowed_from_dashboard is False
    assert entry.verification_required_before_start is True


def test_foundation_immutable_core_binding_view_genesis_hash_entry() -> None:
    """Immutable-core binding view should expose genesis hash entry."""
    view = build_foundation_immutable_core_binding_view()
    entry = view.entries[-1]

    assert entry.binding_entry_id == "foundationimmutable_genesis_hash_001"
    assert entry.core_artifact_id == "core_genesis_hash_001"
    assert entry.artifact_path == "CORE_ROOT/genesis_hash.bin"
    assert entry.immutable_candidate is True
    assert entry.integrity_visible is True
    assert entry.dashboard_visible is True
    assert entry.mutation_allowed_from_dashboard is False
    assert entry.verification_required_before_start is True


def test_foundation_immutable_core_binding_view_order() -> None:
    """Immutable-core binding view should preserve canonical artifact order."""
    view = build_foundation_immutable_core_binding_view()

    assert [entry.artifact_path for entry in view.entries] == [
        "CORE_ROOT/stop_gate.py",
        "CORE_ROOT/stop_gate_watcher.py",
        "CORE_ROOT/core_guard.py",
        "CORE_ROOT/core_integrity_verifier.py",
        "CORE_ROOT/genesis_hash.bin",
    ]
