from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_read_model import (
    build_panel_registry_read_model,
)


def test_panel_registry_read_model_smoke() -> None:
    read_model = build_panel_registry_read_model()

    assert len(read_model.rows) == 8
    assert read_model.rows[0].panel_id == "system_status"
    assert read_model.rows[-1].panel_id == "audit_timeline"


def test_panel_registry_read_model_titles_are_present() -> None:
    read_model = build_panel_registry_read_model()

    for row in read_model.rows:
        assert row.title
        assert row.panel_family
        assert row.panel_kind
