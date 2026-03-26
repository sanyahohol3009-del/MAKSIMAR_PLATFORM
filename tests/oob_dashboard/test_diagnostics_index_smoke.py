from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_state_snapshot,
    build_diagnostics_index,
)


def test_diagnostics_index_builds() -> None:
    """Diagnostics index should build successfully."""
    snapshot = build_dashboard_state_snapshot()
    diagnostics = build_diagnostics_index(snapshot)

    assert diagnostics.total_hints == 4
    assert len(diagnostics.hints) == 4


def test_diagnostics_index_contains_expected_sources() -> None:
    """Diagnostics index should contain expected diagnostic sources."""
    snapshot = build_dashboard_state_snapshot()
    diagnostics = build_diagnostics_index(snapshot)

    assert any(hint.source_name == "platform_self_check" for hint in diagnostics.hints)
    assert any(hint.source_name == "alert_policy" for hint in diagnostics.hints)
