from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_ids import (
    build_canonical_panel_ids,
    is_known_panel_id,
)


def test_canonical_panel_ids_exist_and_are_stable() -> None:
    panel_ids = build_canonical_panel_ids()

    assert panel_ids == (
        "system_status",
        "guard_chain",
        "incidents",
        "logs",
        "topology",
        "action_queue",
        "approval_queue",
        "audit_timeline",
    )


def test_canonical_panel_ids_are_unique() -> None:
    panel_ids = build_canonical_panel_ids()
    assert len(panel_ids) == len(set(panel_ids))


def test_canonical_panel_ids_are_non_empty_and_trimmed() -> None:
    panel_ids = build_canonical_panel_ids()

    for panel_id in panel_ids:
        assert panel_id
        assert panel_id == panel_id.strip()
        assert " " not in panel_id


def test_unknown_panel_id_is_rejected() -> None:
    assert is_known_panel_id("system_status") is True
    assert is_known_panel_id("nonexistent_panel") is False
