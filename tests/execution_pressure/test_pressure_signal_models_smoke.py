from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_pressure import (
    build_pressure_signal_contract,
)


def test_pressure_signal_contract_builds() -> None:
    """Pressure signal contract should build successfully."""
    contract = build_pressure_signal_contract()

    assert contract.total_signals == 5
    assert len(contract.signals) == 5


def test_pressure_signal_contract_contains_expected_signal_kinds() -> None:
    """Pressure signal contract should expose expected pressure signals."""
    contract = build_pressure_signal_contract()

    signal_kinds = {entry.signal_kind for entry in contract.signals}

    assert "cpu_pressure" in signal_kinds
    assert "ram_pressure" in signal_kinds
    assert "queue_pressure" in signal_kinds
    assert "worker_saturation" in signal_kinds
    assert "artifact_storage_pressure" in signal_kinds


def test_pressure_signal_contract_thresholds_are_monotonic() -> None:
    """Pressure signal thresholds should increase monotonically."""
    contract = build_pressure_signal_contract()

    for entry in contract.signals:
        assert entry.elevated_threshold < entry.high_threshold
        assert entry.high_threshold < entry.critical_threshold
        assert entry.default_level_below_elevated == "normal"
