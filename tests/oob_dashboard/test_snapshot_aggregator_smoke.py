from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import build_dashboard_state_snapshot


def test_dashboard_state_snapshot_builds() -> None:
    """Dashboard state snapshot should build successfully."""
    snapshot = build_dashboard_state_snapshot()

    assert snapshot.overall_status == "ok"
    assert snapshot.total_lines == 4
    assert len(snapshot.lines) == 4


def test_dashboard_state_snapshot_contains_expected_sources() -> None:
    """Dashboard snapshot should contain expected read-only sources."""
    snapshot = build_dashboard_state_snapshot()

    assert any(line.source_name == "platform_self_check" for line in snapshot.lines)
    assert any(line.source_name == "alert_policy" for line in snapshot.lines)
