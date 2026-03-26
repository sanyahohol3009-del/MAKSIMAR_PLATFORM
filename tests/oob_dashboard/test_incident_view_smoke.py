from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import build_dashboard_incident_view


def test_dashboard_incident_view_builds() -> None:
    """Dashboard incident view should build successfully."""
    view = build_dashboard_incident_view()

    assert view.overall_status == "ok"
    assert view.total_lines == 4
    assert len(view.lines) == 4


def test_dashboard_incident_view_contains_locations() -> None:
    """Dashboard incident view should contain localized incident sources."""
    view = build_dashboard_incident_view()

    assert any(line.incident_name == "health_failed_domains" for line in view.lines)
    assert any("MAKSIMAR_CORE_LIB" in line.probable_location for line in view.lines)
