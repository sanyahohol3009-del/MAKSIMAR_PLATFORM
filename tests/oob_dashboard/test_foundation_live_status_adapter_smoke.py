from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_live_status_adapter import (
    _normalize_status_output,
    build_foundation_live_status_snapshot,
)


def test_normalize_status_output_alive() -> None:
    """Status output with ALIVE state should normalize to ALIVE."""
    assert _normalize_status_output("[ctl] state:\n  ALIVE") == "ALIVE"


def test_normalize_status_output_dead() -> None:
    """Status output with DEAD state should normalize to DEAD."""
    assert _normalize_status_output("[guard_ctl] state:\n  DEAD") == "DEAD"


def test_normalize_status_output_degraded() -> None:
    """Status output with DEGRADED state should normalize to DEGRADED."""
    assert _normalize_status_output("[ctl] state:\n  DEGRADED") == "DEGRADED"


def test_build_foundation_live_status_snapshot_shape() -> None:
    """Foundation live status snapshot should expose expected shape."""
    snapshot = build_foundation_live_status_snapshot()

    assert snapshot.total_records == 4
    assert len(snapshot.records) == 4
    assert [record.truth_scope for record in snapshot.records] == [
        "runtime",
        "guard",
        "core_guard",
        "kernel_guard",
    ]

    for record in snapshot.records:
        assert record.display_title
        assert record.status_command.startswith("./tools/")
        assert record.derived_state in {
            "ALIVE",
            "DEAD",
            "DEGRADED",
            "BROKEN",
            "WARMING_UP",
        }
        assert record.signal_path_visible is True
        assert record.execution_stage_visible is True
        assert record.read_only is True
