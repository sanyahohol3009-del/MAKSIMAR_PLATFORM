from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_pressure import (
    build_pressure_level_contract,
)


def test_pressure_level_contract_builds() -> None:
    """Pressure level contract should build successfully."""
    contract = build_pressure_level_contract()

    assert contract.total_levels == 4
    assert len(contract.levels) == 4


def test_pressure_level_contract_contains_expected_levels() -> None:
    """Pressure level contract should expose expected pressure levels."""
    contract = build_pressure_level_contract()

    assert contract.levels[0].pressure_level == "normal"
    assert contract.levels[1].pressure_level == "elevated"
    assert contract.levels[2].pressure_level == "high"
    assert contract.levels[3].pressure_level == "critical"


def test_pressure_level_contract_marks_high_and_critical_for_protection() -> None:
    """High and critical pressure levels should require protection semantics."""
    contract = build_pressure_level_contract()

    high = contract.levels[2]
    critical = contract.levels[3]

    assert high.throttling_required is True
    assert high.degraded_mode_candidate is True
    assert critical.throttling_required is True
    assert critical.degraded_mode_candidate is True
