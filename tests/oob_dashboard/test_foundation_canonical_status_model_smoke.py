from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_canonical_status_model import (
    build_foundation_canonical_status_model,
)


def test_foundation_canonical_status_model_counts() -> None:
    """Canonical foundation status model should expose expected counts."""
    model = build_foundation_canonical_status_model()

    assert model.total_statuses == 6
    assert model.live_statuses == 5
    assert model.terminal_statuses == 2
    assert model.historical_only_statuses == 1


def test_foundation_canonical_status_model_alive_entry() -> None:
    """Canonical foundation status model should expose ALIVE entry."""
    model = build_foundation_canonical_status_model()
    entry = model.entries[1]

    assert entry.status_id == "foundation_status_alive_001"
    assert entry.status == "ALIVE"
    assert entry.terminal is False
    assert entry.live_state is True
    assert entry.historical_only is False
    assert entry.severity == "info"


def test_foundation_canonical_status_model_broken_entry() -> None:
    """Canonical foundation status model should expose BROKEN entry."""
    model = build_foundation_canonical_status_model()
    entry = model.entries[4]

    assert entry.status_id == "foundation_status_broken_001"
    assert entry.status == "BROKEN"
    assert entry.terminal is True
    assert entry.live_state is True
    assert entry.historical_only is False
    assert entry.severity == "critical"


def test_foundation_canonical_status_model_order() -> None:
    """Canonical foundation status model should preserve expected order."""
    model = build_foundation_canonical_status_model()

    assert [entry.status for entry in model.entries] == [
        "WARMING_UP",
        "ALIVE",
        "DEGRADED",
        "DEAD",
        "BROKEN",
        "UNKNOWN",
    ]
